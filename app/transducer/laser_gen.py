#pylint: disable=C0103
"""Laser interface for generating programs to compute the answer"""
# coding=utf-8
__author__ = 'rvr'
import os
import os.path as path
import platform
import base64
from string import Template
from django.conf import settings

ZIP_PROG = "zip"
UNZIP_PROG = "unzip"

BUILD_NAME = {"CODE": ("buildUDCodeProperty", ["ssigma"], 1),
              "EDITDIST": ("editDistanceW", ["a"], 0),
              "ERRCORR": ("buildErrorCorrectPropS", ["t"], 1),
              "ERRDET": ("buildErrorDetectPropS", ["t"], 1),
              "EXPDENSITY": ("exponentialDensityP", ["a"], 0),
              "HYPERCODE": ("buildHypercodeProperty", ["ssigma"], 1),
              "INALT": ("buildIATPropS", ["t"], 1),
              "INFIX": ("buildInfixProperty", ["ssigma"], 1),
              "INPRES": ("buildIPTPropS", ["t"], 1),
              "OUTFIX": ("buildOutfixProperty", ["ssigma"], 1),
              "PREFIX": ("buildPrefixProperty", ["ssigma"], 1),
              "SUFFIX": ("buildSuffixProperty", ["ssigma"], 1),
              "TRAJECT": ("buildTrajPropS", ["$strexp", "$sigma"], 1)}

TESTS = {"MAXP": "maximalP",
         "MAXW": "notMaximalW",
         "AMAX": "prax_maximal_nfa",
         "SATP": "satisfiesP",
         "SATW": "notSatisfiesW",
         "NONEMPTYW": "Aut.inIntersection(a).outIntersection(theta_aut).nonEmptyW",
         "MKCO": "makeCode"}

PARSERS_BEFORE = {"readOneFromString": "readOneFromString",
                  #"importFromGrailString": "importFromGrailString",
                  "str2regexp": "str2regexp"}

PARSERS_AFTER = {"readOneFromString": "",
                 # "importFromGrailString": "",
                  "str2regexp": ".toNFA()"}

#for running unittest
#PATH='/Users/Stavros/Dropbox/Documents/\
# my_documents/RESEARCH/myHQP/abisola/laser_update/laser/media/'
#PATH = '/var/www/project/media/'

#for running the server, it's beautiful
PATH = settings.MEDIA_ROOT

FADO_ZIP = path.join(PATH, "FAdo.zip")

def stand_alone(name, lines, request=None):
    """Create the standalone python files"""
    name = path.join(PATH, name)
    os.system("rm -rf %s" % name)
    os.mkdir(name)
    os.system("rm -f %s.zip" % name)
    os.chdir(name)
    os.system("%s %s" % (UNZIP_PROG, FADO_ZIP))
    generate_program_file(lines, "__main__.py", request)
    os.system("zip -r %s.zip *" % name)
    os.chdir("..")
    os.system("rm -r %s" % name)
    #pylint: disable=w1401
    os.system("find %s -regextype sed -regex '.*[0-9]\{13\}.zip' \
    -mtime +1 -exec rm -rf {} \;" % PATH)

def generate_program_file(lines, name=None, request=None):
    """
    Generation of the stand alone program
    :param list lines: list of the commands to include
    :param str name: name of the file
    :param str request: the description of the request for which to generate program
    :rtype: str
    """
    prog = the_prologue(request)
    for line in lines:
        prog += line + "\n"
    prog += the_epilogue()
    if name is not None:
        file_ = open(name, "w")
        file_.write(prog)
        file_.close()
    return prog

def the_prologue(request=None):
    """
    Returns the import statements for the program
    :param str request: the description of the request for which to generate program
    :rtype: str"""
    pro = """try:
    from FAdo.reex import *
    from FAdo.codes import *
    from FAdo.fio import *
    from FAdo.prax import *
    import base64
    import copy
except:
    print("Error with imports. Program will now exit.")
    exit()

"""
    if request is not None:
        pro += "print(\"\\nREQUEST:\\n" + request + "\")\n"
    pro += "print(\"\\nANSWER:\\n\"),\n"
    return pro

def the_epilogue():
    """
    :rtype: str"""
    return "input('\\nPress <enter> to quit.')\n"

def theta_helper_methods(theta_str, list_):
    """Add the helper methods for theta-transducer properties."""
    list_.append("""
def parse_theta_str(theta_str):
    match = re.search(r'^@THETA *\\n(([\\w\\d] +[\\w\\d]\\s*)+)', theta_str, re.IGNORECASE)

    swaps = match.group(1)

    result = {}
    for swap in swaps.splitlines():
        tmp = swap.split(' ')
        result[tmp[0]] = tmp[1]

    for key in result.keys():
        result[result[key]] = key

    return result""")

    list_.append("""
def apply_theta_antimorphism(aut, theta):
    new_aut = copy.deepcopy(aut.toNFA())

    newdelta = {}

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
""")

    list_.extend([
        "tx = %s" % base64.b64encode(theta_str.encode(encoding="utf-8")),
        "tt = parse_theta_str(base64.b64decode(tx).decode(encoding='utf-8')",
        "theta_aut = apply_theta_antimorphism(a, tt)"
    ])


