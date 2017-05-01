# coding=utf-8
__author__ = 'rvr'
import os
import marshal
from string import Template
import os.path
import base64
from django.conf import settings


zipProg = "zip"
unzipProg = "unzip"
FAdoZip = "FAdo.zip"


#for running unittest
#PATH = '/Users/Stavros/Dropbox/Documents/my_documents/RESEARCH/myHQP/abisola/laser_update/laser/media/'
#PATH = '/var/www/project/media/'

#for running the server
PATH = settings.MEDIA_ROOT

FAdoZip = PATH + FAdoZip

def standAlone(name, lines, aname, tname, request=None):
    name = PATH + name
    os.system("rm -rf %s" % name)
    os.mkdir(name)
    os.system("rm -f %s.zip" % name)
    os.chdir(name)
    os.system("%s -q %s" % (unzipProg, FAdoZip ))
    generate_program(lines, "__main__.py", request)
    os.system("zip -r -q %s.zip *" % name)
    os.chdir("..")
    os.system("rm -r %s" % name)
    os.system("find %s -regextype sed -regex '.*[0-9]\{13\}.zip' -mtime +1 -exec rm -rf {} \;" % PATH)


def generate_program(lines, name=None, request=None):
    """ Generation of the stand alone program

    :param list lines: list of the commands to include
    :param str name: name of the file
    :param str request: the description of the request for which to generate program
    :rtype: str"""
    prog = the_prologue(request)
    for l in lines:
        prog += l
    prog += the_epilogue()
    if name is not None:
        f = open(name, "w")
        f.write(prog)
        f.close()
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


buildName = {"CODE": ("buildUDCodeProperty", ["ssigma"], 1),
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


tests = {"MAXP": "maximalP",
         "MAXW": "notMaximalW",
         "SATP": "satisfiesP",
         "SATW": "notSatisfiesW",
         "MKCO": "makeCode"}


def program(ptype, test=None, aname=None, strexp=None, sigma=None, tname=None, s_num=None, l_num=None, n_num=None):

    def expand(s):
        s1 = Template(s)
        return s1.substitute(strexp=strexp, sigma=sigma)

    if test == 'MKCO':
        l = list()
        l.append("s_num = int(\"%s\")\n" % s_num)
        l.append("l_num = int(\"%s\")\n" % l_num)
        l.append("n_num = int(\"%s\")\n" % n_num)
        if buildName[ptype][2] == 1:
            s = ''
            if tname:
                l.append("tx = \"%s\"\n" % base64.b64encode(tname))
                l.append("t = base64.b64decode(tx)\n")
            else:
                s += "alp = set()\nfor i in range(int(s_num)):\n    alp.add(str(i))\n"
                s += "ssigma = alp\n"
            s += "p = " + buildName[ptype][0] + "("
            for s1 in buildName[ptype][1]:
                if s1 == "$strexp":
                    s += "t, "
                else:
                    s += "%s," % expand(s1)
            s = s[:-1] + ")\n"
            l.append(s)
            l.append("a, answer = p.%s(n_num, l_num, s_num)\n" % tests[test])
            l.append("print\nfor w in answer:\n    print w\n")
        else:  # this is probably not needed
            s = "print " + buildName[ptype][0] + "("
            for s1 in buildName[ptype][1]:
                s += "%s," % expand(s1)
            s = s[:-1] + ")\n"
            l.append(s)
        return l
    else:
        l = list()
        l.append("ax = \"%s\"\n" % base64.b64encode(aname))
        l.append("a = readOneFromString(base64.b64decode(ax))\n")
        if buildName[ptype][2] == 1:
            if tname:
                l.append("tx = \"%s\"\n" % base64.b64encode(tname))
                l.append("t = base64.b64decode(tx)\n")
            s = "ssigma = a.Sigma\n"
            s += "p = " + buildName[ptype][0] + "("
            for s1 in buildName[ptype][1]:
                if s1 == "$strexp":
                    s += "t, "
                else:
                    s += "%s," % expand(s1)
            s = s[:-1] + ")\n"
            l.append(s)
            #l.append("print p.%s(a)\n" % tests[test])  # = the original line
            l.append("answer = p.%s(a)\n" % tests[test])
            l.append("print answer\n")
        else:
            s = "print " + buildName[ptype][0] + "("
            for s1 in buildName[ptype][1]:
                s += "%s," % expand(s1)
            s = s[:-1] + ")\n"
            l.append(s)
        return l


def fixString(s):
    a = ""
    for l in s:
        a += l[:-2] + "!"
    return a


def genProgram(fName, propType, tstName=None, autName=None, tName=None, sigma=None,
               regExp=None, request=None, testMode=None, s_num=None, l_num=None, n_num=None):
    """

    :param str fName: name of the generated program (.zip)
    :param str propType: key of the property name
    :param str tstName: key for the test inside prop (if that is the case)
    :param str autName: string description of the automaton
    :param str tName: string description of the transducer (if needed)
    :param set sigma:  the alphabet (if needed)
    :param str regExp: the regular expression for trajectories
    :param str request: description of request for which to generate program
    :param bool testMode: whether the method is used for testing
    :rtype: list"""
    lines = program(propType, tstName, autName, regExp, sigma, tName,  s_num, l_num, n_num)
    if (testMode is None) or (not testMode):
        standAlone(fName, lines, autName, tName, request)
    return lines

