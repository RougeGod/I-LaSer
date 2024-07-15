"""Common functions required by a lot of the FAdo backend. 
   This version of laser_shared is based off of the June 7, 2024 git commit
   and doesn't change very much compared to the web version, as much of this
   is back-end stuff
"""

from .FAdo.fio import readOneFromString
from .FAdo import reex
from .FAdo.codes import IATProp, buildTrajPropS, TrajProp
from .FAdo.fa import DFA, NFA
from .FAdo.common import FAdoError
from .FAdo.fl import FL
from lark import UnexpectedCharacters

from .util import list_to_string, long_to_base

FIXED = ['PREFIX', 'SUFFIX', 'INFIX', 'OUTFIX', 'HYPERCODE', 'CODE']

def construct_automaton(aut_str):
    """construct an automaton from a string"""
    aut_str = str(aut_str).strip()
    try:
        return readOneFromString(aut_str + "\n")
    except UnexpectedCharacters: #If the string is a regex
        try:
            return reex.str2regexp(aut_str).toNFA()
        except Exception: #anything goes wrong with the regex parsing 
            raise IncorrectFormat("could not build automaton")

def detect_automaton_type(aut_str):
    """construct an automaton from a string"""
    aut_str = str(aut_str).strip()
    try:
        readOneFromString(aut_str + "\n")
        return 'readOneFromString'
    except UnexpectedCharacters:
        try:
            reex.str2regexp(aut_str).toNFA()
            return 'str2regexp'
        except Exception:
            raise IncorrectFormat("could not read from string")

def construct_input_alt_prop(t_str, sigma, gen=False):
    """Construct an input-altering property"""

    t_str = t_str.strip()

    try:
        result = readOneFromString(t_str + "\n") #newline no longer added in handlers.py since it breaks regex parsing, add it in when needed
        if isinstance(result, (NFA, DFA)):
            if gen:
                return 'INALT'
            return IATProp(result)
        else:
            if gen:
                return 'TRAJECT'
            return TrajProp(result, sigma)
    except UnexpectedCharacters:
        try:
            if gen:
                return 'TRAJECT'
            return buildTrajPropS(t_str, sigma)
        except Exception:
            raise IncorrectFormat

def convertToCorrectType(value, default, desiredType=float): 
    '''Converts a value to any desired type, if this is not possible, supply a default'''
    try: 
        return desiredType(value)
    except (ValueError, TypeError):
        return default

def format_counter_example(witness, theta=False):
    """Using a witness object, output a string that shows an example where a property fails."""
    if isinstance(witness, tuple):
        if len(witness) == 3:
            return "Witness: The word '%s' results from '%s' and '%s'" % witness
        elif len(witness) == 2:
            if isinstance(witness[0], list):
                return "Witness: The word '%s' can be factored as %s and %s" \
                       % (''.join(witness[0]), str(witness[0]), str(witness[1]))
                    # % (witness[0][0]+witness[0][1], str(witness[0]), str(witness[1]) )
            else:
                return "Witness: The words '%s' and '%s' violate the property" % witness
        else:
            return "N/A"
    else:
        return "Witness: The word '%s' can be added to the language" % witness


def isLimitExceedForEditDist(automaton):
    """Decide if the size of automaton exceeds the limit.
       Number of transitions of automaton is denoted as N;
       If N*N*N*N exceeds 100000000, return False, else return True.
    """
    size = 0
    if isinstance(automaton, DFA):
        for key in automaton.delta.keys():
            for _ in automaton.delta[key]:
                size = size + 1
    elif isinstance(automaton, NFA):
        for key in automaton.delta.keys():
            for str_ in automaton.delta[key]:
                size = size + len(automaton.delta[key][str_])
    else:
        return size
    return size*size*len(automaton.Sigma) > 1000000


def is_subset(aut, transducer):
    '''Tests whether the automaton's alphabet is a subset of the transducer's
       Returns "trajectory" if the property is a trajectory, which will evaluate
       to true in a Boolean comparison '''
    if (type(transducer) == TrajProp):
        return "trajectory"
    else:
        return all([(letter in transducer.Sigma) for letter in aut.Sigma])
    
def limit_tran_prop(aut_delta, tran_delta, limit, lang_size=0):
    """Find if the calculation would be too long to do on the server"""
    size = lang_size
    if size == 0:
        for key in aut_delta:
            for key_2 in aut_delta[key]:
                if isinstance(aut_delta[key][key_2], int):
                    size += 1
                else:
                    size += len(aut_delta[key][key_2])

    size_2 = 0
    for key in tran_delta:
        for key2 in tran_delta[key]:
            size_2 += len(tran_delta[key][key2])

    return size*size*size_2 > limit

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
    aut = FL(words).trieFA().toNFA()
    return aut, words

class IncorrectFormat(Exception):
    pass
