import unittest
from transducer.views import * #getCode, getResponse
#from transducer.ILaser_gen import *
from FAdo.reex import *
from FAdo.fio import readOneFromFile
from FAdo.codes import buildIATPropF
import FAdo.fl as fl

regs = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa']
TrajNames = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IATnames  = ['test_files/P-infix.fa', 'test_files/P-suffix.fa', 'test_files/P-transpose1.01.ia.fa']
IPTnames  = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa', 'test_files/P-infix-ipt.fa',
             'test_files/TR-del1.a.fa', 'test_files/TR-sub1.01.ip.fa', 'test_files/TR-sub2.01.ip.fa',
             'test_files/P-transpose1.01.ip.fa']


def hammDist(x,y):
    n = len(x)
    if n != len(y): return None
    dist = 0
    for i in range(n):
        if (x[i] != y[i]):  dist += 1
    return dist


def hammDistList(L):
    minDist = None
    for x in L:
        for y in L:
            if (x==y): continue
            dxy = hammDist(x, y)
            if dxy is not None: 
                if minDist is None: minDist = dxy
                else:    minDist = min(minDist, dxy)
    return minDist


class MyTestCase(unittest.TestCase):

    def test_hammDist(self):
        self.assertEquals(hammDist('000','101'), 2)
        self.assertEquals(hammDist('00','101'), None)
        self.assertEquals(hammDist('0011001100','1111000011'), 6)
        self.assertEquals(hammDistList(['000','101']), 2)
        self.assertEquals(hammDistList(['0011001100','1111000011','000','101']), 2)


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
        # aut = open(regs[9])
        # tFile = open(IPTnames[1])
        # files = {'automata_file': aut, 'transducer_file': tFile}
        # lines = getCode(post, files, False, True)
        # should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)\n') and \
        #             (lines[LN_ANS] == 'print p.notSatisfiesW(a)\n')
        # self.assertTrue(should_be)


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
        # aut = open(regs[0])
        # tFile = open(IPTnames[0])
        # files = {'automata_file': aut, 'transducer_file': tFile}
        # lines = getCode(post, files, False, True)
        # should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)\n') and \
        #             (lines[LN_ANS] == 'print p.notMaximalW(a)\n')
        # self.assertTrue(should_be)


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


    def test_IPTconstr(self):
        post = {'que': '3', 'prv': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = open(regs[4])
        tFile = open(IPTnames[4])
        files = {'transducer_file': tFile} #{'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        #print 'hdist = ', hammDistList(result['witness'])
        self.assertTrue(hammDistList(result['witness']) > 1)
        post = {'que': '3', 'prv': '3', 'n_int': 5, 'l_int': 8, 's_int': 2}
        #aut = open(regs[4])
        tFile = open(IPTnames[5])
        files = {'transducer_file': tFile} #{'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        W = result['witness']
        self.assertTrue(hammDistList(W) > 2)
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))
        tFile = open(IPTnames[6])
        files = {'transducer_file': tFile} #{'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        W = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))
        tFile = open(IPTnames[5])
        files = {'transducer_file': tFile} #{'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)  
        W = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))
        tFile = open(IPTnames[5])
        files = {'transducer_file': tFile} #{'automata_file': aut, 'transducer_file': tFile}
        result = getResponse(post, files, False)
        W = result['witness']
        self.assertTrue(result['prop'].satisfiesP(fl.FL(W).trieFA().toNFA()))


if __name__ == '__main__':
    unittest.main()
