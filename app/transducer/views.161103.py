
try:
    from forms import UploadFileForm
    from django.shortcuts import render_to_response
    from django.shortcuts import render
except:
    pass

import django
import os

from django.conf import settings

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250


from FAdo.fio import readOneFromString
from FAdo.fa import *
import FAdo.codes as codes
import FAdo.fl as fl
from FAdo.codes import *
import FAdo.fio as fio
from FAdo.yappy_parser import YappyError
from time import time
try:
    from ILaser_gen import genProgram
except:
    pass

from laserShared import constructAutomaton, IncorrectFormat, \
     constructInAltProp, limitAutP, limitTranP, formatCounterExample

"""
The views.py program receives the requests of the user
and creates the appropriate automata/transducers to
test the decision question.
"""


def upload_file(request):
    form = UploadFileForm()
    try:
        if request.method == 'POST':
            if 'run_code' in request.POST:
                if request.POST['que'] == "":
                    return render(request, 'upload.html',{'error_message':'You have to select a question and its options to perform a request', 'form':form})
                response = getResponse(request.POST, request.FILES)
            elif 'gen_code' in request.POST:
                if request.POST['que'] == "":
                    return render(request, 'upload.html',{'error_message':'You have to select a question and its options to perform a request', 'form':form})
                response = getCode(request.POST, request.FILES)
            elif 'clear_page' in request.POST:
                return render(request, 'upload.html',{'form':form})
        else:
            response = {'form': form}

        return render(request,'upload.html', response)
    except KeyError, k:
        return render(request, 'upload.html', {'form': form,'error_message': k.message+"\n You either have uploaded only a file or no file."})


