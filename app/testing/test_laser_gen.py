"""Laser Program Generation Tests"""

from django.test import TestCase
from app.transducer.views import get_code
from app.transducer.laser_gen import program_lines, generate_program_file
from app.testing.test_data import a_bstar_a, s1ts, a_ab_bb, t1ts, aa_ab_bb, a_ab_ba, a_bb_star
from app.testing.test_util import hamm_dist, hamm_dist_list, readfile, openfile
import re

#  This program tests methods in the module "laser_gen.py". The
#  current directory should contain a directory "transducer"
#  which in turn should contain "laser_gen.py" (if not then change
#  the above line "from transducer.laser_gen...." appropriately)

LN_ANS = 6
LN_REQ = 11
EXP_EDIT_LINE = 2
FIXED_LINE = 4

#pylint:disable=C0301,W0122,C0111,C0103
class MyTestCase(TestCase):
    def test_p_transpose_constr(self):
        files = {}
        trans_text = readfile('test_files/P-transpose1.01.ia.fa')
        post = {'question': '3', 'property_type': '2', 'transducer_text1': trans_text, 'n_int': 20, 'l_int': 10, 's_int': 10}
        result = get_code(post, files, False)

        self.assertTrue(result.get('result').startswith('<a'))

    def test_CORRsatNO(self):
        lines = "".join(program_lines(ptype="ERRCORR", test="SATW", aut_str=a_bstar_a,
                                      strexp=None, sigma=None, t_str=s1ts, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildErrorCorrectPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        request = 'decide error corection.'
        plines = generate_program_file(lines, None, request).split("\n")
        self.assertEqual(plines[LN_REQ], "print(\"\\nREQUEST:\\n" + request + "\")")
        # stand_alone('1502161240', lines, None, None, request)

    def test_DETmaxNO(self):
        lines = "".join(program_lines(ptype="ERRDET", test="MAXW", aut_str=a_ab_bb,
                                      strexp=None, sigma=None, t_str=t1ts, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        self.assertEqual(lines[LN_ANS-1], 'p = buildErrorDetectPropS(t)')
        self.assertEqual(lines[LN_ANS], 'answer = p.notMaximalW(a)')
        request = 'decide error detection.'
        plines = generate_program_file(lines, None, request).split("\n")
        self.assertEqual(plines[LN_REQ], "print(\"\\nREQUEST:\\n" + request + "\")")

    def test_IPTmaxNO(self):
        lines = "".join(program_lines(ptype="INPRES", test="MAXW", aut_str=a_ab_bb,
                                      strexp=None, sigma=None, t_str=t1ts, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        self.assertEqual(lines[LN_ANS-1], 'p = buildIPTPropS(t)')
        self.assertEqual(lines[LN_ANS], 'answer = p.notMaximalW(a)')
        request = 'decide maximality.'
        plines = generate_program_file(lines, None, request).split("\n")
        self.assertEqual(plines[LN_REQ], "print(\"\\nREQUEST:\\n" + request + "\")")

    def test_TRAJsatNO(self):
        lines = "".join(program_lines(ptype="TRAJECT", test="SATW", aut_str=a_ab_bb,
                                      strexp="1*0*1*", sigma={'a', 'b'}, t_str=None,
                                      s_num=None, l_num=None, n_num=None)).split("\n")
        self.assertTrue(re.match('p = buildTrajPropS\(t, {\'[ab]\', \'[ba]\'}\)',lines[FIXED_LINE- 1]))
        self.assertEqual(lines[FIXED_LINE], 'answer = p.notSatisfiesW(a)')


    def test_IATsatNO(self):
        lines = "".join(program_lines(ptype="INALT", test="SATW", aut_str=a_ab_bb,
                                      strexp=None, sigma=None, t_str=s1ts, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[LN_ANS-1] == 'p = buildIATPropS(t)') and \
                    (lines[LN_ANS] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)


    def test_FIXED_CODEmaxNO(self):
        lines = "".join(program_lines(ptype="CODE", test="MAXP", aut_str=aa_ab_bb,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildUDCodeProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.maximalP(a)')
        self.assertTrue(should_be)


    def test_FIXED_satNO(self):
        lines = "".join(program_lines(ptype="HYPERCODE", test="SATW", aut_str=a_ab_ba,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildHypercodeProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program_lines(ptype="INFIX", test="SATW", aut_str=a_ab_ba,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildInfixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program_lines(ptype="OUTFIX", test="SATW", aut_str=a_ab_ba,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildOutfixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program_lines(ptype="PREFIX", test="SATW", aut_str=a_ab_ba,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildPrefixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)
        #
        lines = "".join(program_lines(ptype="SUFFIX", test="SATW", aut_str=a_ab_ba,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        should_be = (lines[FIXED_LINE-1] == 'p = buildSuffixProperty(ssigma)') and \
                    (lines[FIXED_LINE] == 'answer = p.notSatisfiesW(a)')
        self.assertTrue(should_be)




    def test_EXP_DENS_YES(self):
        lines = "".join(program_lines(ptype="EXPDENSITY", test=None, aut_str=a_bb_star,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        self.assertEqual(lines[EXP_EDIT_LINE], 'print(exponentialDensityP(a))')
        request = 'decide exponential density.'
        plines = generate_program_file(lines, None, request).split("\n")
        self.assertEqual(plines[LN_REQ], "print(\"\\nREQUEST:\\n" + request + "\")")


    def test_EDIT_DIST(self):
        lines = "".join(program_lines(ptype="EDITDIST", test=None, aut_str=a_ab_bb,
                                      strexp=None, sigma=None, t_str=None, s_num=None,
                                      l_num=None, n_num=None)).split("\n")
        self.assertEqual(lines[EXP_EDIT_LINE], 'print(editDistanceW(a))')
