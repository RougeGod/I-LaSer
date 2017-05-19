"""Online mode unit tests"""

import os.path as path

from app.transducer.views import get_response
import FAdo.fl as fl

from django.test import TestCase


REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa']
TRAJ_NAMES = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IATRANSDUCER_NAMES = ['test_files/P-infix.fa', 'test_files/P-suffix.fa',
                      'test_files/P-transpose1.01.ia.fa']
IPTRANSDUCER_NAMES = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa',
                      'test_files/P-infix-ipt.fa', 'test_files/TR-del1.a.fa',
                      'test_files/TR-sub1.01.ip.fa', 'test_files/TR-sub2.01.ip.fa',
                      'test_files/P-transpose1.01.ip.fa']
COMBINED_NAMES = ['test_files/combined/test1.fa', 'test_files/combined/test2.fa',
                  'test_files/combined/test3.fa', 'test_files/combined/test4.fa',
                  'test_files/combined/test5.fa', 'test_files/combined/test6.fa']

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

#pylint:disable=C0111,C0301,C0103
class MyTestCase(TestCase):
    """Holds test cases for the website"""

    def test_hamm_dist(self):
        self.assertEquals(hamm_dist('000', '101'), 2)
        self.assertEquals(hamm_dist('00', '101'), None)
        self.assertEquals(hamm_dist('0011001100', '1111000011'), 6)
        self.assertEquals(hamm_dist_list(['000', '101']), 2)
        self.assertEquals(hamm_dist_list(['0011001100', '1111000011', '000', '101']), 2)

    def test_combined_files(self):
        def readfile(file_):
            aut_file = open(path.join(path.dirname(__file__), file_))
            aut_text = aut_file.read()
            aut_file.close()
            return aut_text

        files = {}

        aut_text = readfile(COMBINED_NAMES[0])
        post = {'que': '1', 'prv': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

        aut_text = readfile(COMBINED_NAMES[1])
        post = {'que': '1', 'prv': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

        aut_text = readfile(COMBINED_NAMES[2])
        post = {'que': '1', 'prv': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

        aut_text = readfile(COMBINED_NAMES[3])
        post = {'que': '1', 'prv': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))

        aut_text = readfile(COMBINED_NAMES[4])
        post = {'que': '1', 'prv': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

    def test_TRAJsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[3]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))

    def test_TRAJTsatYES(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

    def test_IATsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))
        aut = open(path.join(path.dirname(__file__), REGS[3]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))

    def test_IATsatYES(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

    def test_IPTsatNO(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))
        aut = open(path.join(path.dirname(__file__), REGS[3]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))
        aut = open(path.join(path.dirname(__file__), REGS[1]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)

    def test_IPTsatYES(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), REGS[4]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))
        aut = open(path.join(path.dirname(__file__), REGS[5]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('YES'))

    def test_CORRsatNO(self):
        post = {'que': '1', 'prv': '4'}
        aut = open(path.join(path.dirname(__file__), REGS[9]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith('NO'))
        aut.close()
        t_file.close()
        # next test program generation
        # aut = open(path.join(path.dirname(__file__), REGS[9]))
        # t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[1]))
        # files = {'automata_file': aut, 'transducer_file': t_file}
        # lines = getCode(post, files, False, True)
        # should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)\n') and \
        #             (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        # self.assertTrue(should_be)

    def test_TRAJmaxNO(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[1]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[5]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

    def test_TRAJTmaxYES(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        t_file = open(path.join(path.dirname(__file__), TRAJ_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

    def test_IATmaxNO(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[1]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[5]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        t_file = open(path.join(path.dirname(__file__), IATRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

    def test_IPTmaxNO(self):
        post = {'que': '2', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), REGS[5]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[2]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()
        # next test program generation
        # aut = open(path.join(path.dirname(__file__), REGS[0]))
        # t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[0]))
        # files = {'automata_file': aut, 'transducer_file': t_file}
        # lines = getCode(post, files, False, True)
        # should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)\n') and \
        #             (lines[LN_ANS] == 'print p.notMaximalW(a)\n')
        # self.assertTrue(should_be)

    def test_IPTmaxYES(self):
        post = {'que': '2', 'prv': '3'}
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[2]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[6]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

    def test_CORRmaxNO(self):
        post = {'que': '2', 'prv': '4'}
        aut = open(path.join(path.dirname(__file__), REGS[7]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[1]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[0]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

    def test_CORRmaxYES(self):
        post = {'que': '2', 'prv': '4'}
        aut = open(path.join(path.dirname(__file__), REGS[8]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[3]))
        files = {'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '1'}  # PREFIX
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
        post = {'que': '1', 'prv': '1', 'fixed_type': '3'}  # INFIX
        aut = open(path.join(path.dirname(__file__), REGS[3]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

    def test_FIXED_IATsatYES(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'que': '1', 'prv': '1', 'fixed_type': '4'}  # OUTFIX
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")

    def test_FIXED_IATmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(path.join(path.dirname(__file__), REGS[1]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'que': '2', 'prv': '1', 'fixed_type': '5'}  # HYPERCODE
        aut = open(path.join(path.dirname(__file__), REGS[7]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")

    def test_FIXED_IATmaxYES(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'que': '2', 'prv': '1', 'fixed_type': '1'}  # PREFIX
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")

    def test_FIXED_CODEsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), REGS[6]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
        post = {'que': '1', 'prv': '1', 'fixed_type': '3'}
        aut = open(path.join(path.dirname(__file__), REGS[3]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

    def test_FIXED_CODEsatYES(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'que': '1', 'prv': '1', 'fixed_type': '4'}
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")

    def test_FIXED_CODEmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), REGS[1]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'que': '2', 'prv': '1', 'fixed_type': '3'}
        aut = open(path.join(path.dirname(__file__), REGS[5]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")

    def test_FIXED_CODEmaxYES(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(path.join(path.dirname(__file__), REGS[0]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'que': '2', 'prv': '1', 'fixed_type': '4'}
        aut = open(path.join(path.dirname(__file__), REGS[2]))
        files = {'automata_file': aut}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")

    def test_IPTconstr(self):
        post = {'que': '3', 'prv': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = open(path.join(path.dirname(__file__), REGS[4]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[4]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        #print 'hdist = ', hamm_dist_list(result['witness'])
        self.assertTrue(hamm_dist_list(result['witness']) > 1)
        post = {'que': '3', 'prv': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = open(path.join(path.dirname(__file__), REGS[4]))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[5]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(hamm_dist_list(witness) > 2)
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[6]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[5]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = open(path.join(path.dirname(__file__), IPTRANSDUCER_NAMES[5]))
        files = {'transducer_file': t_file} #{'automata_file': aut, 'transducer_file': t_file}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
