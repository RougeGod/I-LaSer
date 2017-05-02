"""
The views.py program receives the requests of the user
and creates the appropriate automata/transducers to
test the decision question.
"""

from time import time
import django
from django.shortcuts import render_to_response, render
from django.conf import settings

from FAdo.fio import readOneFromString, NFA, DFA

import FAdo.codes as codes
from FAdo.codes import UDCodeProp, PropertyNotSatisfied, IPTProp, DFAsymbolUnknown, \
ErrCorrectProp, regexpInvalid, infixTransducer, IATProp
from FAdo.yappy_parser import YappyError

from app.transducer.laserShared import constructAutomaton, IncorrectFormat, \
     constructInAltProp, limitAutP, limitTranP, formatCounterExample

try:
    from app.transducer.ILaser_gen import genProgram
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

def get_response(post, files, form = True):
    """This does something with the response?"""
    if form:
        form = UploadFileForm(post, files)
    else:
        form = None

    try:
        question = post['que']
    except:
        decision = "Please select a question."
        return {'form': form, 'error_message': decision}

    try:
        property_type = post['prv']
    except:
        decision = "Please select a property type."
        return {'form': form, 'error_message': decision}

    if question == "1" or question == "2":
        try:
            #automaton string
            aut_str = files['automata_file'].read()

            #automaton name
            aut_name = "Language: " + files['automata_file'].name
            files['automata_file'].close()
        except:
            decision = "Please provide an automaton file."
            return {'form': form, 'error_message': decision}

        try:
            #print aut_str
            aut = constructAutomaton(aut_str)
        except IncorrectFormat:
            decision = "ERROR: the automaton appears to be incorrectly formatted"
            return {'form': form, 'error_message': decision, 'automaton': aut_name}
        except TypeError:
            decision = "The property file appears to be incorrectly formatted."
            return {'form':form, 'error_message': decision, 'automaton':aut_name}

        if limitAutP(aut, LIMIT_AUTOMATON):
            decision = "Size of the automaton exceeds limit! (See \"Technical Notes\")"
            return {'form':form, 'error_message': decision, 'automaton':aut_name}

        # Fixed Property
        if property_type == "1":
            t_name = ""
            fixed_type = post['fixed_type']
            if 0 < int(fixed_type) < 6:
                prop = create_fixed_property(aut.Sigma, fixed_type)
            else:
                p_name = "code"
                proof = ''
                prop = UDCodeProp(aut.Sigma)
                if question == '2':
                    try:
                        if prop.maximalP(aut):
                            decision = "YES, the language is a maximal " + p_name
                            proof = ""
                        else:
                            decision = "NO, the language is not a maximal " + p_name
                    except PropertyNotSatisfied:
                        decision = "ERROR: the language doesn't satisfy the property"
                        proof = ""
                else:
                    witness = prop.notSatisfiesW(aut)
                    if witness == (None, None):
                        decision = "YES, the language satisfies the " + p_name + " property"
                    else:
                        decision = "NO, the language does not satisfy the " + p_name + " property"
                        proof = formatCounterExample(witness)

                return {'form': form, 'automaton': aut_name, 'result': decision, 'proof': proof}

        # User-Input Property
        else:
            try:
                t_str = files['transducer_file'].read()
                t_name = "Property: " + files['transducer_file'].name
                files['transducer_file'].close()
            except:
                decision = "Please provide a property file."
                return {'form':form, 'error_message': decision, 'automaton':aut_name}

            # Input-Altering Property (given as trajectory or transducer)
            if property_type == "2":
                try:
                    prop = constructInAltProp(t_str, aut.Sigma)
                except IncorrectFormat:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}
                except TypeError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}

            # Input-Preserving Property
            elif property_type == "3":
                try:
                    prop = IPTProp(readOneFromString(t_str))
                except YappyError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}
                except AttributeError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}

            # Error-Correction
            elif property_type == "4":
                try:
                    prop = ErrCorrectProp(readOneFromString(t_str))
                except YappyError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}
                except AttributeError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}

        if limitTranP(aut.delta, prop.Aut.delta, LIMIT):
            decision = "Sizes of the automaton and transducer exceed limit! (See 'Technical Notes')"
            return {'form':form, 'error_message': decision,
                    'automaton':aut_name, 'transducer':t_name}
        else:
            proof = ""
            if question == "1":
                try:
                    witness = prop.notSatisfiesW(aut)
                except TypeError:
                    decision = "The automaton file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}

                if witness == (None, None) or witness == (None, None, None):
                    decision = "YES, the language satisfies the property"
                    proof = ""
                else:
                    decision = "NO, the language does not satisfy the property"
                    proof = formatCounterExample(witness)
                return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                        'result':decision, 'proof': proof}
            elif question == "2":
                try:
                    witness = prop.notMaximalW(aut)
                except PropertyNotSatisfied:
                    decision = "ERROR: the language does not satisfy the property."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}
                except TypeError:
                    decision = "The automaton file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision,
                            'automaton':aut_name, 'transducer':t_name}

                if witness is None:
                    decision = "YES, the language is maximal with respect to the property."
                else:
                    decision = "NO, the language is not maximal with respect to the property."
                    proof = formatCounterExample(witness)

                return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                        'result':decision, 'proof': proof}
    elif question == "3":
        n_num = post["n_int"]
        s_num = post["s_int"]
        l_num = post["l_int"]

        if n_num == "" or s_num == "" or l_num == "":
            decision = "Please enter three positive integers S, N, L."
            return {'form': form, 'error_message': decision}
        elif int(s_num) < 2  or int(s_num) > 10:
            decision = "S must be less than 10 and greater than 1"
            return {'form': form, 'error_message': decision}
        elif int(s_num) > int(l_num):
            decision = "S must be less than L"
            return {'form': form, 'error_message': decision}
        else:
            decision = ''
            witness = ''
            alp = set()
            for i in range(int(s_num)):
                alp.add(str(i))

            if property_type == "1":
                if (int(n_num)*int(l_num)) > LIMIT:
                    decision = "Size of request exceeds limit! (See \"Technical Notes\")"
                    return {'form':form, 'error_message': decision}
                # try:
                    # a, witness = makeBlockCode(int(n_num), int(l_num), int(s_num))
                # except DFAsymbolUnknown:
                decision = "Something went wrong (views.py: construction, fixed property)."
                return {'form': form, 'error_message': decision}
                # filename = str(int(time() * 1000))
                # #text_path, text_title = write_witness(witness, filename)
                # words = write_witness(witness, filename)
                # result = '<div class="text-center" style="font-size: 14px; \
                # color: #999999; margin-bottom: 10px;">\Your Output</div>\
                # <div><textarea class="text-center" rows="6" cols="50" \
                # readonly>'+ words +'</textarea></div>'
                # return {'form': form, 'construct_path': '',
                #         'construct_text': '', 'result': result}

            else:
                try:
                    t_str = files['transducer_file'].read()
                    t_name = "Property: " + files['transducer_file'].name
                    files['transducer_file'].close()
                    #print '\n-----------> ', len(t_str), '   line 256 of views.py'
                except:
                    decision = "Please provide a correct property file."
                    return {'form': form, 'error_message': decision}

                # Input-Altering Property (given as trajectory or transducer)
                if property_type == "2":
                    try:
                        prop = constructInAltProp(t_str, alp)
                    except IncorrectFormat:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': t_name}
                    except TypeError:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form':form, 'error_message': decision,
                                'automaton':aut_name, 'transducer':t_name}

                    if limitTranP({}, prop.Aut.delta, LIMIT, int(n_num)):
                        decision = "Size of request exceeds limit! (See \"Technical Notes\")"
                        return {'form':form, 'error_message': decision}

                    try:
                        aut, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
                    except DFAsymbolUnknown:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': t_name}

                    filename = str(int(time()*1000))
                    #text_path, text_title = write_witness(witness, filename)
                    words = write_witness(witness, filename)
                    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
                    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
                    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
                    return {'form': form, 'construct_path': '',
                            'construct_text': '', 'result': result}

                # Input-Preserving Property
                elif property_type == "3":
                    try:
                        #prop = codes.ErrDetectProp(readOneFromString(t_str))
                        prop = codes.buildErrorDetectPropS(t_str)
                    except YappyError:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': t_name}
                    except AttributeError:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form':form, 'error_message': decision,
                                'automaton':aut_name, 'transducer':t_name}

                    if limitTranP({}, prop.Aut.delta, LIMIT, int(n_num)):
                        decision = "Size of request exceeds limit! (See \"Technical Notes\")"
                        return {'form':form, 'error_message': decision}

                    try:
                        aut, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
                    except DFAsymbolUnknown:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': t_name}

                    filename = str(int(time() * 1000))
                    #text_path, text_title = write_witness(witness, filename)
                    words = write_witness(witness, filename)
                    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
                    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
                    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
                    return {'form': form, 'witness': witness, 'prop': prop,
                            'construct_path': '', 'construct_text': '', 'result': result}

