from django.test import TestCase
from transducer.ILaser_gen import *
#import FAdo.fio as fio

#  This program tests methods in the module "ILaser_gen.py". The
#  current directory should contain a directory "transducer"
#  which in turn should contain "ILaser_gen.py" (if not then change
#  the above line "from transducer.ILaser_gen...." appropriately)

####################################################################
#   THE NEXT SECTION CONTAINS LOTS OF GLOBAL VARIABLES FOR
#   DESCRIBING AUTOMATA AND TRANSDUCERS
#
#   UNIT TESTING ITSELF IS LOCATED FURTHER BELOW
####################################################################

#
#
##  Input altering transducers for var length codes
strpx = '@Transducer 1 * 0\n0 a a 0\n0 b b 0\n0 a @epsilon 1\n0 b @epsilon 1\n1 a @epsilon 1\n1 b @epsilon 1\n'
#tpx = fio.readOneFromString(strpx)
strsx = '@Transducer 1 * 0\n0 a @epsilon 0\n0 b @epsilon 0\n0 a @epsilon 1\n0 b @epsilon 1\n1 a a 1\n1 b b 1\n'
#tsx = fio.readOneFromString(strsx)
#
#
##  Input altering transducers
str1sd = '@Transducer 1 * 0\n0 a a 0\n0 b b 0\n0 a b 1\n1 a a 1\n1 b b 1\n'
#t1sd = fio.readOneFromString(str1sd)
str2sd = '@Transducer 1 2 * 0\n0 a a 0\n0 b b 0\n0 a b 1\n1 a a 1\n1 b b 1\n1 a b 2\n1 b a 2\n2 a a 2\n2 b b 2\n'
#t2sd = fio.readOneFromString(str2sd)
#
str1id = '@Transducer 1 * 0\n0 a a 0\n0 b b 0\n0 a @epsilon 1\n0 b @epsilon 1\n1 a a 1\n1 b b 1\n'
#t1id = fio.readOneFromString(str1id)
str2id = '@Transducer 1 2 * 0 3 6\n0 a a 0\n0 b b 0\n0 a @epsilon 1\n0 b @epsilon 1\n'\
         '1 a a 1\n1 b b 1\n1 a @epsilon 2\n1 b @epsilon 2\n2 a a 2\n2 b b 2\n'\
         '3 a a 3\n3 b b 3\n3 a @epsilon 4\n4 b b 5\n5 a a 5\n5 b b 5\n4 @epsilon b 2\n'\
         '5 @epsilon a 2\n5 @epsilon b 2\n'\
         '6 a a 6\n6 b b 6\n6 @epsilon b 7\n7 a a 8\n8 a a 8\n8 b b 8\n7 a @epsilon 2\n'\
         '8 a @epsilon 2\n8 b @epsilon 2\n'
#t2id = fio.readOneFromString(str2id)
#
#
##  Input preserving transducers for error-detection
#
# Up to 1 substitution (IP transducer)
s1ts = '@Transducer 0 1 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 b a 1\n'\
        '0 a b 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'

# Up to 2 substitutions (IP transducer)
s2ts = '@Transducer 0 1 2 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 b a 1\n'\
        '0 a b 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'\
        '1 b a 2\n'\
        '1 a b 2\n'\
        '2 a a 2\n'\
        '2 b b 2\n'

# Up to 1 insertion and deletion (IP transducer)
id1ts = '@Transducer 0 1 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 @epsilon a 1\n'\
        '0 @epsilon b 1\n'\
        '0 a @epsilon 1\n'\
        '0 b @epsilon 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'

# Up to 2 insertions and deletions (IP transducer)
id2ts = '@Transducer 0 1 2 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 @epsilon a 1\n'\
        '0 @epsilon b 1\n'\
        '0 a @epsilon 1\n'\
        '0 b @epsilon 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'\
        '1 @epsilon a 2\n'\
        '1 @epsilon b 2\n'\
        '1 a @epsilon 2\n'\
        '1 b @epsilon 2\n'\
        '2 a a 2\n'\
        '2 b b 2\n'

# Up to 1 transposition error
t1ts = '@Transducer 0 3 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 a b 1\n'\
        '1 b a 3\n'\
        '0 b a 2\n'\
        '2 a b 3\n'\
        '3 a a 3\n'\
        '3 b b 3\n'

#
# odd parity code of length 5
op5as = '@NFA 9 * 0\n'\
        '0 a 2\n'\
        '0 b 1\n'\
        '2 a 4\n'\
        '2 b 3\n'\
        '4 a 6\n'\
        '4 b 5\n'\
        '6 a 8\n'\
        '6 b 7\n'\
        '8 b 9\n'\
        '1 a 3\n'\
        '1 b 4\n'\
        '3 a 5\n'\
        '3 b 6\n'\
        '5 a 7\n'\
        '5 b 8\n'\
        '7 a 9\n'

a_bstar_a = '@NFA 2 * 0\n'\
        '0 a 1\n'\
        '1 b 1\n'\
        '1 a 2\n'\

a_bb_star = '@NFA 0 * 0\n'\
        '0 a 0\n'\
        '0 b 1\n'\
        '1 b 0\n'\

