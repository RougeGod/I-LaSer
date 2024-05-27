"""Laser Unit Tests"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile
import re


REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity100.fa']
TRAJ_NAMES = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IA_TRANSDUCER_NAMES = ['test_files/P-infix.fa', 'test_files/P-suffix.fa']
IP_TRANSDUCER_NAMES = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa',
                       'test_files/P-infix-ipt.fa', 'test_files/TR-del1.a.fa']

LN_ANS = 6
LN_REQ = 4

#pylint:disable=C0301,W0122,C0111,C0103
class MyTestCase(TestCase):
    def test_TRAJsatNO(self):
        post = {'question': '1', 'property_type': '2'}
 #       aut = openfile(REGS[3])
  #      tFile = openfile(TRAJ_NAMES[1])
   #     files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
    #    result = get_response(post, files, False)
     #   self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = openfile(REGS[0])
        tFile = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")


    def test_TRAJTsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = openfile(REGS[2])
        tFile = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_IATsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
#        aut = openfile(REGS[3])
 #       tFile = openfile(IA_TRANSDUCER_NAMES[1])
  #      files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
   #     result = get_response(post, files, False)
    #    self.assertEquals(result['result'], "NO, the language does not satisfy the property")


    def test_IATsatYES(self):
        post = {'question': '1', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = openfile(REGS[2])
        tFile = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_IPTsatNO(self):
        post = {'question': '1', 'property_type': '3'}
        aut = openfile(REGS[2])
        tFile = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
#        aut = openfile(REGS[3])
 #       tFile = openfile(IA_TRANSDUCER_NAMES[1])
  #      files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
   #     result = get_response(post, files, False)
    #    self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = openfile(REGS[1])
        tFile = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)


    def test_IPTsatYES(self):
        post = {'question': '1', 'property_type': '3'}
        aut = openfile(REGS[4])
        tFile = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = openfile(REGS[5])
        tFile = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_CORRsatNO(self):
        post = {'question': '1', 'property_type': '4'}
        aut = openfile(REGS[9])
        tFile = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertIsNone(result.get('result'))
        aut.close()
        tFile.close()
        # next test program generation
        aut = openfile(REGS[9])
        tFile = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)


    def test_TRAJmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        aut = openfile(REGS[1])
        tFile = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = openfile(REGS[5])
        tFile = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_TRAJTmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(TRAJ_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = openfile(REGS[2])
        tFile = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_IATmaxNO(self):
        post = {'question': '2', 'property_type': '2'}
        aut = openfile(REGS[1])
        tFile = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = openfile(REGS[5])
        tFile = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'question': '2', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = openfile(REGS[2])
        tFile = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_IPTmaxNO(self):
        post = {'question': '2', 'property_type': '3'}
        aut = openfile(REGS[5])
        tFile = openfile(IP_TRANSDUCER_NAMES[2])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = openfile(REGS[0])
        tFile = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut.close()
        tFile.close()
        # next test program generation
        aut = openfile(REGS[0])
        tFile = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notMaximalW(a)')
        self.assertTrue(should_be)


    def test_IPTmaxYES(self):
        post = {'question': '2', 'property_type': '3'}
        aut = openfile(REGS[2])
        tFile = openfile(IP_TRANSDUCER_NAMES[2])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = openfile(REGS[6])
        tFile = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_CORRmaxNO(self):
        post = {'question': '2', 'property_type': '4'}
        aut = openfile(REGS[7])
        tFile = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = openfile(REGS[0])
        tFile = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_CORRmaxYES(self):
        post = {'question': '2', 'property_type': '4'}
        aut = openfile(REGS[8])
        tFile = openfile(IP_TRANSDUCER_NAMES[3])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        aut = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
#        post = {'question': '1', 'property_type': '1', 'fixed_type': '3'}  # INFIX
 #       aut = openfile(REGS[3])
  #      files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
    #    result = get_response(post, files, False)
   #     self.assertTrue(result['result'][:26], "NO, the language does not")


    def test_FIXED_IATsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        aut = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}  # OUTFIX
        aut = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")


    def test_FIXED_IATmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        aut = openfile(REGS[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '5'}  # HYPERCODE
        aut = openfile(REGS[7])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")


    def test_FIXED_IATmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '2'}  # SUFFIX
        aut = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '1'}  # PREFIX
        aut = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")


    def test_FIXED_CODEsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[6])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
#        post = {'question': '1', 'property_type': '1', 'fixed_type': '3'}
 #       aut = openfile(REGS[3])
  #      files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
   #     result = get_response(post, files, False)
    #    self.assertTrue(result['result'][:26], "NO, the language does not")


    def test_FIXED_CODEsatYES(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'question': '1', 'property_type': '1', 'fixed_type': '4'}
        aut = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")


    def test_FIXED_CODEmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '3'}
        aut = openfile(REGS[5])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")


    def test_FIXED_CODEmaxYES(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'question': '2', 'property_type': '1', 'fixed_type': '4'}
        aut = openfile(REGS[2])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")


    def testGEN_TRAJsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(TRAJ_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        #set ordering doesn't matter but it has to be a set with both a and b
        self.assertTrue(re.match('p = buildTrajPropS\(t, {\'[ab]\', \'[ba]\'}\)', lines[LN_ANS - 1]))
        self.assertEqual(lines[LN_ANS],'answer = p.notSatisfiesW(a)')


    def testGEN_IATsatNO(self):
        post = {'question': '1', 'property_type': '2'}
        aut = openfile(REGS[0])
        tFile = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")

        should_be = (lines[LN_ANS-1].startswith('p = buildIATPropS')) and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)


    def testGEN_IPTsatNO(self):
        post = {'question': '1', 'property_type': '3'}
        aut = openfile(REGS[2])
        tFile = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file': SimpleUploadedFile(tFile.name, str.encode(tFile.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)


    def testGEN_FIXED_CODEmaxNO(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[1])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        should_be = (lines[LN_REQ-1] == 'p = buildUDCodeProperty(ssigma)') and \
                    (lines[LN_REQ] == 'answer = p.maximalP(a)')
        self.assertTrue(should_be)


    def testGEN_FIXED_CODEsatNO(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[6])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        should_be = (lines[LN_REQ-1] == 'p = buildUDCodeProperty(ssigma)') and \
                    (lines[LN_REQ] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6'}
        aut = openfile(REGS[3])
        files = {'automata_file': SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
        lines = "".join(get_code(post, files, False, True)).split("\n")
        should_be = (lines[LN_REQ-1] == 'p = buildUDCodeProperty(ssigma)') and \
                    (lines[LN_REQ] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
