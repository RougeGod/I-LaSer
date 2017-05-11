"""Interfaces for the website to communicate with the FAdo backend"""
from FAdo.fio import readOneFromString
from FAdo.grail import importFromGrailString
from FAdo import reex
from FAdo.yappy_parser import YappyError
from FAdo.codes import IATProp, buildTrajPropS, TrajProp
from FAdo.fa import DFA, NFA

FIXED = ['PREFIX', 'SUFFIX', 'INFIX', 'OUTFIX', 'HYPERCODE', 'CODE']

def construct_automaton(aut_str):
    """construct an automaton from a string"""
    aut_str.strip()
    aut_str += "\n"
    try:
        return readOneFromString(aut_str)
    except YappyError:
        try:
            return importFromGrailString(aut_str)
        except YappyError:
            try:
                aut_str.strip()
                return reex.str2regexp(aut_str).toNFA()
            except Exception:
                raise IncorrectFormat()

def constructInAltProp(t_str, sigma):
    """Construct an input-altering property"""
    try:
        result = readOneFromString(t_str)
        if isinstance(result, NFA) or isinstance(result, DFA):
            return TrajProp(result, sigma)
        else:
            return IATProp(result)
    except YappyError:
        try:
            return buildTrajPropS(t_str, sigma)
        except Exception:
            raise IncorrectFormat

def formatCounterExample(witness):
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


def limitAutP(aut, limit):
    """Does something with limits"""
    return len(aut.delta) >= limit


def limitTranP(aut_delta, tran_delta, limit, lang_size=0):
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


class IncorrectFormat(Exception):
    """IncorrectFormat error"""
    pass
