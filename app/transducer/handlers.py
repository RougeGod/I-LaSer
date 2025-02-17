"""Module contains all of the various handlers for different branches of the site."""

import re

import django
from django.conf import settings

from FAdo.fio import readOneFromString

from FAdo.codes import UDCodeProp, PropertyNotSatisfied, IPTProp, DFAsymbolUnknown, \
    ErrCorrectProp, buildErrorDetectPropS, IATProp

from FAdo.prax import GenWordDis, prax_maximal_nfa, Dirichlet

from app.transducer.laser_shared import construct_automaton, detect_automaton_type, IncorrectFormat, \
     construct_input_alt_prop, limit_aut_prop, limit_tran_prop, format_counter_example, \
     make_block_code, limit_theta_prop, is_subset, convertToCorrectType, check_construction_alphabets

from app.transducer.util import create_fixed_property, write_witness, parse_aut_str, parse_theta_str, \
                                apply_theta_antimorphism, reverse_theta_antimorphism, parse_transducer_string

from lark import UnexpectedCharacters
from lark.exceptions import VisitError

PROPERTY_INCORRECT_FORMAT = 'The property appears to be incorrectly formatted.'
AUTOMATON_INCORRECT_FORMAT = "The automaton or regular expression appears to be invalid."
ALPHABET_TOO_SMALL = "The construction alphabet is larger than the transducer's alphabet."

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250

def error(form, err):
    """Formats an error using the given string"""
    return {'form': form, 'error_message': err}

def handle_iap(
        n_num, l_num, s_num,
        t_name, t_str, form=True
    ):
    """Handle Input-altering properties"""
    # Creating an alphabet of the given size
    alphabet = set()
    for i in range(int(s_num)):
        alphabet.add(str(i))

    # Create the Input Altering Property
    try:
        prop = construct_input_alt_prop(t_str, alphabet)
        err = check_construction_alphabets(s_num, prop.Aut.Sigma)
        if err is not None:
            return {'form': form, 'error_message':err,
                'transducer': t_name}
    except (IncorrectFormat, TypeError):
        return {'form': form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'transducer': t_name}

    # Check to see if the computation would be too computationally expensive
    if limit_tran_prop({}, prop.Aut.delta, LIMIT, int(n_num)):
        raise LimitExceeded("Construction: IAP")

    # Attempt to create the code, that satisfies the given property.
    try:
        _, witness = prop.makeCode(n_num, l_num, s_num)
    except:
        return {'form': form, 'error_message':"Unexpected issue constructing language.",
                'transducer': t_name}

    # If successful, return the given words that satisfy it.
    words = write_witness(witness)
    #create the special text area for construction output
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
        prop = buildErrorDetectPropS(t_str + "\n") #directly calls FAdo code so we need to add the newline here
        err = check_construction_alphabets(s_num, prop.Aut.Sigma)
        if err is not None:
            return {'form':form, 'error_message':err,
                'transducer':t_name}
    except AttributeError:
        return {'form':form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'transducer':t_name}
    except UnexpectedCharacters:
        return {'form':form, 'error_message':"Failed to parse transducer. Did you input a trajectory?",
                'transducer':t_name}

    # Check to see if the computation would be too computationally expensive
    if limit_tran_prop({}, prop.Aut.delta, LIMIT, int(n_num)):
        raise LimitExceeded("Input-Preserving Property")

    try:
        # Create a language that satisfies the property - witness is the list of words in L
        _, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
    except:
        return {'form': form, 'error_message':"Unexpected issue constructing language.",
                'transducer': t_name}

    #text_path, text_title = write_witness(witness, filename)
    words = write_witness(witness)
    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
    return {'form': form, 'witness': witness, 'prop': prop,
            'construct_path': '', 'construct_text': '', 'result': result}

