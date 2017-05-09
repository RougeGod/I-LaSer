"""
The views.py program receives the requests of the user
and creates the appropriate automata/transducers to
test the decision question.
"""

from time import time
import re
import logging
import django
from django.shortcuts import render_to_response, render
from django.conf import settings

from FAdo.fio import readOneFromString, NFA, DFA

import FAdo.codes as codes
from FAdo.codes import UDCodeProp, PropertyNotSatisfied, IPTProp, DFAsymbolUnknown, \
ErrCorrectProp, regexpInvalid, infixTransducer, IATProp
from FAdo.yappy_parser import YappyError
import FAdo.fl as fl

from app.transducer.laserShared import construct_automaton, IncorrectFormat, \
     constructInAltProp, limitAutP, limitTranP, formatCounterExample

try:
    from app.transducer.ILaser_gen import gen_program
    from app.transducer.forms import UploadFileForm
except ImportError:
    pass

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250

DECIDE_REQUEST = 'decide whether the given language '
TEST_DICT = {'1': 'SATW', '2': 'MAXW', '3': 'MAXP', '4': 'MKCO'}
DESCRIBE = {'1': DECIDE_REQUEST + 'satisfies the given property. \
                    If no, return a witness; else return Nones.',
            '2': DECIDE_REQUEST+'is maximal. If no, return a witness; else return None.',
            '3': DECIDE_REQUEST+'is maximal.',
            '4': 'Construct set of words satisfying the given property.'}
FIXED_DICT = {'1': 'PREFIX', '2': 'SUFFIX', '3': 'INFIX',
              '4': 'OUTFIX', '5': 'HYPERCODE', '6': 'CODE'}

def list_to_string(list_, dict_):
    """turns a list into a string"""
    return "".join([dict_[i] for i in list_])

def long_to_base(num, base):
    """Maps num to a list of digits corresponding to base q representation of n in reverse order"""
    list_ = []
    while num > 0:
        list_.append(num % base)
        num /= base
    return list_

def make_block_code(list_length, word_length, alphabet_size):
    """Returns an NFA and a list W of up to N words of length word_length, such that the NFA
    accepts W, which satisfies the property. The alphabet to use is
    {0,1,...,s-1}. where s <= 10."""
    words = []
    list_ = dict()

    for i in range(alphabet_size):
        list_[i] = str(i)
    size = min(list_length, alphabet_size**word_length)
    for j in range(size):
        if j == 0:
            digit_list = [0]
        else:
            digit_list = long_to_base(j, alphabet_size)
        zeros = []
        for _ in range(word_length - len(digit_list)):
            zeros.append(0)
        digit_list.extend(zeros)
        word = list_to_string(digit_list, list_)
        words.append(word)
    aut = fl.FL(words).trieFA().toNFA()
    return aut, words

def upload_file(request):
    """This method handles the parsing of a file uploaded from the website."""
    form = UploadFileForm()
    try:
        if request.method == 'POST':
            if 'run_code' in request.POST:
                if request.POST['que'] == "":
                    return render(request, 'upload.html',
                                  {'error_message': 'You have to select a question \
                                  and its options to perform a request', 'form':form})
                response = get_response(request.POST, request.FILES)
            elif 'gen_code' in request.POST:
                if request.POST['que'] == "":
                    return render(request, 'upload.html',
                                  {'error_message':'You have to select a question and its options \
                                  to perform a request', 'form':form})
                response = get_code(request.POST, request.FILES)
            elif 'clear_page' in request.POST:
                return render(request, 'upload.html', {'form':form})
        else:
            response = {'form': form}

        return render(request, 'upload.html', response)
    except KeyError, k:
        return render(request, 'upload.html', {'form': form, 'error_message': k.message+"\n You \
        either have uploaded only a file or no file."})

def get_fixed_type(aut_str):
    if aut_str.count('@') > 1:
        res = re.search(r'(.+?)\n([\s\S]+)$', re.sub(r'\r', "", aut_str))
        fixed_type = res.group(1).strip(' @')

        aut_str = res.group(2)

        return aut_str, fixed_type
    return aut_str, None