a_ab_bb = '@NFA 1 3 * 0\n'\
        '0 a 1\n'\
        '0 b 2\n'\
        '1 b 3\n'\
        '2 b 3\n'\

a_ab_ba = '@NFA 1 3 * 0\n'\
        '0 a 1\n'\
        '0 b 2\n'\
        '1 b 3\n'\
        '2 a 3\n'\

aa_ab_bb = '@NFA 3 * 0\n'\
        '0 a 1\n'\
        '0 b 2\n'\
        '1 a 3\n'\
        '1 b 3\n'\
        '2 b 3\n'\

strb5 = '@NFA 5 * 0\n0 a 1\n0 b 1\n1 a 2\n1 b 2\n2 a 3\n2 b 3\n3 a 4\n3 b 4\n4 a 5\n4 b 5\n'
#ab5 = fio.readOneFromString(strb5)
strb6 = '@NFA 6 * 0\n0 a 1\n0 b 1\n1 a 2\n1 b 2\n2 a 3\n2 b 3\n3 a 4\n3 b 4\n4 a 5\n4 b 5\n5 a 6\n5 b 6\n'
#ab6 = fio.readOneFromString(strb6)
strb7 = '@NFA 7 * 0\n0 a 1\n0 b 1\n1 a 2\n1 b 2\n2 a 3\n2 b 3\n3 a 4\n3 b 4\n4 a 5\n4 b 5\n5 a 6\n5 b 6\n6 a 7\n6 b 7\n'
#ab7 = fio.readOneFromString(strb7)


############################################################################
#
#         UNIT TESTING IS NEXT
#
############################################################################
#

LN_ANS = 6
LN_REQ = 8
EXP_EDIT_LINE = 2
FIXED_LINE = 4

class MyTestCase(TestCase):
    def test_CORRsatNO(self):
        lines = "".join(program(ptype="ERRCORR", test="SATW", aname=a_bstar_a,
                                strexp=None, sigma=None, tname=s1ts, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        request = 'decide error corection.'
        plines = generate_program(lines, None, request).split("\n")
        self.assertTrue(plines[LN_REQ] == 'print "\\nREQUEST:\\n'+request+'"')
        # stand_alone('1502161240', lines, None, None, request)


    def test_DETmaxNO(self):
        lines = "".join(program(ptype="ERRDET", test="MAXW", aname=a_ab_bb,
                                strexp=None, sigma=None, tname=t1ts, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildErrorDetectPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notMaximalW(a)')
        self.assertTrue(should_be)
        request = 'decide error detection.'
        plines = generate_program(lines, None, request).split("\n")
        self.assertTrue(plines[LN_REQ] == 'print "\\nREQUEST:\\n'+request+'"')


    def test_IPTmaxNO(self):
        lines = "".join(program(ptype="INPRES", test="MAXW", aname=a_ab_bb,
                                strexp=None, sigma=None, tname=t1ts, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildIPTPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notMaximalW(a)')
        self.assertTrue(should_be)
        request = 'decide maximality.'
        plines = generate_program(lines, None, request).split("\n")
        should_be = plines[LN_REQ] == 'print "\\nREQUEST:\\n'+request+'"'
        self.assertTrue(should_be)


    def test_TRAJsatNO(self):
        lines = "".join(program(ptype="TRAJECT", test="SATW", aname=a_ab_bb,
                                strexp="1*0*1*", sigma={'a', 'b'}, tname=None,
                                s_num=None, l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildTrajPropS(t, set([\'a\', \'b\']))') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)


    def test_IATsatNO(self):
        lines = "".join(program(ptype="INALT", test="SATW", aname=a_ab_bb,
                                strexp=None, sigma=None, tname=s1ts, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildIATPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)


    def test_FIXED_CODEmaxNO(self):
        lines = "".join(program(ptype="CODE", test="MAXP", aname=aa_ab_bb,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildUDCodeProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.maximalP(a)')
        self.assertTrue(should_be)


    def test_FIXED_satNO(self):
        lines = "".join(program(ptype="HYPERCODE", test="SATW", aname=a_ab_ba,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildHypercodeProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program(ptype="INFIX", test="SATW", aname=a_ab_ba,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildInfixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program(ptype="OUTFIX", test="SATW", aname=a_ab_ba,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildOutfixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program(ptype="PREFIX", test="SATW", aname=a_ab_ba,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildPrefixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program(ptype="SUFFIX", test="SATW", aname=a_ab_ba,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildSuffixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)




    def test_EXP_DENS_YES(self):
        lines = "".join(program(ptype="EXPDENSITY", test=None, aname=a_bb_star,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[EXP_EDIT_LINE] == 'print exponentialDensityP(a)')
        self.assertTrue(should_be)
        request = 'decide exponential density.'
        plines = generate_program(lines, None, request).split("\n")
        should_be = plines[LN_REQ] == 'print "\\nREQUEST:\\n'+request+'"'
        self.assertTrue(should_be)


    def test_EDIT_DIST(self):
        lines = "".join(program(ptype="EDITDIST", test=None, aname=a_ab_bb,
                                strexp=None, sigma=None, tname=None, s_num=None,
                                l_num=None, n_num=None)).split("\n")
        should_be = (lines[EXP_EDIT_LINE] == 'print editDistanceW(a)')
        self.assertTrue(should_be)