def handle_construction(
        property_type, data, files, form
    ):
    """
    Handle the construction choice of the website.
    """

    def error(msg):
        return {"form": form, 'error_message': msg}

    # The post passes the sizes as string, so we need to parse them.
    # This has the added benefit of that if no numbers are given, it defaults to -1,
    # Which will fail!
    n_num = convertToCorrectType(data.get("n_int"), -1, desiredType=int)
    s_num = convertToCorrectType(data.get("s_int"), -1, desiredType=int)
    l_num = convertToCorrectType(data.get("l_int"), -1, desiredType=int)

    err = ''
    # Checking number's validity
    if n_num <= 0 or s_num <= 0 or l_num <= 0:
        err = "Please enter three positive integers S, N, L."
    elif s_num < 2 or s_num > 10:
        err = "S must be less than 10 and greater than 1"
    if err:
        return error(err)

    if not property_type:
        return error("Please select a property type.")

    if property_type == "1":
        # Check to see if the computation will be too expensive
        if (n_num * l_num) > LIMIT:
            raise LimitExceeded("Construction: Fixed Type")
        try:
            _, witness = make_block_code(n_num, l_num, s_num)
        except DFAsymbolUnknown:
            return error("Could not construct examples (Construction, fixed type).")
        #text_path, text_title = write_witness(witness, filename)
        words = write_witness(witness)
        result = '<div class="text-center" style="font-size: 14px; \
        color: #999999; margin-bottom: 10px;">Your Output</div>\
        <div><textarea class="text-center" rows="6" cols="50" \
        readonly>'+ words +'</textarea></div>'
        return {'form': form, 'construct_path': '',
                'construct_text': '', 'result': result}

    if not data.get("transducer_text"):
        return error('Please provide a property file.')

    t_str = parse_transducer_string(data.get('transducer_text'))["t_str"]

    t_name = data.get('trans_name', 'TextareaProperty')


    # Input Altering Property
    if property_type == '2':
        result = handle_iap(n_num, l_num, s_num, t_name, t_str, form)
    # Input-Preserving Property
    elif property_type == '3':
        result = handle_ipp(n_num, l_num, s_num, t_name, t_str, form)
    else:
        return error("This feature has not yet been implemented.")

    return result

def check_approx_maximality(automaton, prop, eps, t, disp):
    if not (0 < eps < 1):
        return error("Epsilon must be between 0 and 1.")
    if not (t > 1):
        return error("T must be greater than 1.")
    if not (disp >= 0):
        return error("Displacement must be non-negative.")
    pdist = Dirichlet(t=t, d=disp) #Dirichlet t is the same as the t in this function argument
    wordDist = GenWordDis(pdist, automaton.Sigma, eps)
    witness = prax_maximal_nfa(wordDist, automaton, prop)
    if witness is None:
        return "Yes, the language is approximately maximal with respect to the property.", ""
    else:
        return "No, the language is not maximal with respect to the property.", format_counter_example(witness)

def check_satisfaction(automaton, prop):
    try:
        witness = prop.notSatisfiesW(automaton)
    except TypeError:
        decision = AUTOMATON_INCORRECT_FORMAT
        return {'error_message': decision}
    if witness == (None, None) or witness == (None, None, None):
        decision = 'YES, the language satisfies the property'
        proof = ''
        satisfaction = True
    elif (type(prop) == IATProp) and (witness[0] == witness[1]):
        return {'error_message': "This is an input-preserving property, not an input-altering property."}
    else:
        decision = 'NO, the language does not satisfy the property'
        proof = format_counter_example(witness)
        satisfaction = False
    return {'result':decision, 'proof': proof, "isSatisfied": satisfaction}



