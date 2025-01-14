"""Utility functions for unit testing"""

from os import path
import string

from app.transducer.laser_gen import generate_program_file
from app.transducer.views import get_code
from django.core.files.uploadedfile import SimpleUploadedFile

PROGRAM_PRELUDE = "import sys\n" + "sys.stdout = open('/dev/null', 'w')\nfrom FAdo.prax import *\nfrom FAdo.codes import *\nfrom FAdo.reex import *\nfrom FAdo.fio import *\nimport base64\nimport copy\n" #lines that go at the start of every program generated

def hamm_dist(str1, str2):
    """Return the hamming distance of two strings"""
    length = len(str1)
    if len(str1) != len(str2):
        return None
    dist = 0
    for i in range(length):
        if str1[i] != str2[i]:
            dist += 1
    return dist


def hamm_dist_list(list_):
    """returns the hamming distance of a list or strings"""
    min_dist = None
    for str1 in list_:
        for str2 in list_:
            if str1 == str2:
                continue
            dist = hamm_dist(str1, str2)
            if dist is not None:
                if min_dist is None:
                    min_dist = dist
                else:
                    min_dist = min(min_dist, dist)
    return min_dist

def create_file_dictionary(aut_file=None, trans_file=None, theta_file=None):
    '''get_response wants a dictionary of files, which need to be opened a certain way
       accepts filenames, returns a dictionary'''
    output = {}
    aut = openfile(aut_file) if aut_file is not None else None
    trans = openfile(trans_file) if trans_file is not None else None
    theta = openfile(theta_file) if theta_file is not None else None
    if aut is not None:
        output['automata_file'] = SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))
    if trans is not None:
        output['transducer_file'] = SimpleUploadedFile(trans.name, str.encode(trans.read(), encoding="utf-8"))
    if theta is not None:
        output['theta_file'] = SimpleUploadedFile(theta.name, str.encode(theta.read(), encoding="utf-8"))

    return output

def exec_program(post, files):
    generated = "".join(get_code(post, files, None, True, None))
    if type(generated) == dict: #if there is a form error message, the return type is a dict
        return generated
    prog = PROGRAM_PRELUDE + generated
    execvars = {}
    exec(prog, execvars, execvars) #may also raise an exception
    return execvars



def readfile(file_):
    """Return the contents of a file"""
    with open(path.join(path.dirname(__file__), file_)) as aut_file:
        aut_text = aut_file.read()
    return aut_text

def openfile(file_):
    """Return an opened file"""
    return open(path.join(path.dirname(__file__), file_))

def make_prog(lines, request):
    """makes program out of the given lines, omitting I/O statements, or replacing them with pass"""
    plines = generate_program_file(lines, None, request, test=True).split("\n")
    len_ = len(plines)
    prog = ''
    #remove all "input" and "print" statements so that generated programs can
    #be automatically tested
    for i in range(len_):
        if plines[i].find("input(") != -1:
            continue
        if plines[i].find("print(") != -1 and plines[i].find("answer)") != -1: #do print the answer, nothing more
            continue
        prog = prog+plines[i]+'\n'
    return prog