def getResponse(post, files, form = True):
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
            autStr = files['automata_file'].read()
        except:
            decision = "Please provide an automaton file."
            return {'form': form, 'error_message': decision}

        autName = "Language: " + files['automata_file'].name

        try:
            #print autStr
            aut = constructAutomaton(autStr)
        except IncorrectFormat:
            decision = "ERROR: the automaton appears to be incorrectly formatted"
            return {'form': form, 'error_message': decision, 'automaton': autName}
        except TypeError:
            decision = "The property file appears to be incorrectly formatted."
            return {'form':form, 'error_message': decision, 'automaton':autName}

        if limitAutP(aut, LIMIT_AUTOMATON):
            decision = "Size of the automaton exceeds limit! (See \"Technical Notes\")"
            return {'form':form, 'error_message': decision, 'automaton':autName}

        # Fixed Property
        if property_type == "1":
            tName = ""
            fixed_type = post['fixed_type']
            if 0 < int(fixed_type) < 6:
                prop = createFixedProperty(aut.Sigma, fixed_type)
            else:
                pName = "code"
                proof = ''
                prop = UDCodeProp(aut.Sigma)
                if question == '2':
                    try:
                        if prop.maximalP(aut):
                            decision = "YES, the language is a maximal " + pName
                            proof = ""
                        else:
                            decision = "NO, the language is not a maximal " + pName
                    except PropertyNotSatisfied:
                        decision = "ERROR: the language doesn't satisfy the property"
                        proof = ""
                else:
                    witness = prop.notSatisfiesW(aut)
                    if witness == (None, None):
                        decision = "YES, the language satisfies the " + pName + " property"
                    else:
                        decision = "NO, the language does not satisfy the " + pName + " property"
                        proof = formatCounterExample(witness)

                return {'form': form, 'automaton': autName, 'result': decision, 'proof': proof}

        # User-Input Property
        else:
            try:
                tStr = files['transducer_file'].read()
            except Exception:
                decision = "Please provide a property file."
                return {'form':form, 'error_message': decision, 'automaton':autName}

            tName = "Property: " + files['transducer_file'].name
            # Input-Altering Property (given as trajectory or transducer)
            if property_type == "2":
                try:
                    prop = constructInAltProp(tStr, aut.Sigma)
                except IncorrectFormat:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}
                except TypeError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

            # Input-Preserving Property
            elif property_type == "3":
                try:
                    prop = IPTProp(readOneFromString(tStr))
                except YappyError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}
                except AttributeError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

            # Error-Correction
            elif property_type == "4":
                try:
                    prop = ErrCorrectProp(readOneFromString(tStr))
                except YappyError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}
                except AttributeError:
                    decision = "The property file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

        if limitTranP(aut.delta, prop.Aut.delta, LIMIT):
            decision = "Sizes of the automaton and transducer exceed limit! (See \"Technical Notes\")"
            return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}
        else:
            proof = ""
            if question == "1":
                try:
                    witness = prop.notSatisfiesW(aut)
                except TypeError:
                    decision = "The automaton file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

                if witness == (None, None) or witness == (None, None, None):
                    decision = "YES, the language satisfies the property"
                    proof = ""
                else:
                    decision = "NO, the language does not satisfy the property"
                    proof = formatCounterExample(witness)
                return {'form':form, 'automaton':autName, 'transducer':tName,
                        'result':decision, 'proof': proof}
            elif question == "2":
                try:
                    witness = prop.notMaximalW(aut)
                except PropertyNotSatisfied:
                    decision = "ERROR: the language does not satisfy the property."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}
                except TypeError:
                    decision = "The automaton file appears to be incorrectly formatted."
                    return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

                if witness is None:
                    decision = "YES, the language is maximal with respect to the property."
                else:
                    decision = "NO, the language is not maximal with respect to the property."
                    proof = formatCounterExample(witness)

                return {'form':form, 'automaton':autName, 'transducer':tName,
                        'result':decision, 'proof': proof}
    elif question == "3":
        n_num = post["n_int"];
        s_num = post["s_int"];
        l_num = post["l_int"];
        if (n_num == "" or s_num == "" or l_num == ""):
            decision = "Please enter three positive integers S, N, L."
            return {'form': form, 'error_message': decision}
        elif (int(s_num) < 2  or int(s_num) > 10):
            decision = "S must be less than 10 and greater than 1"
            return {'form': form, 'error_message': decision}
        elif (int(s_num) > int(l_num)):
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
                try:
                    a, witness = makeBlockCode(int(n_num), int(l_num), int(s_num))
                except DFAsymbolUnknown:
                    decision = "Something went wrong (views.py: construction, fixed property)."
                    return {'form': form, 'error_message': decision}
                filename = str(int(time() * 1000))
                #text_path, text_title = writeWitness(witness, filename)
                words = writeWitness(witness, filename)
                result = '<div class="text-center" style="font-size: 14px; color: #999999; margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" rows="6" cols="50" readonly>'+ words +'</textarea></div>'
                return {'form': form, 'construct_path': '', 'construct_text': '', 'result': result}

            else:
                try:
                    tStr = files['transducer_file'].read()
                except Exception:
                    decision = "Please provide a correct property file."
                    return {'form': form, 'error_message': decision}

                tName = "Property: " + files['transducer_file'].name
                # Input-Altering Property (given as trajectory or transducer)
                if property_type == "2":
                    try:
                        prop = constructInAltProp(tStr, alp)
                    except IncorrectFormat:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': tName}
                    except TypeError:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

                    if limitTranP({}, prop.Aut.delta, LIMIT, int(n_num)):
                        decision = "Size of request exceeds limit! (See \"Technical Notes\")"
                        return {'form':form, 'error_message': decision}

                    try:
                        a, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
                    except DFAsymbolUnknown:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': tName}

                    filename = str(int( time()*1000 ))
                    #text_path, text_title = writeWitness(witness, filename)
                    words = writeWitness(witness, filename)
                    result = '<div class="text-center" style="font-size: 14px; color: #999999; margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" rows="6" cols="50" readonly>'+ words +'</textarea></div>'
                    return {'form': form, 'construct_path': '', 'construct_text': '', 'result': result}
                # Input-Preserving Property
                elif property_type == "3":
                    try:
                        prop = codes.ErrDetectProp(readOneFromString(tStr))
                    except YappyError:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': tName}
                    except AttributeError:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form':form, 'error_message': decision, 'automaton':autName, 'transducer':tName}

                    if limitTranP({}, prop.Aut.delta, LIMIT, int(n_num)):
                        decision = "Size of request exceeds limit! (See \"Technical Notes\")"
                        return {'form':form, 'error_message': decision}

                    try:
                        a, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
                    except DFAsymbolUnknown:
                        decision = "The property file appears to be incorrectly formatted."
                        return {'form': form, 'error_message': decision, 'transducer': tName}

                    filename = str(int(time() * 1000))
                    #text_path, text_title = writeWitness(witness, filename)
                    words = writeWitness(witness, filename)
                    result = '<div class="text-center" style="font-size: 14px; color: #999999; margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" rows="6" cols="50" readonly>'+ words +'</textarea></div>'
                    return {'form': form, 'construct_path': '', 'construct_text': '', 'result': result}