def handle_satisfaction_maximality(
        property_type, question, post,
        files, form=True
    ):
    """This method handles satisfaction and maximality choices."""
    file_ = files.get('automata_file')

    if file_: # Get it from the file by default
        # automaton string
        aut_str = file_.read()

        #automaton name
        aut_name = "Language: " + file_.name

        file_.close()
    elif post.get('automata_text'):
        # automaton string
        aut_str = str(post.get('automata_text'))

        #automaton name
        aut_name = "Language: N/A"
    else:
        return {'form': form, 'error_message': 'Please provide an automaton file.'}

    aut_str, fixed_type = get_fixed_type(aut_str)

    try:
        aut = construct_automaton(aut_str)
    except (IncorrectFormat, TypeError):
        return {'form': form, 'error_message':
                'ERROR: The property file appears to be incorrectly formatted.',
                'automaton': aut_name}

    if limitAutP(aut, LIMIT_AUTOMATON):
        return {'form':form, 'error_message':
                'Size of the automaton exceeds limit! (See "Technical Notes")',
                'automaton':aut_name}
    if property_type == "1":
        t_name = ""
        if fixed_type is None:
            fixed_type = post.get('fixed_type')

        prop = create_fixed_property(aut.Sigma, fixed_type)
        if prop is None:
            prop = UDCodeProp(aut.Sigma)
            if question == '1':
                witness = prop.notSatisfiesW(aut)
                if witness == (None, None):
                    decision = "YES, the language satisfies the code property"
                    proof = ''
                else:
                    decision = "NO, the language does not satisfy the code property"
                    proof = formatCounterExample(witness)
            else:
                proof = ''
                try:
                    if prop.maximalP(aut):
                        decision = "YES, the language is a maximal code"
                    else:
                        decision = "NO, the language is not a maximal code"
                except PropertyNotSatisfied:
                    decision = "ERROR: the language doesn't satisfy the property"

            return {'form': form, 'automaton': aut_name, 'result': decision, 'proof': proof}

    # User-Input Property
    else:
        file_ = files.get('transducer_file')
        if file_ is None:
            return {'form':form, 'error_message': "Please provide a property file.",
                    'automaton':aut_name}

        t_str = file_.read()
        t_name = "Property: " + file_.name
        file_.close()

        # Input-Altering Property (given as trajectory or transducer)
        if property_type == "2":
            try:
                prop = constructInAltProp(t_str, aut.Sigma)
            except (IncorrectFormat, TypeError):
                return {'form':form, 'error_message':
                        'The property file appears to be incorrectly formatted.',
                        'automaton':aut_name, 'transducer':t_name}

        # Input-Preserving Property
        elif property_type == "3":
            try:
                prop = IPTProp(readOneFromString(t_str))
            except (YappyError, AttributeError):
                return {'form':form, 'error_message':
                        'The property file appears to be incorrectly formatted.',
                        'automaton':aut_name, 'transducer':t_name}

        # Error-Correction
        elif property_type == "4":
            try:
                prop = ErrCorrectProp(readOneFromString(t_str))
            except (YappyError, AttributeError):
                return {'form':form, 'error_message':
                        'The property file appears to be incorrectly formatted.',
                        'automaton':aut_name, 'transducer':t_name}

    if limitTranP(aut.delta, prop.Aut.delta, LIMIT):
        return {'form':form, 'error_message':
                'Sizes of the automaton and transducer exceed limit! (See "Technical Notes")',
                'automaton':aut_name, 'transducer':t_name}
    else:
        if question == "1":
            try:
                witness = prop.notSatisfiesW(aut)
            except TypeError:
                decision = "The automaton file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision,
                        'automaton':aut_name, 'transducer':t_name}

            if witness == (None, None) or witness == (None, None, None):
                decision = "YES, the language satisfies the property"
                proof = ''
            else:
                decision = "NO, the language does not satisfy the property"
                proof = formatCounterExample(witness)
            return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                    'result':decision, 'proof': proof}
        elif question == "2":
            err = ''
            try:
                witness = prop.notMaximalW(aut)
            except PropertyNotSatisfied:
                err = "ERROR: the language does not satisfy the property."
            except TypeError:
                err = "The automaton file appears to be incorrectly formatted."

            if err:
                return {'form':form, 'error_message': err,
                        'automaton':aut_name, 'transducer':t_name}

            if witness is None:
                decision = "YES, the language is maximal with respect to the property."
                proof = ''
            else:
                decision = "NO, the language is not maximal with respect to the property."
                proof = formatCounterExample(witness)

            return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                    'result':decision, 'proof': proof}

