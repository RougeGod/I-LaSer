"""Interfaces for the website to communicate with the FAdo backend"""
from FAdo.fio import readOneFromString
from FAdo.grail import importFromGrailString
from FAdo import reex
from FAdo.yappy_parser import YappyError
from FAdo.codes import IATProp, buildTrajPropS, TrajProp
from FAdo.fa import DFA, NFA
import FAdo.fl as fl

from app.transducer.util import list_to_string, long_to_base

FIXED = ['PREFIX', 'SUFFIX', 'INFIX', 'OUTFIX', 'HYPERCODE', 'CODE']

def construct_automaton(aut_str):
    """construct an automaton from a string"""

    aut_str = str(aut_str)

    aut_str.strip()
    aut_str += "\n"
    try:
        return readOneFromString(aut_str)
    except (YappyError, IndexError):
        try:
            return importFromGrailString(aut_str)
        except YappyError:
            try:
                aut_str.strip()
                return reex.str2regexp(aut_str, no_table=0).toNFA()
            except Exception:
                raise IncorrectFormat()

def detect_automaton_type(aut_str):
    """construct an automaton from a string"""

    aut_str = str(aut_str)

    aut_str.strip()
    aut_str += "\n"
    try:
        readOneFromString(aut_str)

        return 'readOneFromString'
    except (YappyError, IndexError):
        try:
            importFromGrailString(aut_str)

            return 'importFromGrailString'
        except YappyError:
            try:
                aut_str.strip()
                reex.str2regexp(aut_str).toNFA()
                return 'str2regexp'
            except Exception:
                raise IncorrectFormat()

def construct_input_alt_prop(t_str, sigma, gen=False):
    """Construct an input-altering property"""

    t_str.strip()
    t_str += "\n"

    try:
        result = readOneFromString(t_str)
        if isinstance(result, (NFA, DFA)):
            if gen:
                return 'INALT'
            return IATProp(result)
        else:
            if gen:
                return 'TRAJECT'
            return TrajProp(result, sigma)
    except YappyError:
        try:
            if gen:
                return 'TRAJECT'
            return buildTrajPropS(t_str, sigma)
        except Exception:
            raise IncorrectFormat

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


def limit_aut_prop(aut, limit):
    """Does something with limits"""
    return len(aut.delta) >= limit


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

def limit_theta_prop(aut_delta, tran_delta, theta, limit, lang_size=0):
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

    size_3 = len(theta)

    return size*size*size_2*size*size_3 > limit


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
    aut = fl.FL(words).trieFA().toNFA()
    return aut, words

class IncorrectFormat(Exception):
    """IncorrectFormat error"""
    pass
