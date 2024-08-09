'''Code mostly copy-pasted with a few modifications from the original LaSer web version
   for the LaSer local (installable) version which does not use any web technologies. 

   The returned result is still a dict, as I would like the local version to 
   be able to distinguish errors from regular results.'''

import re

from .FAdo.fio import readOneFromString

from .FAdo.codes import UDCodeProp, PropertyNotSatisfied, IPTProp, DFAsymbolUnknown, \
    ErrCorrectProp, buildErrorDetectPropS, IATProp

from .FAdo.prax import GenWordDis, prax_maximal_nfa, Dirichlet

from .laser_shared import construct_automaton, detect_automaton_type, IncorrectFormat, \
     construct_input_alt_prop, format_counter_example, \
     make_block_code, is_subset, convertToCorrectType, check_construction_alphabets

from .util import create_fixed_property, write_witness, parse_aut_str, parse_theta_str, \
                                apply_theta_antimorphism, reverse_theta_antimorphism, parse_transducer_string

from lark import UnexpectedCharacters
from lark.exceptions import VisitError

from func_timeout import func_timeout, FunctionTimedOut

PROPERTY_INCORRECT_FORMAT = 'The property appears to be incorrectly formatted.'
AUTOMATON_INCORRECT_FORMAT = "The automaton or regular expression appears to be invalid."

def error(err):
    """Formats an error using the given string"""
    return {'error_message': err}


def get_response(data):
    """
    Handle the actual response based on the inputted data to the GUI program. 
    """
    question = data.get('question')
    property_type = data.get('property_type')
    time_limit = data.get('time_limit')

    if not question: #User clicked submit without specifying question (question is 0, so not question is true)
        return {'error_message': "Please select a question."}
    if not property_type: 
        return {"error_message": "Please select a property type."}

    if (time_limit is None) or (time_limit <= 0): #no lime limit, go to completion no matter how long 
        if question in [1, 2, 4]:
            return handle_satisfaction_maximality(data)
        elif question == 3:
            return handle_construction(data)
    
    if question in [1, 2, 4]:
        try:
            return func_timeout(time_limit, handle_satisfaction_maximality, args=(data,)) 
        #args must be a tuple, as if this is not, it is treated as a dict
        except FunctionTimedOut:
            return {"error_message": "The function timed out."}
    elif question == 3:
        try: 
            return func_timeout(time_limit, handle_construction, args=(data,))
        except FunctionTimedOut: 
            return {"error_message": "The function timed out."}
        
