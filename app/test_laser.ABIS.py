import unittest. mock
from transducer.views import *
from transducer.ILaser_gen import *
from FAdo.reex import *
from FAdo.fio import readOneFromFile
from FAdo.codes import buildIATPropF

file_path = '/Users/Stavros/Dropbox/Documents/my_documents/RESEARCH/myHQP/abisola/laser_update/laser/app/test_files/'
regs = [file_path+'DFA-a+ab+bb.fa', file_path+'NFA-aa+ab+bb.fa', file_path+'NFA-aa+ab+ba+bb.fa', file_path+'NFA-abx.fa', file_path+'DFA-a+ab+bb.txt', file_path+'NFA-ab#a.fa',
        file_path+'NFA-Even-b-words.fa', file_path+'NFA-aaa+bbb.fa', file_path+'NFA-a(aa)#.fa', file_path+'DFA-EvenParity100.fa']
TrajNames = [file_path+'1#0#1#.traj', file_path+'1#0#.traj']
IATnames  = [file_path+'P-infix.fa', file_path+'P-suffix.fa']
IPTnames  = [file_path+'P-transpose-1.ipt.fa', file_path+'TR-sub1.ab.fa', file_path+'P-infix-ipt.fa', file_path+'TR-del1.a.fa']

class MyTestCase(unittest.TestCase):
        
    def test_TRAJsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(regs[3])
        tFile = open(TrajNames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(regs[0])
        tFile = open(TrajNames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")


    def test_TRAJTsatYES(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(TrajNames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = open(regs[2])
        tFile = open(TrajNames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_IATsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(IATnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(regs[3])
        tFile = open(IATnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")


    def test_IATsatYES(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(IATnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = open(regs[2])
        tFile = open(IATnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_IPTsatNO(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(regs[2])
        tFile = open(IPTnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(regs[3])
        tFile = open(IATnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut = open(regs[1])
        tFile = open(IPTnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)


    def test_IPTsatYES(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(regs[4])
        tFile = open(IPTnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")
        aut = open(regs[5])
        tFile = open(IPTnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language satisfies the property")


    def test_CORRsatNO(self):
        post = {'que': '1', 'prv': '4'}
        aut = open(regs[9])
        tFile = open(IPTnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language does not satisfy the property")
        aut.close()
        tFile.close()
        # next test program generation 
        aut = open(regs[9])
        tFile = open(IPTnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)\n') and \
                    (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        self.assertTrue(should_be)


    def test_TRAJmaxNO(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(regs[1])
        tFile = open(TrajNames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(regs[5])
        tFile = open(TrajNames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_TRAJTmaxYES(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(TrajNames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(regs[2])
        tFile = open(TrajNames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_IATmaxNO(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(regs[1])
        tFile = open(IATnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(regs[5])
        tFile = open(IATnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'que': '2', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(IATnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(regs[2])
        tFile = open(IATnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_IPTmaxNO(self):
        post = {'que': '2', 'prv': '3'}
        aut = open(regs[5])
        tFile = open(IPTnames[2])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(regs[0])
        tFile = open(IPTnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut.close()
        tFile.close()
        # next test program generation 
        aut = open(regs[0])
        tFile = open(IPTnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)\n') and \
                    (lines[LN_ANS] == 'print p.notMaximalW(a)\n')
        self.assertTrue(should_be)


    def test_IPTmaxYES(self):
        post = {'que': '2', 'prv': '3'}
        aut = open(regs[2])
        tFile = open(IPTnames[2])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")
        aut = open(regs[6])
        tFile = open(IPTnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_CORRmaxNO(self):
        post = {'que': '2', 'prv': '4'}
        aut = open(regs[7])
        tFile = open(IPTnames[1])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")
        aut = open(regs[0])
        tFile = open(IPTnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "NO, the language is not maximal with respect to the property.")


    def test_CORRmaxYES(self):
        post = {'que': '2', 'prv': '4'}
        aut = open(regs[8])
        tFile = open(IPTnames[3])
        files = {'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'], "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '1'}  # PREFIX
        aut = open(regs[0])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
        post = {'que': '1', 'prv': '1', 'fixed_type': '3'}  # INFIX
        aut = open(regs[3])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")


    def test_FIXED_IATsatYES(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(regs[0])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'que': '1', 'prv': '1', 'fixed_type': '4'}  # OUTFIX
        aut = open(regs[2])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")


    def test_FIXED_IATmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(regs[1])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'que': '2', 'prv': '1', 'fixed_type': '5'}  # HYPERCODE
        aut = open(regs[7])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")


    def test_FIXED_IATmaxYES(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '2'}  # SUFFIX
        aut = open(regs[0])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'que': '2', 'prv': '1', 'fixed_type': '1'}  # PREFIX
        aut = open(regs[2])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")


    def test_FIXED_CODEsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[6])   
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")
        post = {'que': '1', 'prv': '1', 'fixed_type': '3'}
        aut = open(regs[3])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:26], "NO, the language does not")


    def test_FIXED_CODEsatYES(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[0])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")
        post = {'que': '1', 'prv': '1', 'fixed_type': '4'}
        aut = open(regs[2])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:27], "YES, the language satisfies")


    def test_FIXED_CODEmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[1])   
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")
        post = {'que': '2', 'prv': '1', 'fixed_type': '3'}
        aut = open(regs[5])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertTrue(result['result'][:23], "NO, the language is not")


    def test_FIXED_CODEmaxYES(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[0])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")
        post = {'que': '2', 'prv': '1', 'fixed_type': '4'}
        aut = open(regs[2])
        files = {'automata_file': aut}
        result = getResponse(post, files, False)
        self.assertEquals(result['result'][:20], "YES, the language is")


    def testGEN_TRAJsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(TrajNames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildTrajPropS(t, set([\'a\', \'b\']))\n') and \
                    (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        self.assertTrue(should_be)

        
    def testGEN_IATsatNO(self):
        post = {'que': '1', 'prv': '2'}
        aut = open(regs[0])
        tFile = open(IATnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildIATPropS(t)\n') and \
                    (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        self.assertTrue(should_be)


    def testGEN_IPTsatNO(self):
        post = {'que': '1', 'prv': '3'}
        aut = open(regs[2])
        tFile = open(IPTnames[0])
        files = {'automata_file': aut, 'transducer_file': tFile}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)\n') and \
                    (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        self.assertTrue(should_be)


    def testGEN_FIXED_CODEmaxNO(self):
        post = {'que': '2', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[1])   
        files = {'automata_file': aut}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildUDCodeProperty(a.Sigma)\n') and \
                    (lines[LN_ANS] == 'print p.maximalP(a)\n')
        self.assertTrue(should_be)


    def testGEN_FIXED_CODEsatNO(self):
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[6])   
        files = {'automata_file': aut}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildUDCodeProperty(a.Sigma)\n') and \
                    (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        self.assertTrue(should_be)
        post = {'que': '1', 'prv': '1', 'fixed_type': '6'}
        aut = open(regs[3])
        files = {'automata_file': aut}
        lines = getCode(post, files, False, True)
        should_be = (lines[LN_ANS-1] == 'p = buildUDCodeProperty(a.Sigma)\n') and \
                    (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        self.assertTrue(should_be)


if __name__ == '__main__':
    unittest.main()
