
from FAdo.fio import readOneFromString
from FAdo.grail import importFromGrailString
from FAdo import reex
from FAdo.yappy_parser import YappyError
from FAdo.codes import IATProp, buildTrajPropS, TrajProp
from FAdo.fa import DFA, NFA

def constructAutomaton(autStr):
    autStr.strip()
    autStr += "\n"
    try:
        return readOneFromString(autStr)
    except YappyError:
        try:
            return importFromGrailString(autStr)
        except YappyError:
            try:
                autStr.strip()
                return reex.str2regexp(autStr).toNFA()
            except Exception:
                raise IncorrectFormat()

def constructInAltProp(tStr, sigma):
    try:
        m = readOneFromString(tStr)
        if type(m) is NFA or type(m) is DFA:
            return TrajProp(m, sigma)
        else:
            return IATProp(m)
    except YappyError:
        try:
            return buildTrajPropS(tStr, sigma)
        except Exception:
            raise IncorrectFormat

def formatCounterExample(witness):
    def concatL(lt):
        w = ''
        for s in lt:
            if not s == '@epsilon':
                w = w + s
        return w
    if type(witness) is tuple:
        if len(witness) == 3:
            return "Witness: The word '%s' results from '%s' and '%s'" % witness
        elif len(witness) == 2:
            if type(witness[0]) is list:
                return "Witness: The word '%s' can be factored as %s and %s" \
                       % (concatL(witness[0]), str(witness[0]), str(witness[1]))
                    # % (witness[0][0]+witness[0][1], str(witness[0]), str(witness[1]) )
            else:
                return "Witness: The words '%s' and '%s' violate the property" % witness
        else:
            return "N/A"
    else:
        return "Witness: The word '%s' can be added to the language" % witness


def isLimitExceedForEditDist(FA):
    """Decide if the size of FA exceeds the limit.
       Number of transitions of FA is denoted as N;
       If N*N*N*N exceeds 100000000, return False, else return True.
    """
    N = 0
    if type(FA) == DFA:
        for s in FA.delta.keys():
            for str in FA.delta[s]:
                N = N + 1
    elif type(FA) == NFA:
        for s in FA.delta.keys():
            for str in FA.delta[s]:
                N = N + len(FA.delta[s][str])
    else:
        return N
    if N*N*len(FA.Sigma) > 1000000:
        return True
    else:
        return False


def limitAutP(aut, limit):
    """
    """
    return len(aut.delta) >= limit


def limitTranP(autDelta, tranDelta, limit, langSize=0):
    """
    """
    N = langSize
    if N == 0:
        for s in autDelta:
            for c in autDelta[s]:
                if type(autDelta[s][c]) is int:
                    N += 1
                else:
                    N += len(autDelta[s][c])

    M = 0
    for s in tranDelta:
        for inp in tranDelta[s]:
            M += len(tranDelta[s][inp])

    if N*N*M > limit:
        return True
    else:
        return False


class IncorrectFormat(Exception):
    pass