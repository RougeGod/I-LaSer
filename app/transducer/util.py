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
    if fixed_type == "1" or fixed_type == "PREFIX":
        result = codes.buildPrefixProperty(alphabet)
    elif fixed_type == "2" or fixed_type == "SUFFIX":
        result = codes.buildSuffixProperty(alphabet)
    elif fixed_type == "3" or fixed_type == "INFIX":
        result = IATProp(codes.infixTransducer(alphabet))
    elif fixed_type == "4" or fixed_type == "OUTFIX":
        result = codes.buildOutfixProperty(alphabet)
    elif fixed_type == "5" or fixed_type == "HYPERCODE":
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

    aut_str = re.sub(r'\r', "", aut_str)
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

    if count == 0:
        res = re.search(r'(.+?)\n([\s\S]+)', aut_str)
        if res:
            result['trajectory'] = res.group(1)
            result['aut_str'] = res.group(2)
            return result
    elif count == 1: # @DFA or @NFA, or Fixed type with regex
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
            else:
                result['aut_str'] = aut_str

        return result
    elif count == 2: # Two choices: Fixed Type, Transducer Without Type
        res = re.search(r'(@[\s\S]+)\n(@[\s\S]+)$', aut_str)

        if res.group(1).strip(' @') in ['PREFIX', 'SUFFIX', 'INFIX', 'OUTFIX', 'HYPERCODE', 'CODE']:
            result['fixed_type'] = res.group(1).strip(' @')
            result['aut_str'] = res.group(2)
        elif res.group(1).strip().lower().startswith('@transducer'):
            result['transducer'] = res.group(1)
            result['aut_str'] = res.group(2)
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


