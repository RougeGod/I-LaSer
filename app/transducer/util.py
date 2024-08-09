"""Various Utility methods used throughout the program"""
import copy
import re

import FAdo.codes as codes
from FAdo.codes import IATProp

from .expand_carets import expand_carets

def list_to_string(list_, dict_):
    """turns a list into a string"""
    return "".join([dict_[i] for i in list_])

def long_to_base(num, base):
    """Maps num to a list of digits corresponding to base q representation of n in reverse order"""
    list_ = []
    while num > 0:
        list_.append(num % base)
        num //= base
    return list_

def create_fixed_property(alphabet, fixed_type):
    """
    Create a property of a fixed variety such as prefix or suffix codes
    """
    result = None
    if fixed_type in ["1", "PREFIX", 1]:
        result = codes.buildPrefixProperty(alphabet)
    elif fixed_type in ["2", "SUFFIX", 2]:
        result = codes.buildSuffixProperty(alphabet)
    elif fixed_type in ["3", "BIFIX", 3]:
        result = codes.buildPrefixProperty(alphabet) & codes.buildSuffixProperty(alphabet)
    elif fixed_type in ["4", "INFIX", 4]:
        result = IATProp(codes.infixTransducer(alphabet))
    elif fixed_type in ["5", "OUTFIX", 5]:
        result = codes.buildOutfixProperty(alphabet)
    elif fixed_type in ["6", "CODE", 6]:
        result = codes.UDCodeProp(alphabet)
    elif fixed_type in ["7", "HYPERCODE", 7]:
        result = codes.buildHypercodeProperty(alphabet)
    return result

def write_witness(witness):
    """Creates the witness for a given error"""
    string = ''
    for line in set(witness):
        string += line + '\n'
    return string

def parse_aut_str(aut_str):
    """
    Cleans up the automata string inputted through a file or textarea, removing
    commented lines, commented line parts, and normalizing newlines to UNIX format. 
    Will also convert input from Grail to FAdo, if necessary. 

    Formerly allowed a property to be input in the NFA area, but this functionality
    has been removed as of Version 6. 
    """

    aut_str = re.sub(r'\r', '', aut_str)
    aut_str = re.sub(r'\n#.+\n', '\n', aut_str)
    aut_str = re.sub(r'#.+', '', aut_str)

    aut_str = aut_str.strip()

    if "@Transducer" in aut_str:
        raise IncorrectFormat("Please enter the transducer in its own input area.")
    
    if "(START)" in aut_str:
        result = convertGrailToFAdo(aut_str.strip())
        return result

    if not ("@DFA" in aut_str or "@NFA" in aut_str):
        aut_str = expand_carets(aut_str)            

    result = aut_str.strip()
    return result

def parse_transducer_string(t_str):
    result = {
    "t_str": None,
    #add more fields if necessary
    }    
    if (t_str is None):
        return None
    #removes comments and normalizes newlines
    t_str = re.sub(r'\r', '', t_str.strip())
    t_str = re.sub(r'\n#.+\n', '\n', t_str)
    t_str = re.sub(r'#.+', '', t_str)
    result["t_str"] = t_str.strip()
    return result

def convertGrailToFAdo(grailString):
    '''Converts a Grail-formatted string to a FAdo-formatted string for use in 
       both generated programs and in-website solving. The website will use this converted
       string in all operations without interacting with the original Grail.
       Accepts String, returns String'''
    splitString = grailString.strip().split("\n")
    startStates = set()
    isStartStateInLines = False
    endStates = set()
    otherLines = []
    for line in splitString:
        if line.strip().startswith("(START) |-"):
            if (len(line.strip().split()) == 3): 
                startStates.add(line.strip().split()[2])
            else: 
                raise IncorrectFormat("The Grail string has an improper start state.")
        elif line.strip().endswith("-| (FINAL)"):
            if (len(line.strip().split()) == 3):
                endStates.add(line.strip().split()[0])
            else: 
                raise IncorrectFormat("The Grail string has an improper final state.")
        else: #intermediate line 
            otherLines.append(line)
    if len(startStates) == 0:
        raise IncorrectFormat("The start state of the Grail string was not specified.")
    if len(endStates) == 0:
        raise IncorrectFormat("The final state of the Grail string was not specified.")
    firstLine = "@NFA "
    for state in endStates:
        firstLine += str(state) + " "
    firstLine += "* "
    for state in startStates:
        firstLine += str(state) + " "
    firstLine = firstLine.strip() + "\n" #remove the last trailing space
    return firstLine + "\n".join(otherLines)
    

# pylint:disable=C0201
def parse_theta_str(theta_str):
    """Parses the theta string into a dict used to convert automata
       Example: If the Theta string is:
       @THETA
       a t
       c g
       return a dictionary {a:t, t:a, c:g, g:c}"""

    match = re.search(r'^@THETA *\n(([\w\d] +[\w\d]\s*)+)', theta_str, re.IGNORECASE)

    swaps = match.group(1) #remove the @THETA, which is only used to determine whether 
                           #it's an antimorphism and not used in creating it. 

    initial = {} #The initially entered swaps
    reverse = {} #The inverse of each swap
    for swap in swaps.splitlines(): #collect the swap from each of the lines and add those in
        tmp = swap.split(' ')
        initial[tmp[0]] = tmp[1] #contains the entered swaps

    for key in initial.keys():
        reverse[initial[key]] = key #reverse each of the entered swaps, put that in its own dict

    return initial | reverse #the union of the two dictionaries, containing both forward and backward swaps

def reverse_theta_antimorphism(word, theta):
    new_word = ''
    for c in word[::-1]:
        new_word += theta[c]

    return new_word

def apply_theta_antimorphism(aut, theta):
    """Update the automaton to reverse start and end states, reverse transitions, and update sigma"""
    new_aut = copy.deepcopy(aut.toNFA())

    newdelta = {}

    # Update transitions to theta(old)
    for delta in new_aut.delta:
        newdelta[delta] = {}
        for key in theta:
            try:
                newdelta[delta][theta[key]] = new_aut.delta[delta][key]
            except KeyError:
                continue

    new_aut.delta = newdelta

    # Swap Initial and Final States
    initial = new_aut.Initial
    final = new_aut.Final

    new_aut.Initial = set()
    new_aut.Final = set()
    for index in final:
        new_aut.addInitial(new_aut.stateIndex(new_aut.States[index]))
    for index in initial:
        new_aut.addFinal(new_aut.stateIndex(new_aut.States[index]))

    # Swap transitions
    delta = new_aut.delta
    new_aut.delta = {}

    for endstate in delta:
        for val in delta[endstate]:
            for startstate in delta[endstate][val]:
                if not startstate in new_aut.delta:
                    new_aut.delta[startstate] = {}
                if not val in new_aut.delta[startstate]:
                    new_aut.delta[startstate][val] = set()
                new_aut.delta[startstate][val].add(endstate)

    return new_aut

class IncorrectFormat(Exception):
    """IncorrectFormat error"""
    pass