def handle_construction(
        property_type, post,
        files, form=True
    ):
    """Handle the construction choice of the website"""
    n_num = int(post.get("n_int", -1))
    s_num = int(post.get("s_int", -1))
    l_num = int(post.get("l_int", -1))

    err = ''
    if n_num <= 0 or s_num <= 0 or l_num <= 0:
        err = "Please enter three positive integers S, N, L."
    elif s_num < 2 or s_num > 10:
        err = "S must be less than 10 and greater than 1"
    elif s_num > l_num:
        err = "S must be less than L"

    if err != '':
        return {'form': form, 'error_message': err}

    if property_type == "1":
        if (n_num * l_num) > LIMIT:
            return {'form':form, 'error_message':
                    "Size of request exceeds limit! (See 'Technical Notes')"}
        try:
            _, witness = make_block_code(int(n_num), int(l_num), int(s_num))
        except DFAsymbolUnknown:
            return {'form': form, 'error_message':
                    "Something went wrong (views.py: construction, fixed property)."}
        #text_path, text_title = write_witness(witness, filename)
        words = write_witness(witness)
        result = '<div class="text-center" style="font-size: 14px; \
        color: #999999; margin-bottom: 10px;">Your Output</div>\
        <div><textarea class="text-center" rows="6" cols="50" \
        readonly>'+ words +'</textarea></div>'
        return {'form': form, 'construct_path': '',
                'construct_text': '', 'result': result}

    file_ = files.get('transducer_file')
    if not file_:
        return {'form':form, 'error_message':"Please provide a correct property file."}

    t_str = file_.read()
    t_name = "Property: " + file_.name
    file_.close()

    # Input-Altering Property (given as trajectory or transducer)
    if property_type == "2":
        result = handle_iap(n_num, l_num, s_num, t_name, t_str, form)
    # Input-Preserving Property
    elif property_type == "3":
        result = handle_ipp(n_num, l_num, s_num, t_name, t_str, form)

    return result

def handle_iap(
        n_num, l_num, s_num,
        t_name, t_str, form=True
    ):
    """Handle Input-altering properties"""
    alp = set()
    for i in range(int(s_num)):
        alp.add(str(i))

    try:
        prop = constructInAltProp(t_str, alp)
    except (IncorrectFormat, TypeError):
        return {'form': form, 'error_message':
                "The property file appears to be incorrectly formatted.",
                'transducer': t_name}

    if limitTranP({}, prop.Aut.delta, LIMIT, int(n_num)):
        return {'form':form, 'error_message':
                "Size of request exceeds limit! (See 'Technical Notes')"}

    try:
        _, witness = prop.makeCode(n_num, l_num, s_num)
    except DFAsymbolUnknown:
        return {'form': form, 'error_message':
                'The property file appears to be incorrectly formatted.',
                'transducer': t_name}

    words = write_witness(witness)
    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
    return {'form': form, 'construct_path': '',
            'construct_text': '', 'result': result}

def handle_ipp(
        n_num, l_num, s_num,
        t_name, t_str, form=True
    ):
    """Handle Input-preserving properties"""
    try:
        prop = codes.buildErrorDetectPropS(t_str)
    except (YappyError, AttributeError):
        return {'form':form, 'error_message':
                "The property file appears to be incorrectly formatted.",
                'transducer':t_name}

    if limitTranP({}, prop.Aut.delta, LIMIT, int(n_num)):
        return {'form':form, 'error_message':
                "Size of request exceeds limit! (See 'Technical Notes')"}

    try:
        _, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
    except DFAsymbolUnknown:
        return {'form': form, 'error_message':
                "The property file appears to be incorrectly formatted.",
                'transducer': t_name}

    #text_path, text_title = write_witness(witness, filename)
    words = write_witness(witness)
    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
    return {'form': form, 'witness': witness, 'prop': prop,
            'construct_path': '', 'construct_text': '', 'result': result}


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
    elif not property_type:
        return {'form': form, 'error_message': "Please select a property type."}

    if question == "1" or question == "2":
        return handle_satisfaction_maximality(property_type, question, post, files, form)
    elif question == "3":
        return handle_construction(property_type, post, files, form)

def write_witness(witness):
    """Creates the witness for a given error"""
    string = ''
    for line in witness:
        string += line + '\n'
    return string


