"""Various Utility methods used throughout the program"""

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
        num /= base
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

    aut_str = re.sub(r'\r', '', aut_str)
    aut_str = re.sub(r'\n#.+\n', '\n', aut_str)
    aut_str = re.sub(r'#.+', '', aut_str)

    count = 0
    for line in aut_str.splitlines():
        if line.startswith('@'):
            count += 1

    result = {
        'aut_str': None,
        'fixed_type': None,
        'trajectory': None,
        'transducer': None,
        'transducer_type': None
    }

    if aut_str.strip().startswith('(START)'):
        result['aut_str'] = aut_str
        return result

    if count == 0: # Trajectory and Regex
        res = re.search(r'(.+?)\n([\s\S]+)', aut_str)
        if res:
            result['trajectory'] = res.group(1)
            result['aut_str'] = res.group(2)
            return result
    elif count == 1: # @DFA or @NFA, or Fixed type with regex, or transducer with regex
        if not aut_str.startswith('@'):
            res = re.search(r'(.+?)\n([\s\S]+)', aut_str)
            result['trajectory'] = res.group(1)
            result['aut_str'] = res.group(2)
        else:
            if aut_str.startswith(\
                    ('@PREFIX', '@SUFFIX', '@INFIX', '@OUTFIX', '@HYPERCODE', '@CODE')):
                res = re.search(r'@(.+)([\s\S]+)', aut_str)
                result['fixed_type'] = res.group(1)
                result['aut_str'] = res.group(2)
            elif aut_str.startswith('@Transducer'):
                res = re.search(r'(@Transducer.+\n(\d+ *([\w\d]|@epsilon) *([\w\d]|@epsilon) *\d+ *\n)+)(.+)', aut_str)
                result['transducer'] = res.group(1)
                result['aut_str'] = res.group(5)
            else:
                result['aut_str'] = aut_str

        return result
    # Three choices: Fixed Type, Transducer Without Type, Transducer with type with regex
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

# pylint:disable=C0201
def parse_theta_str(theta_str):
    """Parses the theta string into a dict used to convert automata"""

    match = re.search(r'^@THETA *\n(([\w\d] +[\w\d]\s*)+)', theta_str)

    swaps = match.group(1)

    result = {}
    for swap in swaps.splitlines():
        tmp = swap.split(' ')
        result[tmp[0]] = tmp[1]

    for key in result.keys():
        result[result[key]] = key

    return result

def apply_theta_antimorphism(aut, theta):
    """Update the automaton to reverse start and end states, reverse transitions, and update sigma"""
    orig = aut
    aut = aut.toNFA()

    newDelta = {}

    # Update transitions to theta(old)
    for delta in aut.delta:
        newDelta[delta] = {}
        for key in theta:
            try:
                newDelta[delta][theta[key]] = aut.delta[delta][key]
            except KeyError:
                continue

    aut.delta = newDelta

    # Swap Initial and Final States
    initial = aut.Initial
    final = aut.Final

    aut.Initial = set()
    aut.Final = set()
    for index in final:
        aut.addInitial(aut.stateIndex(aut.States[index]))
    for index in initial:
        aut.addFinal(aut.stateIndex(aut.States[index]))

    # Swap transitions
    delta = aut.delta

    aut.delta = {}

    for to in delta:
        for val in delta[to]:
            for frm in delta[to][val]:
                if not frm in aut.delta:
                    aut.delta[frm] = {}
                
                if not val in aut.delta[frm]:
                    aut.delta[frm][val] = set()

                aut.delta[frm][val].add(to)

    orig.delta == aut.delta

    return aut
