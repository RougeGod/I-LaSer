"""Various Utility methods used throughout the program"""
import copy
import re

import FAdo.codes as codes
from FAdo.codes import IATProp

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
    if fixed_type in ["1", "PREFIX"]:
        result = codes.buildPrefixProperty(alphabet)
    elif fixed_type in ["2", "SUFFIX"]:
        result = codes.buildSuffixProperty(alphabet)
    elif fixed_type in ["3", "INFIX"]:
        result = IATProp(codes.infixTransducer(alphabet))
    elif fixed_type in ["4", "OUTFIX"]:
        result = codes.buildOutfixProperty(alphabet)
    elif fixed_type in ["5", "HYPERCODE"]:
        result = codes.buildHypercodeProperty(alphabet)
    return result

def write_witness(witness):
    """Creates the witness for a given error"""
    string = ''
    for line in witness:
        string += line + '\n'
    return string

def parse_aut_str(aut_str):
    """
    Parses the given string for extra information
    """

    #determines whether a given candidate string could possibly
    #be a valid trajectory. A trajectory can only have the characters
    #0, 1, +, (), *, and space. A value of false indicates that this
    #cannot be a trajectory, but a value of true does not necessarily
    #indicate that this is a trajectory
    def can_be_trajectory(candidate):
        return bool(re.match(r'[01+*)( ]*', candidate))
    
    #given two regex-like objects, says which one the trajectory is and
    #which one the regex is, if it's unambiguous. 
    #if both or neither string could be a trajectory, treat the earlier string
    #(cand1) as the trajectory (LaSer's previous behaviour)
    def one_traj_one_regex(cand1, cand2):
        if can_be_trajectory(cand2) and not can_be_trajectory(cand1):
            return {"trajectory": cand2, "aut_str": cand1}
        else: 
            return {"trajectory": cand1, "aut_str": cand2}
            
        
    aut_str = re.sub(r'\r', '', aut_str)
    aut_str = re.sub(r'\n#.+\n', '\n', aut_str)
    aut_str = re.sub(r'#.+', '', aut_str)

    count = 0
    namedFields = []
    for line in aut_str.splitlines():
        if line.startswith('@'):
            count += 1
            namedFields.append(line.split()[0])

    result = {
        'aut_str': None,
        'fixed_type': None,
        'trajectory': None,
        'transducer': None,
        'transducer_type': None
    }

    #grail string inputted, assume no trajectory or transducer info in the NFA tab. 
    if aut_str.strip().startswith('(START)'):
        result['aut_str'] = convertGrailToFAdo(aut_str.strip())
        return result
    if count == 0: # Trajectory and Regex
        res = re.search(r'(.+?)\n([\s\S]+)', aut_str)
        if res:
            result |= one_traj_one_regex(res.group(1),res.group(2)) #overwrites aut_str and trajectory in the result dict
            return result
    elif count == 1: # @DFA or @NFA, or Fixed type with regex, or transducer with regex
        if not aut_str.startswith('@'):
            res = re.search(r'(.+?)\n([\s\S]+)', aut_str)
            if can_be_trajectory(res.group(1)): #trajectory + @NFA/@DFA
                result['trajectory'] = res.group(1)
                result['aut_str'] = res.group(2)
            else:                               #regex + @Transducer
                result["aut_str"] = res.group(1)
                result["transducer"] = res.group(2)
        else:
            if aut_str.startswith(\
                    ('@PREFIX', '@SUFFIX', '@INFIX', '@OUTFIX', '@HYPERCODE', '@CODE')): #fixed type + regex
                res = re.search(r'@(.+)([\s\S]+)', aut_str)
                result['fixed_type'] = res.group(1)
                result['aut_str'] = res.group(2)
            elif aut_str.startswith('@Transducer'): #transducer + regex
                res = re.search(r'(@Transducer.+\n(\d+ *([\w\d]|@epsilon) *([\w\d]|@epsilon) *\d+ *\n)+)(.+)', aut_str)
                result['transducer'] = res.group(1)
                result['aut_str'] = res.group(5)
            else: #@DFA/@NFA + trajectory, or @DFA/@NFA on its own
                res = re.search(r"(@[DN]FA(?: +\d+?)+\n(?:\d+ (?:\w|@epsilon) \d+(?:\n|$))+)(\n.*)?", aut_str)
                #start with declaration of FA type and one or more final states, then 
                #one or more lines with number_character_number, match as many of these as 
                #possible then possibly an addiotional newline and a trajectory
                if res.group(1):
                    #checking if everything is formatted correctly and the regex matches an FA
                    result['aut_str'] = res.group(1)
                    if res.group(2) is not None and res.group(2).strip(): #trajectory has non-blank characters
                        result['trajectory'] = res.group(2).strip()
                else: 
                    result['aut_str'] = aut_str #no trajectory, just an FA

        return result
    # Three choices: Fixed Type with DFA, Transducer Without Type with DFA, Transducer with type with regex
    elif count == 2:
        reg = r'@(\w+)\n(@Transducer.+\n(\d+ ([\w\d]|@epsilon) ([\w\d]|@epsilon) \d+\n)+)(.+)'

        res = re.search(r'(@[\s\S]+)\n(@[\s\S]+)$', aut_str)

        if res.group(1).strip(' @') in ['PREFIX', 'SUFFIX', 'INFIX', 'OUTFIX', 'HYPERCODE', 'CODE']:
            result['fixed_type'] = res.group(1).strip(' @')
            result['aut_str'] = res.group(2)
        elif res.group(1).strip().lower().startswith('@transducer'):
            result['transducer'] = res.group(1)
            result['aut_str'] = res.group(2)
        elif res.group(1).strip(' @') in ['InputAltering', 'ErrorDetecting', 'ErrorCorrecting']:
            res = re.search(reg, aut_str)
            result['transducer_type'] = res.group(1)
            result['transducer'] = res.group(2)
            result['aut_str'] = res.group(6)
        else:
            result['aut_str'] = aut_str

        return result
    elif count == 3: # Transducer with type
        res = re.search(r'@(.+)\n(@[\s\S]+)\n(@[\s\S]+)$', aut_str)
        result['transducer_type'] = res.group(1)
        result['transducer'] = res.group(2)
        result['aut_str'] = res.group(3)
        return result

    result['aut_str'] = aut_str
    return result