def get_code(post, files, form=True, test_mode=None):
    """
    If a computation is too expensive to be run in due time on the server,
    the user can generate code and allow the download of that. This method
    handles that route.
    """
    if form:
        form = UploadFileForm(post, files)
    else:
        form = None

    question = post.get('que')
    property_type = post.get('prv')

    if question is None:
        return {'form': form, 'error_message': "Please select a question."}
    elif property_type is None:
        return {'form': form, 'error_message': "Please select a property type."}

    if question == '3':
        question = '4'
    elif question == '2' and property_type == '1' and post['fixed_type'] == '6':
        question = '3'

    test = TEST_DICT[question]
    prop = None
    regexp = None
    name = str(int(time()*1000))
    sigma = None
    n_num = ''
    s_num = ''
    l_num = ''

    if question == '1' or question == '2' or question == '3':
        file_ = files.get('automata_file')

        if file_: # Get it from the file by default
            aut_str = file_.read()
            file_.close()
        elif post.get('automata_text'):
            aut_str = str(post.get('automata_text'))
        else:
            return {'form': form, 'error_message': 'Please provide an automaton file.'}

        aut_str, fixed_type = get_fixed_type(aut_str)

        try:
            aut = construct_automaton(aut_str)
            #aut_str = saveToString(aut, '\n')
        except IncorrectFormat:
            decision = "ERROR: the automaton appears to be incorrectly formatted"
            return {'form': form, 'error_message': decision}
    elif question == '4':
        n_num = int(post.get("n_int", -1))
        s_num = int(post.get("s_int", -1))
        l_num = int(post.get("l_int", -1))

        if n_num <= 0 or s_num <= 0 or l_num <= 0:
            decision = "Please enter three positive integers S, N, L."
            return {'form': form, 'error_message': decision}
        elif s_num < 2 or s_num > 10:
            decision = "S must be less than 10 and greater than 1"
            return {'form': form, 'error_message': decision}
        elif s_num > l_num:
            decision = "S must be less than L"
            return {'form': form, 'error_message': decision}

    if property_type == "1":
        t_str = None
        if fixed_type is None:
            fixed_type = post['fixed_type']
            prop = FIXED_DICT[fixed_type]
        else:
            prop = fixed_type
    else:
        file_ = files.get('transducer_file')

        if not file_:
            decision = "Please provide a property file."
            return {'form':form, 'error_message': decision}

        t_str = file_.read()
        file_.close()

        # Input-Altering Property (given as trajectory or transducer)
        if property_type == "2":
            try:
                result = readOneFromString(t_str)
                if isinstance(result, NFA) or isinstance(result, DFA):
                    prop = "TRAJECT"
                    if question == '1' or question == '2' or question == '3':
                        sigma = aut.Sigma
                    elif question == '4':
                        alp = set()
                        for i in range(int(s_num)):
                            alp.add(str(i))
                        sigma = alp
                else:
                    prop = "INALT"
            except YappyError:
                try:
                    if question == '1' or question == '2' or question == '3':
                        codes.buildTrajPropS(t_str, aut.Sigma)
                    elif question == '4':
                        alp = set()
                        for i in range(int(s_num)):
                            alp.add(str(i))
                        codes.buildTrajPropS(t_str, alp)
                except regexpInvalid:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form': form, 'error_message': decision}
                prop = "TRAJECT"
                regexp = "tStr"
                if question == '1' or question == '2' or question == '3':
                    # alp = set()
                    # for i in range(int(s_num)):
                    #     alp.add(str(i))
                    # sigma = alp            ## Replace 3 lines with next
                    sigma = aut.Sigma
                elif question == '4':
                    sigma = alp

        # Input-Preserving Property
        elif property_type == "3":
            try:
                IPTProp(readOneFromString(t_str))
            except (YappyError, AttributeError):
                return {'form':form, 'error_message':
                        'The property file appears to be incorrectly formatted.'}

            prop = "INPRES"

        # Error-Correction
        elif property_type == "4":
            try:
                ErrCorrectProp(readOneFromString(t_str))
            except YappyError:
                decision = "The property file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision}
            prop = "ERRCORR"

    prog_lines = gen_program(name, prop, test, aut_str, t_str, sigma, regexp,
                            DESCRIBE[question], test_mode, s_num, l_num, n_num)

    if test_mode is not None:
        return prog_lines
    else:
        decision = "<a href='"+settings.MEDIA_URL+"%s.zip'> \
        Download your code </a></br> (See 'Technical notes')" % name
        return {'form': form, 'result': decision}


def create_fixed_property(alphabet, fixed_type):
    """
    Create a property of a fixed variety such as prefix or suffix codes
    """
    if fixed_type == "1" or fixed_type == "PREFIX":
        return codes.buildPrefixProperty(alphabet)
    elif fixed_type == "2" or fixed_type == "SUFFIX":
        return codes.buildSuffixProperty(alphabet)
    elif fixed_type == "3" or fixed_type == "INFIX":
        return IATProp(infixTransducer(alphabet))
    elif fixed_type == "4" or fixed_type == "OUTFIX":
        return codes.buildOutfixProperty(alphabet)
    elif fixed_type == "5" or fixed_type == "HYPERCODE":
        return codes.buildHypercodeProperty(alphabet)
    else:
        return None

def index(request):
    """returns the rendered index.html files"""
    return render_to_response('index.html')


def examples(request, example_type):
    """returns the various example html files"""
    return render_to_response('examples/'+example_type+'.html')
