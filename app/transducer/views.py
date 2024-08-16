"""
The views.py program receives the requests of the user
and creates the appropriate automata/transducers to
test the decision question.
"""
import re
from time import time
import django
from django.shortcuts import render
from django.conf import settings

from FAdo.fio import readOneFromString, NFA, DFA
import FAdo.codes as codes
from FAdo.codes import IPTProp, ErrCorrectProp, regexpInvalid

from app.transducer.laser_shared import construct_automaton, IncorrectFormat, construct_input_alt_prop, detect_automaton_type, construct_input_alt_prop, convertToCorrectType, is_subset, check_construction_alphabets
from app.transducer.laser_gen import gen_program
from app.transducer.forms import UploadFileForm
from app.transducer.handlers import handle_construction, handle_satisfaction_maximality, LimitExceeded
from app.transducer.util import parse_aut_str, parse_transducer_string
from app.transducer.expand_carets import expand_carets

from lark import UnexpectedCharacters

from func_timeout import func_timeout, FunctionTimedOut

TIME_LIMIT = 15 #in seconds

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250

name = str(int(time()*1000)) #the name of the ZIP file, which is the current millisecond.

DECIDE_REQUEST = 'Decide whether the given language '
#These next two dictionaries are used in the code generation but do not appear on the website.
TEST_DICT = {'1': 'SATW', '2': 'MAXW', '3': 'MKCO', '4':'AMAX'}
DESCRIBE = {'1': DECIDE_REQUEST + 'satisfies the given property. \
If no, return a witness; else return Nones.', #Satisfaction
            '2': DECIDE_REQUEST+'is maximal.',#Maximality
            '3': 'Construct set of words satisfying the given property.', #Construction
            '4': DECIDE_REQUEST + 'is epsilon-maximal.'} #Approximate Maximality
FIXED_DICT = {'1': 'PREFIX', '2': 'SUFFIX', '3': 'BIFIX', '4': 'INFIX',
              '5': 'OUTFIX', '6': 'CODE', '7': 'HYPERCODE'}

PROPERTY_INCORRECT_FORMAT = 'The property appears to be incorrectly formatted.'

TRANSDUCER_TYPES = {
    'InputAltering': '2',
    'ErrorDetecting': '3',
    'ErrorCorrecting': '4',
}


def upload_file(request):
    """This method handles the parsing of a file uploaded from the website."""
    post = request.POST
    files = request.FILES

    if request.method == 'POST': # POST Request, time to do some calculations
        form = UploadFileForm(post, files)

        if 'clear_page' in post: # ...Unless we are clearing the page
            response = {'form': UploadFileForm()}
        elif not form.is_valid():
            response = {'form': form}
        elif 'run_code' in post: # This will handle server-side calculation
            try:
                response = get_response(form.cleaned_data, files, form)
            except Exception as unforeseen:
                response = {"form": form, "error_message": "Unexpected Error: " + unforeseen}
        elif 'gen_code' in post: # This will handle generation of code for client-side calculation
            try:
                response = get_code(form.cleaned_data, files, form)
            except Exception as unforeseen:
                response = {"form": form, "error_message": "Unexpected Error Generating Code: " + unforeseen}
    else: # GET Request, just render the page
        response = {'form': UploadFileForm()}

    return render(request, 'upload.html', response)

def get_response(data, files, form):
    """
    This handles lighter tasks that can be safely computed on the server.
    It gives the response to the user via the webpage
    """
    if not form: # Test mode
        form = UploadFileForm(data, files)
        form.is_valid()
        data = form.cleaned_data

    question = data.get('question')
    property_type = data.get('property_type')

    if not question: #User clicked submit without specifying question (question is 0, so not question is true)
        return {'form': form, 'error_message': "Please select a question."}
    if not property_type:
        return {"form": form, "error_message": "Please select a property type."}

    if question in ['1', '2', '4']:
        try:
            return func_timeout(TIME_LIMIT, handle_satisfaction_maximality, args=(property_type, question, data, files, form))
        except FunctionTimedOut:
            return get_code(data, files, form=form, sentFrom="Timeout")
        except LimitExceeded:
            return get_code(data, files, form=form, sentFrom="Limit")
    elif question == '3':
        try:
            return func_timeout(TIME_LIMIT, handle_construction, args=(property_type, data, files, form))
        except FunctionTimedOut:
            return get_code(data, files, form=form, sentFrom="Timeout")
        except LimitExceeded:
            return get_code(data, files, form=form, sentFrom="Limit")

