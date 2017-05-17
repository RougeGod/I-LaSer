from app.transducer.views import * #getCode, get_response
#from transducer.ILaser_gen import *
from FAdo.reex import *
from FAdo.fio import readOneFromFile
from FAdo.codes import buildIATPropF
import FAdo.fl as fl

from django.test import TestCase

import os.path as path

regs = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa']
TrajNames = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IATnames  = ['test_files/P-infix.fa', 'test_files/P-suffix.fa', 'test_files/P-transpose1.01.ia.fa']
IPTnames  = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa', 'test_files/P-infix-ipt.fa',
             'test_files/TR-del1.a.fa', 'test_files/TR-sub1.01.ip.fa', 'test_files/TR-sub2.01.ip.fa',
             'test_files/P-transpose1.01.ip.fa']


def hamm_dist(x,y):
    n = len(x)
    if n != len(y): return None
    dist = 0
    for i in range(n):
        if (x[i] != y[i]):  dist += 1
    return dist


def hamm_dist_list(L):
    min_dist = None
    for x in L:
        for y in L:
            if (x==y): continue
            dxy = hamm_dist(x, y)
            if dxy is not None:
                if min_dist is None: min_dist = dxy
                else:    min_dist = min(min_dist, dxy)
    return min_dist

#pylint:disable=C0111,C0301
class MyTestCase(TestCase):
    """Holds test cases for the website"""

    def test_hamm_dist(self):
        self.assertEquals(hamm_dist('000', '101'), 2)
        self.assertEquals(hamm_dist('00', '101'), None)
        self.assertEquals(hamm_dist('0011001100', '1111000011'), 6)
        self.assertEquals(hamm_dist_list(['000', '101']), 2)
        self.assertEquals(hamm_dist_list(['0011001100', '1111000011', '000', '101']), 2)

    def test_TRAJsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[3]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")

    def test_TRAJTsatYES(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = open(path.join(path.dirname(__file__), regs[2]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")

    def test_IATsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), IATnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(path.join(path.dirname(__file__), regs[3]))
        t_file = open(path.join(path.dirname(__file__), IATnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")

    def test_IATsatYES(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), IATnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = open(path.join(path.dirname(__file__), regs[2]))
        t_file = open(path.join(path.dirname(__file__), IATnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")

    def test_IPTsatNO(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), regs[2]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(path.join(path.dirname(__file__), regs[3]))
        t_file = open(path.join(path.dirname(__file__), IATnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(path.join(path.dirname(__file__), regs[1]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)

    def test_IPTsatYES(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), regs[4]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = open(path.join(path.dirname(__file__), regs[5]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")

    def test_CORRsatNO(self):
        post = {'que': '1', 'prv': '4'}
        aut = open(path.join(path.dirname(__file__), regs[9]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut.close()
        t_file.close()
        # next test program generation
        # aut = open(path.join(path.dirname(__file__), regs[9]))
        # t_file = open(path.join(path.dirname(__file__), IPTnames[1]))
        # files = {'automata_file': aut, 'transducer_file': t_file}
        # lines = getCode(post, files, False, True)
        # should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)\n') and \
        #             (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        # self.assertTrue(should_be)

    def test_TRAJmaxNO(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[1]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[5]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

    def test_TRAJTmaxYES(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[2]))
        t_file = open(path.join(path.dirname(__file__), TrajNames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

    def test_IATmaxNO(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[1]))
        t_file = open(path.join(path.dirname(__file__), IATnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[5]))
        t_file = open(path.join(path.dirname(__file__), IATnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), IATnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[2]))
        t_file = open(path.join(path.dirname(__file__), IATnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

    def test_IPTmaxNO(self):
        post = {'que': '2', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), regs[5]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[2]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()
        # next test program generation
        # aut = open(path.join(path.dirname(__file__), regs[0]))
        # t_file = open(path.join(path.dirname(__file__), IPTnames[0]))
        # files = {'automata_file': aut, 'transducer_file': t_file}
        # lines = getCode(post, files, False, True)
        # should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)\n') and \
        #             (lines[LN_ANS] == 'print p.notMaximalW(a)\n')
        # self.assertTrue(should_be)

    def test_IPTmaxYES(self):
        post = {'que': '2', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), regs[2]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[2]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[6]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

    def test_CORRmaxNO(self):
        post = {'que': '2', 'prv': '4'}
        aut = open(path.join(path.dirname(__file__), regs[7]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), regs[0]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

    def test_CORRmaxYES(self):
        post = {'que': '2', 'prv': '4'}
        aut = open(path.join(path.dirname(__file__), regs[8]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[3]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '1'}  # PREFIX
        aut = open(path.join(path.dirname(__file__), regs[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
        post = {'que': '1', 'prv': '1', 'fixed_type': '3'}  # INFIX
        aut = open(path.join(path.dirname(__file__), regs[3]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

    def test_FIXED_IATsatYES(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(path.join(path.dirname(__file__), regs[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'que': '1', 'prv': '1', 'fixed_type': '4'}  # OUTFIX
        aut = open(path.join(path.dirname(__file__), regs[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")

    def test_FIXED_IATmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(path.join(path.dirname(__file__), regs[1]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'que': '2', 'prv': '1', 'fixed_type': '5'}  # HYPERCODE
        aut = open(path.join(path.dirname(__file__), regs[7]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")

    def test_FIXED_IATmaxYES(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(path.join(path.dirname(__file__), regs[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'que': '2', 'prv': '1', 'fixed_type': '1'}  # PREFIX
        aut = open(path.join(path.dirname(__file__), regs[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")

    def test_FIXED_CODEsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), regs[6])  )
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
        post = {'que': '1', 'prv': '1', 'fixed_type': '3'}
        aut = open(path.join(path.dirname(__file__), regs[3]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

    def test_FIXED_CODEsatYES(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'que': '1', 'prv': '1', 'fixed_type': '4'}
        aut = open(path.join(path.dirname(__file__), regs[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")

    def test_FIXED_CODEmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), regs[1])  )
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'que': '2', 'prv': '1', 'fixed_type': '3'}
        aut = open(path.join(path.dirname(__file__), regs[5]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")

    def test_FIXED_CODEmaxYES(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), regs[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'que': '2', 'prv': '1', 'fixed_type': '4'}
        aut = open(path.join(path.dirname(__file__), regs[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")

    def test_IPTconstr(self):
        post = {'que': '3', 'prv': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = open(path.join(path.dirname(__file__), regs[4]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[4]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        #print 'hdist = ', hamm_dist_list(result['witness'])
        self.assertTrue(hamm_dist_list(result['witness']) > 1)
        post = {'que': '3', 'prv': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = open(path.join(path.dirname(__file__), regs[4]))
        t_file = open(path.join(path.dirname(__file__), IPTnames[5]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(hamm_dist_list(witness) > 2)
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = open(path.join(path.dirname(__file__), IPTnames[6]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = open(path.join(path.dirname(__file__), IPTnames[5]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = open(path.join(path.dirname(__file__), IPTnames[5]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
