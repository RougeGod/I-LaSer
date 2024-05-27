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

from app.transducer.laser_shared import construct_automaton, IncorrectFormat, construct_input_alt_prop, detect_automaton_type, construct_input_alt_prop, convertToCorrectType
from app.transducer.laser_gen import gen_program
from app.transducer.forms import UploadFileForm
from app.transducer.handlers import handle_construction, handle_satisfaction_maximality#, handle_approx_maximality
from app.transducer.util import parse_aut_str

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250

DECIDE_REQUEST = 'Decide whether the given language '
#These next two dictionaries are used in the code generation but do not appear on the website. 
TEST_DICT = {'1': 'SATW', '2': 'MAXW', '3': 'MKCO', '4':'AMAX'}
DESCRIBE = {'1': DECIDE_REQUEST + 'satisfies the given property. \
If no, return a witness; else return Nones.', #Satisfaction
            '2': DECIDE_REQUEST+'is maximal.',#Maximality
            '3': 'Construct set of words satisfying the given property.', #Construction
            '4': DECIDE_REQUEST + 'is epsilon-maximal.'} #Approximate Maximality
FIXED_DICT = {'1': 'PREFIX', '2': 'SUFFIX', '3': 'INFIX',
              '4': 'OUTFIX', '5': 'HYPERCODE', '6': 'CODE'}

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
            response = get_response(form.cleaned_data, files, form)
        elif 'gen_code' in post: # This will handle generation of code for client-side calculation
            response = get_code(form.cleaned_data, files, form)
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

    if not question: #User clicked submit without specifying question
        return {'form': form, 'error_message': "Please select a question."}
    #if (property_type == '0'): #no property type was entered (entering property type is unnecessary as automaton text area may contain a property description in the form of a transducer)
    #     return {'form': form, 'error_message': "Please select a property type."}

    if question in ['1', '2', '4']:
        return handle_satisfaction_maximality(property_type, question, data, files, form)
    elif question == '3':
        return handle_construction(property_type, data, files, form)

def get_code(data, files, form=True, test_mode=None):
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

        parsed = parse_aut_str(aut_str)

        aut_str = parsed.get('aut_str')
        fixed_type = parsed.get('fixed_type')
        transducer = parsed.get('transducer')
        transducer_type = parsed.get('transducer_type')
        trajectory = parsed.get('trajectory')
              
        if fixed_type and not property_type: #if we somehow have a fixed property type set without a property type set, assume property type is "fixed"
            property_type = '1'

        try:
            aut_type = detect_automaton_type(aut_str)
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
        elif s_num > l_num:
            return error('S must be less than L')
    
    # Get Fixed Type, or get Transducer String
    if property_type == "1":
        t_str = None
        if fixed_type is None:
            fixed_type = data.get('fixed_type')
            prop = FIXED_DICT[fixed_type]
        else:
            prop = fixed_type
    else:
        t_str = re.sub(r'\r', '', data.get('transducer_text'))

        if transducer:
            t_str = re.sub(r'\r', '', transducer)

            if transducer_type:
                property_type = TRANSDUCER_TYPES[transducer_type]

        elif trajectory:
            t_str = re.sub(r'\r', '', trajectory)

            property_type = '2'

        if not t_str:
            return error('Please provide a property file.')
        else:
            t_str = t_str.strip()

    theta = None

    # Input-Altering Property (given as trajectory or transducer)
    if not property_type:
        return error('Please provide a property type.')
    elif property_type == '2':
        if question in ['1', '2', '4']:
            sigma = aut.Sigma
        elif question == '3':
            sigma = set()
            for i in range(s_num):
                sigma.add(str(i))

        try:
            result = construct_input_alt_prop(t_str, sigma)
            prop = construct_input_alt_prop(t_str, sigma, True)
        except IncorrectFormat:
            return error(PROPERTY_INCORRECT_FORMAT)

    # Input-Preserving Property
    elif property_type == '3':
        try:
            IPTProp(readOneFromString(t_str + "\n")) # Input Preserving Transducer Property
        except AttributeError:
            return error(PROPERTY_INCORRECT_FORMAT)

        prop = 'INPRES' # Input Preserving

    # Error-Correction
    elif property_type == '4':
        try:
            ErrCorrectProp(readOneFromString(t_str + "\n"))
        except AttributeError:
            return error(PROPERTY_INCORRECT_FORMAT)
        prop = 'ERRCORR'

    elif property_type == '5': #Theta-transducer property
        sigma = aut.Sigma
        theta = data.get('theta_text')

        try:
            IPTProp(readOneFromString(t_str + "\n"))
            prop = 'INPRES'
        except AttributeError:
            try:
                prop = construct_input_alt_prop(t_str, aut.Sigma, True)
            except (IncorrectFormat, TypeError):
                return error(PROPERTY_INCORRECT_FORMAT)

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

    # The code has now been placed in the media folder, to download.
    decision = '<a href="%s%s.zip"> Download your code </a></br> (See "Technical notes")'\
         % (settings.MEDIA_URL, name)
    return {'form': form, 'result': decision}

def index(request):
    """renders index.html"""
    return render(request, 'index.html')


def examples(request, example_type):
    """Returns the various examples"""
    return render(request, 'examples/'+example_type+'.html')