def program_lines(
        ptype, test=None, aut_str=None, aut_type="readOneFromString",
        strexp=None, sigma=None, t_str=None,
        s_num=None, l_num=None, n_num=None,
        theta_str=None, dirichletT=None, epsi=None, displacement=None
    ):
    "Generates the program"

    def expand(string):
        """Expand a given string"""
        s_1 = Template(string)
        return s_1.substitute(strexp=strexp, sigma=sigma)

    list_ = list()
    if test == 'MKCO':
        list_.append("s_num = int(\"%s\")\n" % s_num)
        list_.append("l_num = int(\"%s\")\n" % l_num)
        list_.append("n_num = int(\"%s\")\n" % n_num)
        if BUILD_NAME[ptype][2] == 1:
            string = ''
            if t_str:
                list_.append("tx = %s\n" % base64.b64encode(t_str.encode(encoding="utf-8")))
                list_.append("t = str(base64.b64decode(tx).decode(encoding='utf-8'))\n")
            else:
                string += "alp = set()\nfor i in range(int(s_num)):\n    alp.add(str(i))\n"
                string += "ssigma = alp\n"
            string += "p = " + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                if s_1 == "$strexp":
                    string += "t, "
                else:
                    string += "%s," % expand(s_1)
            string = string[:-1] + ")\n"
            list_.extend([string,
                          'a, answer = p.%s(n_num, l_num, s_num)\n' % TESTS[test],
                          'print(\nfor w in answer:\n    print w\n)'])
        else:  # this is probably not needed
            string = "print(" + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                string += "%s," % expand(s_1)
            string = string[:-1] + "))\n"
            list_.append(string)
        return list_
    else:

        if aut_str and not aut_str.endswith('\n'):
            aut_str = aut_str + '\n'

        list_.append("ax = %s\n" % base64.b64encode(aut_str.encode(encoding='utf-8')))

        list_.append("a = %s(str(base64.b64decode(ax).decode(encoding='utf-8').strip()+%s))%s\n" % (PARSERS_BEFORE[aut_type], "\"\\n\"" if PARSERS_BEFORE[aut_type] == "readOneFromString" else "\"\"", PARSERS_AFTER[aut_type])) #regular expression parsing needs no newline, but readOneFromString requires a newline at the end of the file, so add in a literal "\n" if we're reading an automaton from string 
    
        if (test == "AMAX"):
            if dirichletT is None: 
                dirichletT = 2.001
            if epsi is None: 
                epsi = 0.01
            if displacement is None:
                displacement = 1

        if theta_str:
            theta_helper_methods(theta_str, list_)

        if BUILD_NAME[ptype][2] == 1:
            if t_str:
                list_.extend(["tx = \"%s\"\n" % base64.b64encode(t_str.encode(encoding='utf-8')),
                              "t = str(base64.b64decode(tx).decode(encoding='utf-8'))\n"])
            string = "ssigma = a.Sigma\n"
            string += "p = " + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                if s_1 == "$strexp":
                    string += "t, "
                else:
                    string += "%s," % expand(s_1)
            string = string[:-1] + ")\n"
            
            if (test == "AMAX"): #approximate maximality code has very different syntax so gets a special case
                ans = "answer = %s(GenWordDis(Dirichlet(t=%s, d=%s), ssigma, %s), a, p)" % (TESTS["AMAX"], dirichletT, displacement, epsi)
            else: 
                ans = "answer = p.%s(%s)\n" % (TESTS[test], '' if theta_str else 'a')
            

            list_.extend([string, ans, "print(answer) \n"])
        else:
            string = "print(" + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                string += "%s," % expand(s_1)
            string = string[:-1] + "))\n"
            list_.append(string)
        return list_

def gen_program(file_name, prop_type, test_name=None, aut_str=None, aut_type="readOneFromString",
                t_str=None, sigma=None, regexp=None, request=None, test_mode=None, s_num=None,
                l_num=None, n_num=None, theta_str=None, dirichletT=None, epsi=None, displacement=None):
    """
    :param str file_name: name of the generated program (.zip)
    :param str prop_type: key of the property name
    :param str test_name: key for the test inside prop (if that is the case)
    :param str aut_str: string description of the automaton
    :param str t_str: string description of the transducer (if needed)
    :param set sigma:  the alphabet (if needed)
    :param str regexp: the regular expression for trajectories
    :param str request: description of request for which to generate program
    :param bool test_mode: whether the method is used for testing
    :param float dirichletT: the T parameter to the Dirichlet Distribution
    :param float epsi; A value between 0 and 1
    :param displacement An integer value used for approximate maximality
    :rtype: list
    """

    lines = program_lines(prop_type, test_name, aut_str,
                          aut_type, regexp, sigma, t_str,
                          s_num, l_num, n_num,
                          theta_str, dirichletT, epsi, displacement)

    if (test_mode is None) or (not test_mode):
        stand_alone(file_name, lines, request)
    return lines
