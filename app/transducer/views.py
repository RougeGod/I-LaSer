"""
The views.py program receives the requests of the user
and creates the appropriate automata/transducers to
test the decision question.
"""
import re
from time import time
import django
from django.shortcuts import render_to_response, render
from django.conf import settings

from FAdo.fio import readOneFromString, NFA, DFA

import FAdo.codes as codes
from FAdo.codes import IPTProp, ErrCorrectProp, regexpInvalid
from FAdo.yappy_parser import YappyError

from app.transducer.laser_shared import construct_automaton, IncorrectFormat

from app.transducer.ILaser_gen import gen_program
from app.transducer.forms import UploadFileForm
from app.transducer.handlers import handle_construction, handle_satisfaction_maximality
from app.transducer.util import parse_aut_str

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250

DECIDE_REQUEST = 'Decide whether the given language '
TEST_DICT = {'1': 'SATW', '2': 'MAXW', '3': 'MKCO'}
DESCRIBE = {'1': DECIDE_REQUEST + 'satisfies the given property. \
                    If no, return a witness; else return Nones.',#Satisfaction
            '2': DECIDE_REQUEST+'is maximal. If no, return a witness; else return None.',#Maximality
            '3': 'Construct set of words satisfying the given property.'}#Construction
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
    form = UploadFileForm()
    post = request.POST
    files = request.FILES

    if request.method == 'POST': # POST Request, time to do some calculations
        if 'clear_page' in post: # ...Unless we are clearing the page
            response = {'form': form}
        elif not post.get('que'):
            response = {'form':form, 'error_message':
                        'You have to select a question and its options to perform a request'}
        elif 'run_code' in post: # This will handle server-side calculation
            response = get_response(post, files)
        elif 'gen_code' in post: # This will handle generation of code for client-side calculation
            response = get_code(post, files)
    else: # GET Request, just render the page
        response = {'form': form}

    return render(request, 'upload.html', response)

def get_response(post, files, form=True):
    """
    This handles lighter tasks that can be safely computed on the server.
    It gives the response to the user via the webpage
    """
    form = UploadFileForm(post, files) if form else None

    question = post.get('que')
    property_type = post.get('prv')

    if not question:
        return {'form': form, 'error_message': "Please select a question."}
    # elif not property_type:
    #     return {'form': form, 'error_message': "Please select a property type."}

    if question in ['1', '2']:
        return handle_satisfaction_maximality(property_type, question, post, files, form)
    elif question == '3':
        return handle_construction(property_type, post, files, form)

def get_code(post, files, form=True, test_mode=None):
    """
    If a computation is too expensive to be run in due time on the server,
    the user can generate code and allow the download of that. This method
    handles that route.
    """

    form = UploadFileForm(post, files) if form else None

    def error(err):
        """Formats an error using the given string"""
        return {'form': form, 'error_message': err}

    question = post.get('que')
    property_type = post.get('prv')
    if question is None:
        return error("Please select a question.")
    elif property_type is None:
        return error("Please select a property type.")

    prop = None
    regexp = None
    fixed_type = None
    name = str(int(time()*1000))
    sigma = None
    n_num = ''
    s_num = ''
    l_num = ''
    t_str = ''
    aut_str = ''

    # Automaton String, or number generation
    if question in ['1', '2']: # Satisfaction, maximality
        file_ = files.get('automata_file')

        if file_: # Get it from the file by default
            aut_str = file_.read()
            file_.close()
        elif post.get('automata_text'): # Else the text box
            aut_str = str(post.get('automata_text'))
        else:
            return error('Please provide an automaton file.')

        parsed = parse_aut_str(aut_str)

        aut_str = parsed['aut_str']
        fixed_type = parsed['fixed_type']
        transducer = parsed['transducer']
        transducer_type = parsed['transducer_type']
        trajectory = parsed['trajectory']

        if fixed_type and not property_type:
            property_type = "1"

        try:
            aut = construct_automaton(aut_str)
        except IncorrectFormat:
            return {'form': form, 'error_message':
                    'The automaton appears to be incorrectly formatted'}
    elif question == '3': # Construction
        n_num = int(post.get("n_int", -1))
        s_num = int(post.get("s_int", -1))
        l_num = int(post.get("l_int", -1))

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
            fixed_type = post.get('fixed_type')
            prop = FIXED_DICT[fixed_type]
        else:
            prop = fixed_type
    else:
        file_ = files.get('transducer_file')

        if file_: # Get it from the file by default
            # transducer string
            t_str = file_.read()

            file_.close()
        elif post.get('transducer_text1'):
            # transducer string
            t_str = str(post.get('transducer_text1'))
        elif post.get('transducer_text2'):
            # transducer string
            t_str = str(post.get('transducer_text2'))
        elif transducer:
            t_str = re.sub(r'\r', '', transducer)

            t_name = "Property: N/A"

            if transducer_type:
                property_type = TRANSDUCER_TYPES[transducer_type]
        elif trajectory:
            t_str = re.sub(r'\r', '', trajectory)

            t_name = "Property: N/A"

            property_type = "2"
        else:
            return error('Please provide a property file.')

    # Input-Altering Property (given as trajectory or transducer)
    if not property_type:
        return error('Please provide a property type.')
    elif property_type == "2":
        if question in ['1', '2']:
            sigma = aut.Sigma
        elif question == '3':
            sigma = set()
            for i in range(int(s_num)):
                sigma.add(str(i))

        try:
            result = readOneFromString(t_str.strip()+'\n')
            if isinstance(result, (DFA, NFA)):
                prop = 'TRAJECT' # Trajectory
            else:
                sigma = None
                prop = 'INALT' # Transducer
        except YappyError:
            try:
                codes.buildTrajPropS(t_str, sigma)
            except regexpInvalid:
                return {'form': form, 'error_message':PROPERTY_INCORRECT_FORMAT}
            prop = 'TRAJECT' # Also Trajectory
            regexp = 'tStr'

    # Input-Preserving Property
    elif property_type == "3":
        try:
            IPTProp(readOneFromString(t_str)) # Input Preserving Transducer Property
        except (YappyError, AttributeError):
            return error(PROPERTY_INCORRECT_FORMAT)

        prop = "INPRES" # Input Preserving

    # Error-Correction
    elif property_type == "4":
        try:
            ErrCorrectProp(readOneFromString(t_str))
        except YappyError:
            return error(PROPERTY_INCORRECT_FORMAT)
        prop = "ERRCORR"

    description = DESCRIBE[question]
    test = TEST_DICT[question]
    if question == '2' and property_type == '1' and fixed_type == '6':
        # This is a special case - code does not return a witness
        description = DECIDE_REQUEST+'is maximal.'
        test = 'MAXP'


    prog_lines = gen_program(name, prop, test, aut_str, t_str, sigma, regexp,
                             description, test_mode, s_num, l_num, n_num)

    if test_mode is not None:
        return prog_lines
    else:
        decision = '<a href="%s%s.zip"> Download your code </a></br> (See "Technical notes")'\
             % (settings.MEDIA_URL, name)
        return {'form': form, 'result': decision}

def index(_):
    """returns the rendered index.html files"""
    return render_to_response('index.html')

def examples(_, example_type):
    """returns the various example html files"""
    return render_to_response('examples/'+example_type+'.html')