def get_code(data, files, form=True, test_mode=None, sentFrom=None):
    """
    If a computation is too expensive to be run in due time on the server,
    the user can generate code and allow the download of that. This method
    handles that route.
    """
    if not form: # Test Mode
        form = UploadFileForm(data, files)
        form.is_valid()
        data = form.cleaned_data

    def error(err):
        """Formats an error using the given string"""
        return {'form': form, 'error_message': err}

    question = data.get('question')
    property_type = data.get('property_type')
    if not question:
        return error('Please select a question.')
    elif property_type == '0':
        return error("Please select a property type.")

    prop = regexp = fixed_type = sigma = aut_type = None
    name = str(int(time()*1000)) #the name of the ZIP file, which is the current millisecond.
    n_num = s_num = l_num = 0
    aut_str = t_str = ''
    transducer = fixed_type = transducer_type = trajectory = None

    DEFAULT_EPSI = 0.01
    DEFAULT_DIRIC = 2.001
    DEFAULT_DISP = 1
    epsi = convertToCorrectType(data.get("epsilon"), DEFAULT_EPSI)
    dirichletT = convertToCorrectType(data.get("dirichletT"), DEFAULT_EPSI)
    displacement = convertToCorrectType(data.get("displacement"), DEFAULT_DISP, desiredType=int)

    # Automaton String, or number generation
    if question in ['1', '2', '4']: # Satisfaction, maximality, approx-maximality
        aut_str = data.get('automata_text')

        if not aut_str:
            return error('Please provide an automaton file.')

        aut_str = parse_aut_str(aut_str)

        try:
            aut_type = detect_automaton_type(aut_str)
            if (aut_type == "str2regexp"):
                try:
                    aut_str = expand_carets(aut_str)
                except ValueError as err:
                    return error(str(err))
            aut = construct_automaton(aut_str)
        except IncorrectFormat:
            return {'form': form, 'error_message':
                    'The automaton appears to be incorrectly formatted'}
    elif question == '3': # Construction
        n_num = data.get('n_int', -1)
        s_num = data.get('s_int', -1)
        l_num = data.get('l_int', -1)

        if n_num <= 0 or s_num <= 0 or l_num <= 0:
            return error('Please enter three positive integers S, N, L.')
        elif s_num < 2 or s_num > 10:
            return error('S must be less than 10 and greater than 1')
    if not property_type:
        return error('Please provide a property type.')
    # Get Fixed Type, or get Transducer String
    if property_type == "1":
        t_str = None
        fixed_type = data.get('fixed_type')
        if fixed_type is None:
            return error("Please select a fixed type.")
        prop = FIXED_DICT[str(fixed_type)]
    else:
        if not data.get("transducer_text"):
            return error('Please provide a property.')
        t_str = parse_transducer_string(data.get('transducer_text'))["t_str"]

    theta = None
    if property_type == '2':  # Input-Altering Property (given as trajectory or transducer)
        if question in ['1', '2', '4']:
            try:
                sigma = aut.Sigma
            except AttributeError:
                if type(aut) == list:
                    return error("Only one automaton may be inputted at a time.")
                else:
                    return error("The automaton appears to be incorrectly formatted.")
        elif question == '3':
            sigma = set()
            for i in range(s_num):
                sigma.add(str(i))
        try:
            result = construct_input_alt_prop(t_str, sigma)
            prop = construct_input_alt_prop(t_str, sigma, True)
            if (prop == "TRAJECT"):
                try:
                    prop = expand_carets(prop)
                except ValueError as err:
                    return error(str(err))
            try:
                if not is_subset(aut, result):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except UnboundLocalError: #there is no automaton (construction Question), so checking it is nonsensical
                err = check_construction_alphabets(s_num, result.Aut.Sigma)
                if err is not None:
                    return error(err)
        except IncorrectFormat:
            return error(PROPERTY_INCORRECT_FORMAT)

    # Input-Preserving Property
    elif property_type == '3':
        try:
            prop = IPTProp(readOneFromString(t_str + "\n")) # Input Preserving Transducer Property
            try:
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except UnboundLocalError:
                err = check_construction_alphabets(s_num, prop.Aut.Sigma)
                if err is not None:
                    return error(err)
        except AttributeError:
            return error(PROPERTY_INCORRECT_FORMAT)

        prop = 'INPRES' # Input Preserving

    # Error-Correction
    elif property_type == '4':
        try:
            prop = ErrCorrectProp(readOneFromString(t_str + "\n"))
            if not is_subset(aut, prop):
                return error("The automaton's alphabet should be a subset of the transducer's")
        except AttributeError:
            return error(PROPERTY_INCORRECT_FORMAT)
        prop = 'ERRCORR'

    elif property_type == '5': #Theta-transducer property
        sigma = aut.Sigma
        theta = data.get('theta_text')

        try:
            IPTProp(readOneFromString(t_str + "\n"))
            prop = 'INPRES'
        except (AttributeError, UnexpectedCharacters):
            try:
                prop = construct_input_alt_prop(t_str, aut.Sigma, True)
            except (IncorrectFormat, TypeError):
                return error(PROPERTY_INCORRECT_FORMAT)
            if not is_subset(aut, prop):
                return error("The automaton's alphabet should be a subset of the transducer's")

    description = DESCRIBE[question]
    test = TEST_DICT[question]

    if property_type == '5':
        test = 'NONEMPTYW'

    if question == '2' and property_type == '1' and fixed_type == '6':
        # This is a special case - code does not return a witness
        description = DECIDE_REQUEST + 'is maximal.'
        test = 'MAXP'

    prog_lines = gen_program(name, prop, test, aut_str, aut_type, t_str, sigma, regexp,
                             description, test_mode, s_num, l_num, n_num, theta, dirichletT, epsi, displacement)

    if test_mode is not None:
        return prog_lines

    url_params = (settings.MEDIA_URL, name)
    if sentFrom == "Timeout":
        decision = "The computation took too long!<br>Would you like to <a href=%s%s.zip>download your code</a>?<br>" % url_params
    elif sentFrom == "Limit":
        decision = "This query is too complex for the web server. <br>Would you like to <a href=%s%s.zip>download your code</a>?<br>" % url_params
        # The code has now been placed in the media folder, to download.
    else:
        decision = '<a href="%s%s.zip"> Download your code </a></br> (See "Technical notes")' % url_params
    return {'form': form, 'result': decision}

def index(request):
    """renders index.html"""
    return render(request, 'index.html')


def examples(request, example_type):
    """Returns the various examples"""
    return render(request, 'examples/'+example_type+'.html')

