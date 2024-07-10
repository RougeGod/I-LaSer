"""Online mode unit tests"""

from app.transducer.views import get_response, get_code
from app.transducer.util import parse_aut_str
from app.testing.test_util import hamm_dist, hamm_dist_list, readfile, openfile, create_file_dictionary
import FAdo.fl as fl

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

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
                  'test_files/combined/test5.fa', 'test_files/combined/test6.fa',
                  'test_files/combined/test7.fa', 'test_files/combined/test8.fa',
                  'test_files/combined/test9.fa', 'test_files/combined/test10.fa',
                  'test_files/combined/test11.fa', 'test_files/combined/test12.fa',
                  'test_files/combined/test13.fa', 'test_files/combined/test14.fa',
                  'test_files/combined/test15.fa', 'test_files/combined/test16.fa']

#pylint:disable=C0111,C0301,C0103
class MyTestCase(TestCase):
    """Holds test cases for the website"""
    def test_hamm_dist(self):
        self.assertEquals(hamm_dist('000', '101'), 2)
        self.assertEquals(hamm_dist('00', '101'), None)
        self.assertEquals(hamm_dist('0011001100', '1111000011'), 6)
        self.assertEquals(hamm_dist_list(['000', '101']), 2)
        self.assertEquals(hamm_dist_list(['0011001100', '1111000011', '000', '101']), 2)

    def test_mixed(self):
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '2', 'transducer_text1': t_text}
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        t_text = readfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '2', 'transducer_text1': t_text}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[0])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_text = readfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_TRAJsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[3], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_TRAJTsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_IATsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IATRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        files = create_file_dictionary(aut_file=REGS[3], trans_file=IATRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_IATsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IATRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        files = create_file_dictionary(aut_file=REGS[2], trans_file=IATRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_IPTsatNO(self):
        post = {'question': '1', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[2], trans_file=IPTRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        files = create_file_dictionary(aut_file=REGS[3], trans_file=IATRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        files = create_file_dictionary(aut_file=REGS[1], trans_file=IPTRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'fail').startswith("NO"))

    def test_IPTsatYES(self):
        post = {'question': '1', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[4], trans_file=IPTRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        files = create_file_dictionary(aut_file=REGS[5], trans_file=IPTRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_CORRsatNO(self):
        post = {'question': '1', 'property_type': '4'}
        files = create_file_dictionary(aut_file=REGS[9], trans_file=IPTRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        #next test program generation
        files = create_file_dictionary(aut_file=REGS[9], trans_file=IPTRANSDUCER_NAMES[1])
        lines = get_code(post, files, False, True)
        self.assertTrue('p = buildErrorCorrectPropS(t)' in lines[-3].split("\n"))
        self.assertEqual(lines[-2],'answer = p.notSatisfiesW(a)\n')
        

    def test_TRAJmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

    def test_TRAJTmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

    def test_IATmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=IATRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=IATRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IATRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=IATRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

    def test_IPTmaxNO(self):
        post = {'question': '2', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[5], trans_file=IPTRANSDUCER_NAMES[2])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IPTRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")


    def test_IPTmaxYES(self):
        post = {'question': '2', 'property_type': '3'}
        files = create_file_dictionary(aut_file=REGS[2], trans_file=IPTRANSDUCER_NAMES[2])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[6], trans_file=IPTRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

    def test_CORRmaxNO(self):
        post = {'question': '2', 'property_type': '4'}
        files = create_file_dictionary(aut_file=REGS[7], trans_file=IPTRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IPTRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

    def test_CORRmaxYES(self):
        post = {'question': '2', 'property_type': '4'}
        files = create_file_dictionary(aut_file=REGS[8], trans_file=IPTRANSDUCER_NAMES[3])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}  # INFIX
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")

    def test_FIXED_IATsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '5'}  # OUTFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")

    def test_FIXED_IATmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '7'}  # HYPERCODE
        files = create_file_dictionary(aut_file=REGS[7])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")

    def test_FIXED_IATmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")

    def test_FIXED_CODEsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=REGS[6])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")

    def test_FIXED_CODEsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")

        post = {'question': '1', 'property_type': '1', 'fixed_type': '5'}
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")

    def test_FIXED_CODEmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=REGS[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '4'}
        files = create_file_dictionary(aut_file=REGS[5])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")

    def test_FIXED_CODEmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")

        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")

    def test_IPTconstr(self):
        post = {'question': '3', 'property_type': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        files = create_file_dictionary(trans_file=IPTRANSDUCER_NAMES[4])
        result = get_response(post, files, False)
        self.assertTrue(hamm_dist_list(result['witness']) > 1)

        post = {'question': '3', 'property_type': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        files = create_file_dictionary(trans_file=IPTRANSDUCER_NAMES[5])
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(hamm_dist_list(witness) > 2)
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))

        files = create_file_dictionary(trans_file=IPTRANSDUCER_NAMES[6])
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))

        files = create_file_dictionary(trans_file=IPTRANSDUCER_NAMES[5])
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))

        files = create_file_dictionary(trans_file=IPTRANSDUCER_NAMES[5])
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
