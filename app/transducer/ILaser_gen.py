#pylint: disable=C0103
"""Laser interface for generating programs to compute the answer"""
# coding=utf-8
__author__ = 'rvr'
import os
import os.path
import base64
from string import Template
from django.conf import settings

ZIP_PROG = "zip"
UNZIP_PROG = "unzip"

#for running unittest
#PATH='/Users/Stavros/Dropbox/Documents/my_documents/RESEARCH/myHQP/abisola/laser_update/laser/media/'
#PATH = '/var/www/project/media/'

#for running the server
PATH = settings.MEDIA_ROOT
FADO_ZIP = PATH + "FAdo.zip"

def stand_alone(name, lines, request=None):
    """Create the standalone python files"""
    name = PATH + name
    os.system("rm -rf %s" % name)
    os.mkdir(name)
    os.system("rm -f %s.zip" % name)
    os.chdir(name)
    os.system("%s -q %s" % (UNZIP_PROG, FADO_ZIP))
    generate_program(lines, "__main__.py", request)
    os.system("zip -r -q %s.zip *" % name)
    os.chdir("..")
    os.system("rm -r %s" % name)
    #pylint: disable=w1401
    os.system("find %s -regextype sed -regex '.*[0-9]\{13\}.zip' \
    -mtime +1 -exec rm -rf {} \;" % PATH)


def generate_program(lines, name=None, request=None):
    """Generation of the stand alone program

    :param list lines: list of the commands to include
    :param str name: name of the file
    :param str request: the description of the request for which to generate program
    :rtype: str"""
    prog = the_prologue(request)
    for line in lines:
        prog += line
    prog += the_epilogue()
    if name is not None:
        file_ = open(name, "w")
        file_.write(prog)
        file_.close()
    return prog


def the_prologue(request=None):
    """
    :param str request: the description of the request for which to generate program
    :rtype: str"""
    pro = "try:\n" \
          "    from FAdo.reex import *\n" \
          "    from FAdo.codes import *\n" \
          "    from FAdo.fio import *\n" \
          "    import base64\n" \
          "except:\n" \
          "    exit()\n"
    if request is not None:
        pro += "print \"\\nREQUEST:\\n" + request + "\"\n"
    pro += "print \"\\nANSWER:\\n\",\n"
    return pro


def the_epilogue():
    """
    :rtype: str"""
    return "raw_input('\\nPress <enter> to quit.')\n"


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
         "SATP": "satisfiesP",
         "SATW": "notSatisfiesW",
         "MKCO": "makeCode"}


def program(
        ptype, test=None, aname=None,
        strexp=None, sigma=None, tname=None,
        s_num=None, l_num=None, n_num=None
    ):
    """Generates the program"""

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
            if tname:
                list_.append("tx = \"%s\"\n" % base64.b64encode(tname))
                list_.append("t = base64.b64decode(tx)\n")
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
            list_.append(string)
            list_.append("a, answer = p.%s(n_num, l_num, s_num)\n" % TESTS[test])
            list_.append("print\nfor w in answer:\n    print w\n")
        else:  # this is probably not needed
            string = "print " + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                string += "%s," % expand(s_1)
            string = string[:-1] + ")\n"
            list_.append(string)
        return list_
    else:
        list_.append("ax = \"%s\"\n" % base64.b64encode(aname))
        list_.append("a = readOneFromString(base64.b64decode(ax))\n")
        if BUILD_NAME[ptype][2] == 1:
            if tname:
                list_.append("tx = \"%s\"\n" % base64.b64encode(tname))
                list_.append("t = base64.b64decode(tx)\n")
            string = "ssigma = a.Sigma\n"
            string += "p = " + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                if s_1 == "$strexp":
                    string += "t, "
                else:
                    string += "%s," % expand(s_1)
            string = string[:-1] + ")\n"
            list_.append(string)
            #l.append("print p.%s(a)\n" % TESTS[test])  # = the original line
            list_.append("answer = p.%s(a)\n" % TESTS[test])
            list_.append("print answer\n")
        else:
            string = "print " + BUILD_NAME[ptype][0] + "("
            for s_1 in BUILD_NAME[ptype][1]:
                string += "%s," % expand(s_1)
            string = string[:-1] + ")\n"
            list_.append(string)
        return list_

def gen_program(file_name, prop_type, test_name=None, aut_name=None, trans_name=None, sigma=None,
                regexp=None, request=None, test_mode=None, s_num=None, l_num=None, n_num=None):
    """
    :param str file_name: name of the generated program (.zip)
    :param str prop_type: key of the property name
    :param str test_name: key for the test inside prop (if that is the case)
    :param str aut_name: string description of the automaton
    :param str trans_name: string description of the transducer (if needed)
    :param set sigma:  the alphabet (if needed)
    :param str regexp: the regular expression for trajectories
    :param str request: description of request for which to generate program
    :param bool test_mode: whether the method is used for testing
    :rtype: list
    """
    lines = program(prop_type, test_name, aut_name, regexp, sigma, trans_name, s_num, l_num, n_num)
    if (test_mode is None) or (not test_mode):
        stand_alone(file_name, lines, request)
    return lines
