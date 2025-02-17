"""Laser Unit Tests"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

import FAdo.fl as fl

from app.transducer.views import get_response
from app.transducer.laser_gen import program_lines
from app.testing.test_util import hamm_dist, hamm_dist_list, openfile, make_prog, create_file_dictionary
from app.testing.test_data import a_ab_bb, a_bstar_a, str1sd, t1ts, t1t01s


TEST_GEN = 1   # whether to test program generation; set it to 1 for YES
if TEST_GEN:
    LN_OMIT = 3  # number of lines to omit from the end of generated program

REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa']
TRAJ_NAMES = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IA_TRANSDUCER_NAMES = ['test_files/P-infix.fa', 'test_files/P-suffix.fa',
                       'test_files/P-transpose1.01.ia.fa']
IP_TRANSDUCER_NAMES = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa',
                       'test_files/P-infix-ipt.fa', 'test_files/TR-del1.a.fa',
                       'test_files/TR-sub1.01.ip.fa', 'test_files/TR-sub2.01.ip.fa',
                       'test_files/P-transpose1.01.ip.fa']


#pylint:disable=C0301,W0122,C0111,C0103,R0904
class MyTestCase(TestCase):
    def test_hamm_dist(self):
        self.assertEquals(hamm_dist('000', '101'), 2)
        self.assertEquals(hamm_dist('00', '101'), None)
        self.assertEquals(hamm_dist('0011001100', '1111000011'), 6)
        self.assertEquals(hamm_dist_list(['000', '101']), 2)
        self.assertEquals(hamm_dist_list(['0011001100', '1111000011', '000', '101']), 2)


    def test_TRAJsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[3], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")


    def test_TRAJTsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_IATsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        files = create_file_dictionary(aut_file=REGS[3], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result['result'], "NO, the language does not satisfy the property")
        if not TEST_GEN:
            return
        lines = program_lines(ptype="INALT", test="SATW", aut_str=a_ab_bb,
                              strexp=None, sigma=None, t_str=str1sd)
        prog = make_prog(lines, 'decide satisfaction')
        execReturn = {}
        exec(prog, globals(), execReturn)
        answer = execReturn["answer"]
        self.assertEquals(set(answer), set(['ab', 'bb']))


    def test_IATsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        files = create_file_dictionary(aut_file=REGS[2], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_IPTsatNO(self):
        post = {'question': '1', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[2], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        files = create_file_dictionary(aut_file=REGS[3], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        files = create_file_dictionary(aut_file=REGS[1], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)


    def test_IPTsatYES(self):
        post = {'question': '1', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[4], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        files = create_file_dictionary(aut_file=REGS[5], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        if not TEST_GEN:
            return
        lines = program_lines(ptype="INPRES", test="SATW", aut_str=a_bstar_a,
                              strexp=None, sigma=None, t_str=t1ts)
        prog = make_prog(lines, 'decide satisfaction.')
        prog_vars = {}
        exec(prog, prog_vars, prog_vars)   # prog computes answer
        self.assertEquals(prog_vars.get('answer'), (None, None))

    def test_CORRsatNO(self):
        post = {'question': '1', 'property_type': '4'}
        files = create_file_dictionary(aut_file=REGS[9], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")


    def test_TRAJmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_TRAJTmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_IATmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_IPTmaxNO(self):
        post = {'question': '2', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[5], trans_file=IP_TRANSDUCER_NAMES[2])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_IPTmaxYES(self):
        post = {'question': '2', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[2], trans_file=IP_TRANSDUCER_NAMES[2])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[6], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_CORRmaxNO(self):
        post = {'question': '2', 'property_type': '4'}
        files = create_file_dictionary(aut_file=REGS[7], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_CORRmaxYES(self):
        post = {'question': '2', 'property_type': '4'}
        files = create_file_dictionary(aut_file=REGS[8], trans_file=IP_TRANSDUCER_NAMES[3])
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}  # INFIX
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

        post = {"question": "1", "property_type": "1", "fixed_type": "3"} # BIFIX
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")


    def test_FIXED_IATsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '5'}  # OUTFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '3'}  # OUTFIX
        files = create_file_dictionary(aut_file=REGS[7])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")


    def test_FIXED_IATmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[1])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '7'}  # HYPERCODE
        files = create_file_dictionary(aut_file=REGS[7])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")


    def test_FIXED_IATmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")


    def test_FIXED_CODEsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'} # CODE
        files = create_file_dictionary(aut_file=REGS[6])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'} # INFIX
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")


    def test_FIXED_CODEsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'} #CODE
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '5'} #OUTFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")


    def test_FIXED_CODEmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=REGS[1])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '4'}
        files = create_file_dictionary(aut_file=REGS[5])
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")


    def test_FIXED_CODEmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '5'} #OUTFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")


    def test_IPTconstr(self):
        post = {'question': '3', 'property_type': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        files = create_file_dictionary(trans_file=IP_TRANSDUCER_NAMES[4])
        result = get_response(post, files, False)
        self.assertTrue(hamm_dist_list(result['witness']) > 1)

        post = {'question': '3', 'property_type': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        files = create_file_dictionary(trans_file=IP_TRANSDUCER_NAMES[5])
        result = get_response(post, files, False)
        W = result['witness']
        self.assertTrue(hamm_dist_list(W) > 2)
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))

        files = create_file_dictionary(trans_file=IP_TRANSDUCER_NAMES[6])
        result = get_response(post, files, False)
        W = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))

        files = create_file_dictionary(trans_file=IP_TRANSDUCER_NAMES[5])
        result = get_response(post, files, False)
        W = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))

        files = create_file_dictionary(trans_file=IP_TRANSDUCER_NAMES[5])
        result = get_response(post, files, False)
        W = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))
        if not TEST_GEN:
            return
        lines = program_lines(ptype="INPRES", test="MKCO", aut_str=None,
                              strexp=None, sigma=None, t_str=t1t01s, s_num=2, l_num=8, n_num=5,testing=True)
        prog = make_prog(lines, 'generate code.')
        prog_vars = {}
        exec(prog, prog_vars)   # prog computes answer and p
        self.assertTrue(prog_vars.get('p').satisfiesP(fl.FL(prog_vars.get('answer')).trieFA().toNFA()))
