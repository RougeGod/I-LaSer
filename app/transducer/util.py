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

def get_fixed_type(aut_str):
    """
    Gets the fixed type of the automaton string, if it's there.
    """
    if aut_str.count('@') > 1:
        res = re.search(r'(.+?)\n([\s\S]+)$', re.sub(r'\r', "", aut_str))
        fixed_type = res.group(1).strip(' @')

        aut_str = res.group(2)

        return aut_str, fixed_type
    return aut_str, None
