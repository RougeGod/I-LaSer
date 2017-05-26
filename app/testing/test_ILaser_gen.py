"""Laser Program Generation Tests"""

from django.test import TestCase
from app.transducer.ILaser_gen import program, generate_program
from app.testing.test_data import a_bstar_a, s1ts, a_ab_bb, t1ts, aa_ab_bb, a_ab_ba, a_bb_star

#  This program tests methods in the module "ILaser_gen.py". The
#  current directory should contain a directory "transducer"
#  which in turn should contain "ILaser_gen.py" (if not then change
#  the above line "from transducer.ILaser_gen...." appropriately)

LN_ANS = 6
LN_REQ = 8
EXP_EDIT_LINE = 2
FIXED_LINE = 4

#pylint:disable=C0301,W0122,C0111,C0103
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