decideRequest = 'decide whether the given language '
testDict = {'1': 'SATW', '2': 'MAXW', '3': 'MAXP', '4': 'MKCO'}
describe = {'1': decideRequest+'satisfies the given property. If no, return a witness; else return Nones.',
            '2': decideRequest+'is maximal. If no, return a witness; else return None.',
            '3': decideRequest+'is maximal.', '4': 'Construction prints out constructed words.'}
fixedDict = {'1': 'PREFIX', '2': 'SUFFIX', '3': 'INFIX',
             '4': 'OUTFIX', '5': 'HYPERCODE', '6': 'CODE'}

def writeWitness(witness, filename):
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
    s = ''
    for w in witness:
        s += w + '\n'
    return s


def getCode(post, files, form=True, testMode=None):

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

    test = testDict[question]
    prop = None
    regexp = None
    #name = "test"
    name = str(int( time()*1000 ))
    #name2 = str(int(time() * 1000))
    n_num = ""
    s_num = ""
    l_num = ""
    autStr = ""
    sigma = None
    if question == '1' or question == '2' or question == '3':
        try:
            autStr = files['automata_file'].read()
        except:
            decision = "Please provide an automaton file."
            return {'form': form, 'error_message': decision}

        try:
            aut = constructAutomaton(autStr)
            #autStr = saveToString(aut, '\n')
        except IncorrectFormat:
            decision = "ERROR: the automaton appears to be incorrectly formatted"
            return {'form': form, 'error_message': decision}
    elif question == '4':
        n_num = post["n_int"];
        s_num = post["s_int"];
        l_num = post["l_int"];
        if (n_num == "" or s_num == "" or l_num == ""):
            decision = "Please enter three positive integers S, N, L."
            return {'form': form, 'error_message': decision}
        elif (int(s_num) < 2  or int(s_num) > 10):
            decision = "S must be less than 10 and greater than 1"
            return {'form': form, 'error_message': decision}
        elif (int(s_num) > int(l_num)):
            decision = "S must be less than L"
            return {'form': form, 'error_message': decision}


    # Fixed Property
    if property_type == "1":
        tStr = None
        fixed_type = post['fixed_type']
        prop = fixedDict[fixed_type]
    else:
        try:
            tStr = files['transducer_file'].read()
        except:
            decision = "Please provide a property file."
            return {'form':form, 'error_message': decision}

        # Input-Altering Property (given as trajectory or transducer)
        if property_type == "2":

            try:
                m = readOneFromString(tStr)
                if type(m) is NFA or type(m) is DFA:
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
                        buildTrajPropS(tStr, aut.Sigma)
                    elif question == '4':
                        alp = set()
                        for i in range(int(s_num)):
                            alp.add(str(i))
                        buildTrajPropS(tStr, alp)
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
                IPTProp(readOneFromString(tStr))
            except:
                decision = "The property file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision}

            prop = "INPRES"

        # Error-Correction
        elif property_type == "4":
            try:
                ErrCorrectProp(readOneFromString(tStr))
            except YappyError:
                decision = "The property file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision}
            prop = "ERRCORR"

    prog_lines = genProgram(name, prop, test, autStr, tStr, sigma, regexp, describe[question], testMode, s_num, l_num, n_num)

    if testMode is not None:
        return prog_lines
    else:
        decision = "<a href='"+settings.MEDIA_URL+"%s.zip'> Download your code </a></br> (See 'Technical notes')" % name
        return {'form': form, 'result': decision}


def createFixedProperty(alphabet, n):
    """
    """
    if n == "1":
        return buildPrefixProperty(alphabet)
    elif n == "2":
        return buildSuffixProperty(alphabet)
    elif n == "3":
        tran = infixTransducer(alphabet)
        return IATProp(tran)
    elif n == "4":
        return buildOutfixProperty(alphabet)
    elif n == "5":
        return buildHypercodeProperty(alphabet)


def index(request):
    return render_to_response('index.html')


def examples(request, example_type):
    return render_to_response('examples/'+example_type+'.html')