#limitation: only allows one start state
def convertGrailToFAdo(grailString):
    '''Converts a Grail-formatted string to a FAdo-formatted string for use in 
       both generated programs and in-website solving. Limitation: Because FAdo
       only supports one start state per automaton, the converted Grail string
       must also only have one start state. The website will use this converted 
       string in all operations without interacting with the original Grail.
       Accepts String, returns String'''
    splitString = grailString.strip().split("\n")
    startState = None
    endStates = set()
    otherLines = []
    for line in splitString:
        if line.strip().startswith("(START) |-"):
            if (startState is None and len(line.strip().split()) == 3): 
                #make sure that we have no previous start states and only one inputted start state
                startState = line.strip().split()[2]
            else: 
                raise IncorrectFormat("The Grail string has too many or improper start states.")
        elif line.strip().endswith("(FINAL)"):
            if (len(line.strip().split()) == 3):
                endStates.add(line.strip().split()[0])
            else: 
                raise IncorrectFormat("The Grail string has an improper final state.")
        else: #intermediate line 
            if (startState is not None) and (line.strip().split()[0] == startState):
                otherLines = [line] + otherLines #appends this line to the start of the intermediate lines
            else:
                otherLines.append(line)
    if startState is None:
        raise IncorrectFormat("The start state of the Grail string was not specified.")
    if len(endStates) == 0:
        raise IncorrectFormat("The final state of the Grail string was not specified.")
    else: 
        firstLine = "@NFA "
        for state in endStates:
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

    initial = {} #The initially entered 
    reverse = {} 
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