def write_witness(witness, filename):
    '''
    if not os.path.exists('media/' + filename):
        os.mkdir('media/' + filename)
    textfile = open('media/' + filename + "/construct.txt", 'w')
    for w in witness:
        textfile.write(w+'\n')
    textfile.close()
    text_path = '/' + filename + "/construct.txt"
    text_title = 'Download your text file'
    return text_path, text_title
    '''
    string = ''
    for line in witness:
        string += line + '\n'
    return string


def get_code(post, files, form=True, testMode=None):

    if form:
        form = UploadFileForm(post, files)
    else:
        form = None

    try:
        question = post['que']
    except:
        decision = "Please select a question."
        return {'form': form, 'error_message': decision}

    try:
        property_type = post['prv']
    except:
        decision = "Please select a property type."
        return {'form': form, 'error_message': decision}
    if question == '3':
        question = '4'
    if question == '2' and property_type == '1' and post['fixed_type'] == '6':
        question = '3'

    test = TEST_DICT[question]
    prop = None
    regexp = None
    name = str(int(time()*1000))
    n_num = ""
    s_num = ""
    l_num = ""
    aut_str = ""
    sigma = None
    if question == '1' or question == '2' or question == '3':
        try:
            aut_str = files['automata_file'].read()
            files['automata_file'].close()
        except:
            decision = "Please provide an automaton file."
            return {'form': form, 'error_message': decision}

        try:
            aut = constructAutomaton(aut_str)
            #aut_str = saveToString(aut, '\n')
        except IncorrectFormat:
            decision = "ERROR: the automaton appears to be incorrectly formatted"
            return {'form': form, 'error_message': decision}
    elif question == '4':
        n_num = post["n_int"]
        s_num = post["s_int"]
        l_num = post["l_int"]
        if n_num == "" or s_num == "" or l_num == "":
            decision = "Please enter three positive integers S, N, L."
            return {'form': form, 'error_message': decision}
        elif int(s_num) < 2  or int(s_num) > 10:
            decision = "S must be less than 10 and greater than 1"
            return {'form': form, 'error_message': decision}
        elif int(s_num) > int(l_num):
            decision = "S must be less than L"
            return {'form': form, 'error_message': decision}

    # Fixed Property
    if property_type == "1":
        t_str = None
        fixed_type = post['fixed_type']
        prop = FIXED_DICT[fixed_type]
    else:
        try:
            t_str = files['transducer_file'].read()
            files['transducer_file'].close()
        except:
            decision = "Please provide a property file."
            return {'form':form, 'error_message': decision}

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
            except:
                decision = "The property file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision}

            prop = "INPRES"

        # Error-Correction
        elif property_type == "4":
            try:
                ErrCorrectProp(readOneFromString(t_str))
            except YappyError:
                decision = "The property file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision}
            prop = "ERRCORR"

    prog_lines = genProgram(name, prop, test, aut_str, t_str, sigma, regexp,
                            DESCRIBE[question], testMode, s_num, l_num, n_num)

    if testMode is not None:
        return prog_lines
    else:
        decision = "<a href='"+settings.MEDIA_URL+"%s.zip'> \
        Download your code </a></br> (See 'Technical notes')" % name
        return {'form': form, 'result': decision}


def create_fixed_property(alphabet, n):
    """
    """
    if n == "1":
        return codes.buildPrefixProperty(alphabet)
    elif n == "2":
        return codes.buildSuffixProperty(alphabet)
    elif n == "3":
        tran = infixTransducer(alphabet)
        return IATProp(tran)
    elif n == "4":
        return codes.buildOutfixProperty(alphabet)
    elif n == "5":
        return codes.buildHypercodeProperty(alphabet)


def index(request):
    """returns the rendered index.html files"""
    return render_to_response('index.html')


def examples(request, example_type):
    """returns the various example html files"""
    return render_to_response('examples/'+example_type+'.html')
