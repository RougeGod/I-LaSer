"""Utility functions for unit testing"""

from os import path
import string

from app.transducer.laser_gen import generate_program

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

def readfile(file_):
    """Return the contents of a file"""
    aut_file = open(path.join(path.dirname(__file__), file_))
    aut_text = aut_file.read()
    aut_file.close()
    return aut_text

def openfile(file_):
    """Return an opened file"""
    return open(path.join(path.dirname(__file__), file_))

def make_prog(lines, request):
    """makes program out of the given lines, omitting I/O statements, or replacing them with pass"""
    plines = generate_program(lines, None, request).split("\n")
    len_ = len(plines)
    prog = ''
    for i in range(len_):
        if string.find(plines[i], "raw_input") == 0:
            continue
        if string.find(plines[i], "print") == 0:
            continue
        if string.find(plines[i].strip(), "print") == 0:
            prog = prog + "    pass"
        else:
            prog = prog+plines[i]+'\n'
    return prog