def handle_satisfaction_maximality(
        property_type, question, data, files, form
    ):
    """This method handles satisfaction and maximality choices."""
    def error(err):
        """Formats an error using the given string"""
        return {'form': form, 'error_message': err}

    # Try and get an automata file from the file/text uploaded.
    aut_str = data.get('automata_text')

    if not aut_str:
        return error('Please provide an automaton file.')
    try:
        aut_str = parse_aut_str(aut_str) #remove comments and convert from Grail
    except ValueError as ex:
        return error(str(ex))

    try:
        aut = construct_automaton(aut_str)
        #get the name of the automaton (web-only)
        aut_name = "Language: " + data.get('aut_name',
            'Textarea Regex' if detect_automaton_type(aut_str) == "str2regexp" else "Textarea Automaton")
    except (IncorrectFormat, TypeError): # Automata syntax error, of any type
        return error(AUTOMATON_INCORRECT_FORMAT)
    except VisitError: #only ever gotten this when putting an NFA and calling it a DFA
        return error("This should be an NFA, not a DFA.")
    except Exception: #catch-all, just in case of other unforeseen errors
        return error("Unexpected error parsing automaton.")


    # Check to see if the computation would be too computationally expensive
    try:
        if limit_aut_prop(aut, LIMIT_AUTOMATON):
            raise LimitExceeded("Automaton")
    except AttributeError:
        if type(aut) == list: #When parsing, if there are multiple NFAs, FAdo returns a list
            return error("Only one automaton may be inputted at a time.")
        return error("The automaton appears to be incorrectly formatted.")
    if property_type == "1": # Fixed type
        t_name = ""
        fixed_type = data.get('fixed_type')
        if fixed_type is None:
            return {'form': form, 'error_message': "No fixed type was entered.",
                'automaton': aut_name}

        # This method will return the fixed property based on the parameters given
        prop = create_fixed_property(aut.Sigma, fixed_type)
        #UDCodeProp has no Aut attribute, so as of now, it cannot be checked for approximate
        #maximality, and the web limits on transducer size cannot be checked, so we must handle
        #this seperately.
        if type(prop) == UDCodeProp:
            proof = ''
            if question == '1':
                # Satisfaction
                witness = prop.notSatisfiesW(aut)
                if witness == (None, None):
                    decision = "YES, the language satisfies the code property"
                else:
                    decision = "NO, the language does not satisfy the code property"
                    proof = format_counter_example(witness)
            elif question == '2': #maximality
                if prop.notSatisfiesW(aut) != (None, None):
                    return error("ERROR: The language does not satisfy the property.")
                if prop.maximalP(aut):
                    decision = "YES, the language is a maximal code"
                else:
                    decision = "NO, the language is not a maximal code"
            elif question == '4':
                return error("Approximate Maximality is not available for the UD Code Property.")

            return {'form': form, 'automaton': aut_name, 'result': decision, 'proof': proof}

    # User-Input Property
    else:
        if (data.get('transducer_text') is None):
            return error("Please provide a property.")
        t_str = parse_transducer_string(data.get('transducer_text'))["t_str"]
        t_name = 'Property: ' + data.get('trans_name', 'Textarea-defined property.')

        if not t_str:
            return error('Please provide a property file.')

        if not property_type:
            return error('Please provide a property type.')
        # Input-Altering Property (given as trajectory or transducer)
        if property_type == "2":
            try:
                prop = construct_input_alt_prop(t_str, aut.Sigma)
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except (IncorrectFormat, TypeError):
                return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                        'automaton':aut_name, 'transducer':t_name}

        # Error-Detection
        elif property_type == "3":
            try:
                prop = IPTProp(readOneFromString(t_str + "\n"))
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except Exception: #catch-all, likely AttributeError or UnexpectedCharacters
                return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                        'automaton':aut_name, 'transducer':t_name}

        # Error-Correction
        elif property_type == "4":
            try:
                prop = ErrCorrectProp(readOneFromString(t_str + "\n"))
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except Exception: #catch-all, likely AttributeError or UnexpectedCharacters
                return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                        'automaton':aut_name, 'transducer':t_name}
        elif property_type == '5': # We have to branch off, it is handled differently.
            if (question != '1'): #asking a non-satisfaction question (currently unsupported, this might change in the future)
                return error("This feature has not yet been implemented.")
            try:
                prop = IPTProp(readOneFromString(t_str + "\n"))
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except UnexpectedCharacters: #caused by inputting a trajectory
                try:
                    prop = construct_input_alt_prop(t_str, aut.Sigma)
                except Exception: #not a parseable trajectory or transducer, error out
                    return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                            'automaton':aut_name, 'transducer':t_name}

            # Here is extra work for DNA Code Property
            try:
                theta = parse_theta_str(data.get('theta_text'))
            except Exception:
                return {'form': form, 'error_message': 'Theta appears to be incorrectly formatted.',
                        'automaton': aut_name, 'transducer': t_name}

            if limit_theta_prop(aut.delta, prop.Aut.delta, theta, LIMIT):
                raise LimitExceeded("Theta")

            theta_aut = apply_theta_antimorphism(aut, theta)

            witness = prop.Aut.inIntersection(aut).outIntersection(theta_aut).nonEmptyW()

            if witness == (None, None):
                decision = 'YES, the language satisfies the theta-transducer property'
                proof = ''
            else:
                decision = 'NO, the language does not satisfy the property'

                witness = (witness[0], reverse_theta_antimorphism(witness[1], theta))

                proof = format_counter_example(witness, True)
            return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                    'result':decision, 'proof': proof}

    try:# Check to see if the computation would be too computationally expensive
        if limit_tran_prop(aut.delta, prop.Aut.delta, LIMIT):
            raise LimitExceeded("Satisfaction/Maximality")
    except AttributeError: #caused when there is no prop (user error), or there is no prop.Aut (UD Code)
        return {'form':form, 'error_message':
        'Error creating property.',
        'automaton':aut_name, 'transducer':t_name}


    # Check Satisfaction
    if question == '1':
        sat = check_satisfaction(aut, prop)
        if sat.get("error_message"):
            return {'form':form, 'error_message': sat.get("error_message"),
                    'automaton':aut_name, 'transducer':t_name}
        else:
            return {"form": form, "automaton": aut_name, "transducer": t_name,
                   "result": sat.get("result"), "proof": sat.get("proof")}
    # Check Maximality
    elif question == '2':
        err = ''
        try:
            witness = prop.notMaximalW(aut)
        except PropertyNotSatisfied:
            err = 'ERROR: The language does not satisfy the property.'
        except TypeError:
            err = AUTOMATON_INCORRECT_FORMAT
        if err:
            return {'form':form, 'error_message': err,
                    'automaton':aut_name, 'transducer':t_name}

        if witness is None:
            decision = 'YES, the language is maximal with respect to the property.'
            proof = ''
        else:
            decision = 'NO, the language is not maximal with respect to the property.'
            proof = format_counter_example(witness)

        return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                'result':decision, 'proof': proof}
    elif question == "4":
        #check satisfaction (maximality without satisfaction makes no sense)
        sat = check_satisfaction(aut, prop)
        if (sat.get("error_message")):
            return {'form':form, 'error_message': sat.get("error_message"),
                    'automaton':aut_name, 'transducer':t_name}
        elif not (sat["isSatisfied"]):
            return {"form": form, "error_message": "ERROR: The language does not satisfy the property.",
                    "automaton": aut_name, "transducer": t_name}
        else:
            try:
                epsi = float(data.get('epsilon'))
                t = float(data.get('dirichletT'))
                disp = int(data.get('displacement'))
            except (ValueError, TypeError):
                return error("Invalid Approximation Parameters")
            decision, proof = check_approx_maximality(aut, prop, epsi, t, disp)
            if t_name == "":
                return {'form': form, 'automaton': aut_name, 'result': decision, "proof": proof}
            else:
                return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                    'result':decision, 'proof': proof}

class LimitExceeded(Exception): #define a new error type for when an automaton or property is too complex
    pass                        #to even attempt quick calculation
    