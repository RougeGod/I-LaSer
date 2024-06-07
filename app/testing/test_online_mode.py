"""Online mode unit tests"""

from app.transducer.views import get_response
from app.transducer.util import parse_aut_str
from app.testing.test_util import hamm_dist, hamm_dist_list, readfile, openfile
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

    '''These tests are a holdover from previous versions, where it was possible to input a language property
       in the language area and have it parsed all as one. Since we have dedicated areas to input language
       properties, and parsing could be ambiguous, the combined language/property feature has been removed
       and these tests are no longer necessary
    def test_combined_files_1(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[0])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_combined_files_2(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[1])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_combined_files_3(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[2])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_combined_files_4(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[3])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_5(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[4])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_combined_files_6(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[5])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_7(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[6])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_8(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[7])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_9(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[8])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_10(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[9])
        post = {'question': '1', 'property_type': '', "automata_text": aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_11(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[10])
        post = {'question': '1', 'property_type': '', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_12(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[11])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_combined_files_13(self):
        files = {}
        aut_text = readfile(COMBINED_NAMES[12])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))
    '''

    def test_mixed(self):
        aut_file = openfile(REGS[3])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '2', 'transducer_text1': t_text}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_file = openfile(REGS[0])
        t_text = readfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '2', 'transducer_text1': t_text}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_text = readfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '2', 'automata_text': aut_text}
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_TRAJsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        aut_file = openfile(REGS[3])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))
        aut_file = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_TRAJTsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        aut_file = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))
        aut_file = openfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_IATsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        aut_file = openfile(REGS[0])
        t_file = openfile(IATRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))
        aut_file = openfile(REGS[3])
        t_file = openfile(IATRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_IATsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        aut_file = openfile(REGS[0])
        t_file = openfile(IATRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))
        aut_file = openfile(REGS[2])
        t_file = openfile(IATRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_IPTsatNO(self):
        post = {'question': '1', 'property_type': '3'}
        aut_file = openfile(REGS[2])
        t_file = openfile(IPTRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))
        aut_file = openfile(REGS[3])
        t_file = openfile(IATRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))
        aut_file = openfile(REGS[1])
        t_file = openfile(IPTRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)

    def test_IPTsatYES(self):
        post = {'question': '1', 'property_type': '3'}
        aut_file = openfile(REGS[4])
        t_file = openfile(IPTRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))
        aut_file = openfile(REGS[5])
        t_file = openfile(IPTRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

    def test_CORRsatNO(self):
        post = {'question': '1', 'property_type': '4'}
        aut_file = openfile(REGS[9])
        t_file = openfile(IPTRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))
        aut_file.close()
        t_file.close()
        #next test program generation
        '''
        aut_file = openfile(REGS[9])
        t_file = openfile(IPTRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        lines = getCode(post, files, False, True)
        self.assertEqual(lines[LN_ANS-1], 'p = buildErrorCorrectPropS(t)\n')
        self.assertEqual(lines[LN_ANS],'print(p.notSatisfiesW(a))\n')
        '''

    def test_TRAJmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        aut_file = openfile(REGS[1])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")
        aut_file = openfile(REGS[5])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

    def test_TRAJTmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        aut_file = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")
        aut_file = openfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

    def test_IATmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        aut_file = openfile(REGS[1])
        t_file = openfile(IATRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")
        aut_file = openfile(REGS[5])
        t_file = openfile(IATRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        aut_file = openfile(REGS[0])
        t_file = openfile(IATRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")
        aut_file = openfile(REGS[2])
        t_file = openfile(IATRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

    def test_IPTmaxNO(self):
        post = {'question': '2', 'property_type': '3'}
        aut_file = openfile(REGS[5])
        t_file = openfile(IPTRANSDUCER_NAMES[2])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")
        aut_file = openfile(REGS[0])
        t_file = openfile(IPTRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")
        aut_file.close()
        t_file.close()
        # next test program generation
        '''
        aut_file = openfile(REGS[0])
        t_file = openfile(IPTRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        lines = getCode(post, files, False, True)
        self.assertEqual(lines[LN_ANS-1],'p = buildIPTPropS(t)\n')
        self.assertEqual(lines[LN_ANS], 'print(p.notMaximalW(a))\n')
        '''

    def test_IPTmaxYES(self):
        post = {'question': '2', 'property_type': '3'}
        aut_file = openfile(REGS[2])
        t_file = openfile(IPTRANSDUCER_NAMES[2])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")
        aut_file = openfile(REGS[6])
        t_file = openfile(IPTRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")

    def test_CORRmaxNO(self):
        post = {'question': '2', 'property_type': '4'}
        aut_file = openfile(REGS[7])
        t_file = openfile(IPTRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")
        aut_file = openfile(REGS[0])
        t_file = openfile(IPTRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "NO, the language is not maximal with respect to the property.")

    def test_CORRmaxYES(self):
        post = {'question': '2', 'property_type': '4'}
        aut_file = openfile(REGS[8])
        t_file = openfile(IPTRANSDUCER_NAMES[3])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")),
         'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL'), "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        aut_file = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '3'}  # INFIX
        aut_file = openfile(REGS[3])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")

    def test_FIXED_IATsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        aut_file = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}  # OUTFIX
        aut_file = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")

    def test_FIXED_IATmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        aut_file = openfile(REGS[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '5'}  # HYPERCODE
        aut_file = openfile(REGS[7])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")

    def test_FIXED_IATmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        aut_file = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        aut_file = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")

    def test_FIXED_CODEsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        aut_file = openfile(REGS[6])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '3'}
        aut_file = openfile(REGS[3])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:26], "NO, the language does not")

    def test_FIXED_CODEsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        aut_file = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}
        aut_file = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:27], "YES, the language satisfies")

    def test_FIXED_CODEmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        aut_file = openfile(REGS[1])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '3'}
        aut_file = openfile(REGS[5])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL')[:23], "NO, the language is not")

    def test_FIXED_CODEmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        aut_file = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '4'}
        aut_file = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result', 'FAIL')[:20], "YES, the language is")

    def test_IPTconstr(self):
        post = {'question': '3', 'property_type': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = openfile(REGS[4])
        t_file = openfile(IPTRANSDUCER_NAMES[4])
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))} #{'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(hamm_dist_list(result['witness']) > 1)
        post = {'question': '3', 'property_type': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = openfile(REGS[4])
        t_file = openfile(IPTRANSDUCER_NAMES[5])
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))} #{'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(hamm_dist_list(witness) > 2)
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = openfile(IPTRANSDUCER_NAMES[6])
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))} #{'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = openfile(IPTRANSDUCER_NAMES[5])
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))} #{'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
        t_file = openfile(IPTRANSDUCER_NAMES[5])
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))} #{'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        witness = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(witness).trieFA().toNFA()))