def handle_iap(
        n_num, l_num, s_num, t_str
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
            return error(err)
    except (IncorrectFormat, TypeError):
        return {'error_message': PROPERTY_INCORRECT_FORMAT}

    # Attempt to create the code, that satisfies the given property (construction only).
    try:
        _, witness = prop.makeCode(n_num, l_num, s_num)
    except DFAsymbolUnknown:
        return error("The transducer's alphabet does not match the construction alphabet.") 
        #probably not necessary, check_construction_alphabet

    # If successful, return the given words that satisfy it.
    words = write_witness(witness)
    return {'result': words}

def handle_ipp(
        n_num, l_num, s_num, t_str
    ):
    """Handle Input-preserving properties"""
    try:
        prop = buildErrorDetectPropS(t_str + "\n") #directly calls FAdo code so we need to add the newline here
        err = check_construction_alphabets(s_num, prop.Aut.Sigma)
        if err is not None:
            return error(err)
    except AttributeError:
        return {'error_message':PROPERTY_INCORRECT_FORMAT}
    except UnexpectedCharacters:
        return error("Failed to parse transducer. Did you input a trajectory?")
    try:
        # Create a language that satisfies the property - witness is the list of words in L
        _, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
    except DFAsymbolUnknown:
        return {'error_message':"Unexpected issue with construction alphabet."}

    words = write_witness(witness)
    return {'result': words}

def handle_construction(data):
    """
    Handle the construction choice of the application.
    """
    # The post passes the sizes as string, so we need to parse them.
    # This has the added benefit of that if no numbers are given, it defaults to -1,
    # Which will fail!
    n_num = convertToCorrectType(data.get("n_int"), -1, desiredType=int)
    s_num = convertToCorrectType(data.get("s_int"), -1, desiredType=int)
    l_num = convertToCorrectType(data.get("l_int"), -1, desiredType=int)
    property_type = data.get("property_type")

    err = ''
    # Checking number's validity
    if n_num <= 0 or s_num <= 0 or l_num <= 0:
        err += "Please enter three positive integers S, N, L."
    elif s_num < 2 or s_num > 10:
        err += "S must be less than 10 and greater than 1"
    if err:
        return error(err)

    if not property_type:
        return error('Please select a property type.')

    if property_type == 1:
        try:
            _, witness = make_block_code(n_num, l_num, s_num)
        except DFAsymbolUnknown:
            return error("Could not construct examples (Construction, fixed type).")
        words = write_witness(witness)
        return {'result': words}

    if not data.get("transducer_text"):
        return error('Please provide a property file.')

    t_str = parse_transducer_string(data.get('transducer_text'))["t_str"]

    # Input Altering Property
    if property_type == 2:
        result = handle_iap(n_num, l_num, s_num, t_str)
    # Input-Preserving Property
    elif property_type == 3:
        result = handle_ipp(n_num, l_num, s_num, t_str)
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
    



def handle_satisfaction_maximality(data):
    question = data.get("question")
    property_type = data.get("property_type")
    
    """This method handles satisfaction and maximality choices."""
    def error(err):
        """Formats an error using the given string"""
        return {'error_message': err}

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
    except (IncorrectFormat, TypeError): # Automata syntax error
        return error(AUTOMATON_INCORRECT_FORMAT)
    except VisitError: #multiple paths, or multiple start states for a DFA
        return error("This should be an NFA, not a DFA")
    except Exception: 
        return error("Unexpected error parsing automaton.")

    if type(aut) == list: 
        #When parsing, if there are multiple NFAs, FAdo returns a list. 
        #Multiple languages at once are not permitted 
        return error("Only one automaton may be inputted at a time.")

    if property_type == 1: # Fixed type
        fixed_type = data.get('fixed_type')
        if fixed_type is None:
            return {'error_message': "No fixed type was entered."}
            
        # This method will return a fixed property, or None if it's a UD Code.
        prop = create_fixed_property(aut.Sigma, fixed_type)
        if type(prop) == UDCodeProp:
            # Create the UD Code Property
            prop = UDCodeProp(aut.Sigma)
            proof = ''
            if question == 1:
                # Satisfaction. UDCode does not have a Prop.Aut, so we need
                #to handle satisfaction seperately.
                witness = prop.notSatisfiesW(aut)
                if witness == (None, None):
                    decision = "YES, the language satisfies the code property"
                else:
                    decision = "NO, the language does not satisfy the code property"
                    proof = format_counter_example(witness)
            elif question == 2:
                # Maximality
                if prop.notSatisfiesW(aut) != (None, None):
                    return error("ERROR: The language does not satisfy the code property.")
                if prop.maximalP(aut):
                    decision = "YES, the language is a maximal code"
                else:
                    decision = "NO, the language is not a maximal code"
            elif question == 4:
                #approximate maximality
                return error("Approximate Maximality is not available for the UD Code Property.")
            return {'result': decision, 'proof': proof}    
                

    # User-Input Property
    else:
        if (data.get('transducer_text') is None):
            return error("Please provide a property.")
        t_str = parse_transducer_string(data.get('transducer_text'))["t_str"]

        if not t_str:
            return error('Please provide a property file.')

        if not property_type:
            return error('Please provide a property type.')
        # Input-Altering Property (given as trajectory or transducer)
        if property_type == 2:
            try:
                prop = construct_input_alt_prop(t_str, aut.Sigma)
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except (IncorrectFormat, TypeError):
                return error(PROPERTY_INCORRECT_FORMAT)

        # Error-Detection
        elif property_type == 3:
            try:
                prop = IPTProp(readOneFromString(t_str + "\n"))
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except Exception: #catch-all, likely AttributeError or UnexpectedCharacters
                return {'error_message': PROPERTY_INCORRECT_FORMAT}

        # Error-Correction
        elif property_type == 4:
            try:
                prop = ErrCorrectProp(readOneFromString(t_str + "\n"))
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except Exception: #catch-all, likely AttributeError or UnexpectedCharacters
                return error(PROPERTY_INCORRECT_FORMAT)

        elif property_type == 5: # We have to branch off, it is handled differently.
            if (question != 1):
                return error("This feature has not yet been implemented.")
            try:
                prop = IPTProp(readOneFromString(t_str + "\n"))
                if not is_subset(aut, prop):
                    return error("The automaton's alphabet should be a subset of the transducer's")
            except UnexpectedCharacters: #caused by inputting a trajectory
                try:
                    prop = construct_input_alt_prop(t_str, aut.Sigma)
                except Exception: #not a parseable trajectory or transducer, error out
                    return error(PROPERTY_INCORRECT_FORMAT)

            # Here is extra work for DNA Code Property
            try:
                theta = parse_theta_str(data.get('theta_text'))
            except Exception:
                return error("Theta appears to be incorrectly formatted.")

            theta_aut = apply_theta_antimorphism(aut, theta)

            witness = prop.Aut.inIntersection(aut).outIntersection(theta_aut).nonEmptyW()

            if witness == (None, None):
                decision = 'YES, the language satisfies the theta-transducer property'
                proof = ''
            else:
                decision = 'NO, the language does not satisfy the property'

                witness = (witness[0], reverse_theta_antimorphism(witness[1], theta))

                proof = format_counter_example(witness, True)
            return {'result':decision, 'proof': proof}
        else:
             return {"error_message": "Please select a valid property/question combination."}

    # Check Satisfaction
    if question == 1:
        return check_satisfaction(aut, prop)
    # Check Maximality
    elif question == 2:
        err = ''
        try:
            witness = prop.notMaximalW(aut)
        except PropertyNotSatisfied:
            err = 'ERROR: The language does not satisfy the property.'
        except TypeError:
            err = AUTOMATON_INCORRECT_FORMAT
        if err:
            return error(err)

        if witness is None:
            decision = 'YES, the language is maximal with respect to the property.'
            proof = ''
        else:
            decision = 'NO, the language is not maximal with respect to the property.'
            proof = format_counter_example(witness)

        return {'result':decision, 'proof': proof}
    elif question == 4:
        #check satisfaction (maximality without satisfaction makes no sense)
        sat = check_satisfaction(aut, prop)
        if (sat.get('error_message')):
            return error(sat.get('error_message'))
        elif not (sat["isSatisfied"]):
            return error("ERROR: The language does not satisfy the property.")
        else:
            try: 
                epsi = float(data.get('epsilon'))
                t = float(data.get('dirichletT'))
                disp = int(data.get('displacement'))
            except (ValueError, TypeError):
                return error("Invalid Approximation Parameters")
            decision, proof = check_approx_maximality(aut, prop, epsi, t, disp)
            return {'result': decision, "proof": proof}
