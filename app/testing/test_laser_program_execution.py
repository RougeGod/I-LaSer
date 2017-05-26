"""Unit Tests for the program execution"""

import os.path as path

from django.test import TestCase
from app.transducer.views import get_response
from app.transducer.ILaser_gen import program, generate_program
from app.testing.test_util import openfile, readfile

REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.fa', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity100.fa']
TRAJ_NAMES = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IA_TRANSDUCER_NAMES = ['test_files/P-infix.fa', 'test_files/P-suffix.fa']
IP_TRANSDUCER_NAMES = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa',
                       'test_files/P-infix-ipt.fa', 'test_files/TR-del1.a.fa']

IA_TRANSDUCER_NAMES_CONS = ['test_files/construction/P-infix.fa',
                            'test_files/construction/P-suffix.fa']
IP_TRANSDUCER_NAMES_CONS = ['test_files/construction/P-transpose-1.ipt.fa',
                            'test_files/construction/TR-sub1.01.fa']

#pylint:disable=C0111,C0301,C0103,W0122
class MyTestCase(TestCase):
    """Holds test cases for laser program execution"""
    def setUp(self):
        self.words = 2
        self.word_length = 2
        self.alphabet_size = 2

    def test_TRAJsatNO(self):
        post = {'que':'1', 'prv':'2'}
        aut = openfile(REGS[3])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language does not satisfy the property")
        aut.close()
        t_file.close()
        aut = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language does not satisfy the property")
        aut.close()
        t_file.close()


    def test_TRAJTsatYES(self):
        post = {'que':'1', 'prv':'2'}
        aut = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language satisfies the property")
        aut.close()
        t_file.close()
        aut = openfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language satisfies the property")
        aut.close()
        t_file.close()


    def test_IATsatNO(self):
        post = {'que':'1', 'prv':'2'}
        aut = openfile(REGS[0])
        t_file = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language does not satisfy the property")
        aut.close()
        t_file.close()
        aut = openfile(REGS[3])
        t_file = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language does not satisfy the property")
        aut.close()
        t_file.close()


    def test_IATsatYES(self):
        post = {'que':'1', 'prv':'2'}
        aut = openfile(REGS[0])
        t_file = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language satisfies the property")
        aut.close()
        t_file.close()
        aut = openfile(REGS[2])
        t_file = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language satisfies the property")
        aut.close()
        t_file.close()


    def test_IPTsatNO(self):
        post = {'que':'1', 'prv':'3'}
        aut = openfile(REGS[3])
        t_file = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language does not satisfy the property")
        aut.close()
        t_file.close()
        aut = openfile(REGS[1])
        t_file = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)


    def test_IPTsatYES(self):
        post = {'que':'1', 'prv':'3'}
        aut = openfile(REGS[4])
        t_file = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language satisfies the property")
        aut.close()
        t_file.close()
        aut = openfile(REGS[5])
        t_file = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language satisfies the property")
        aut.close()
        t_file.close()


    def test_CORRsatNO(self):
        post = {'que':'1', 'prv':'4'}
        aut = openfile(REGS[9])
        t_file = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertTrue(result.get('error_message').startswith("Sizes"))
        aut.close()
        t_file.close()


    def test_TRAJmaxNO(self):
        post = {'que':'2', 'prv':'2'}
        aut = openfile(REGS[1])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()
        aut = openfile(REGS[5])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_TRAJTmaxYES(self):
        post = {'que':'2', 'prv':'2'}
        aut = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language is maximal with respect to the property.")
        aut.close()
        t_file.close()
        aut = openfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language is maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_IATmaxNO(self):
        post = {'que':'2', 'prv':'2'}
        aut = openfile(REGS[1])
        t_file = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()
        aut = openfile(REGS[5])
        t_file = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_IATmaxYES(self):
        post = {'que':'2', 'prv':'2'}
        aut = openfile(REGS[0])
        t_file = openfile(IA_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language is maximal with respect to the property.")
        aut.close()
        t_file.close()
        aut = openfile(REGS[2])
        t_file = openfile(IA_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language is maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_IPTmaxNO(self):
        post = {'que':'2', 'prv':'3'}
        aut = openfile(REGS[5])
        t_file = openfile(IP_TRANSDUCER_NAMES[2])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()
        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_IPTmaxYES(self):
        post = {'que':'2', 'prv':'3'}
        aut = openfile(REGS[2])
        t_file = openfile(IP_TRANSDUCER_NAMES[2])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language is maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_CORRmaxNO(self):
        post = {'que':'2', 'prv':'4'}
        aut = openfile(REGS[7])
        t_file = openfile(IP_TRANSDUCER_NAMES[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()
        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "NO, the language is not maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_CORRmaxYES(self):
        post = {'que':'2', 'prv':'4'}
        aut = openfile(REGS[8])
        t_file = openfile(IP_TRANSDUCER_NAMES[3])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result'), "YES, the language is maximal with respect to the property.")
        aut.close()
        t_file.close()


    def test_FIXED_IATsatNO(self):
        post = {'que':'1', 'prv':'1', 'fixed_type':'1'}  # PREFIX
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")
        aut.close()

        post = {'que':'1', 'prv':'1', 'fixed_type':'3'}  # INFIX
        aut = openfile(REGS[3])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")
        aut.close()



    def test_FIXED_IATsatYES(self):
        post = {'que':'1', 'prv':'1', 'fixed_type':'2'}  # SUFFIX
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:27], "YES, the language satisfies")
        aut.close()

        post = {'que':'1', 'prv':'1', 'fixed_type':'4'}  # OUTFIX
        aut = openfile(REGS[2])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:27], "YES, the language satisfies")
        aut.close()



    def test_FIXED_IATmaxNO(self):
        post = {'que':'2', 'prv':'1', 'fixed_type':'2'}  # SUFFIX
        aut = openfile(REGS[1])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")
        aut.close()

        post = {'que':'2', 'prv':'1', 'fixed_type':'5'}  # HYPERCODE
        aut = openfile(REGS[7])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")
        aut.close()



    def test_FIXED_IATmaxYES(self):
        post = {'que':'2', 'prv':'1', 'fixed_type':'2'}  # SUFFIX
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:20], "YES, the language is")
        aut.close()

        post = {'que':'2', 'prv':'1', 'fixed_type':'1'}  # PREFIX
        aut = openfile(REGS[2])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:20], "YES, the language is")
        aut.close()



    def test_FIXED_CODEsatNO(self):
        post = {'que':'1', 'prv':'1', 'fixed_type':'6'}
        aut = openfile(REGS[6])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")
        aut.close()

        post = {'que':'1', 'prv':'1', 'fixed_type':'3'}
        aut = openfile(REGS[3])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")
        aut.close()



    def test_FIXED_CODEsatYES(self):
        post = {'que':'1', 'prv':'1', 'fixed_type':'6'}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:27], "YES, the language satisfies")
        aut.close()

        post = {'que':'1', 'prv':'1', 'fixed_type':'4'}
        aut = openfile(REGS[2])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:27], "YES, the language satisfies")
        aut.close()



    def test_FIXED_CODEmaxNO(self):
        post = {'que':'2', 'prv':'1', 'fixed_type':'6'}
        aut = openfile(REGS[1])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")
        aut.close()

        post = {'que':'2', 'prv':'1', 'fixed_type':'3'}
        aut = openfile(REGS[5])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")
        aut.close()



    def test_FIXED_CODEmaxYES(self):
        post = {'que':'2', 'prv':'1', 'fixed_type':'6'}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:20], "YES, the language is")
        aut.close()

        post = {'que':'2', 'prv':'1', 'fixed_type':'4'}

        aut = openfile(REGS[2])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertEquals(result.get('result')[:20], "YES, the language is")
        aut.close()


    def test_CODE_CONSTRUCT_FIXED_PREFIX(self):
        post = {'que':'3', 'prv':'1', 'fixed_type':'1', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()

        aut = openfile(REGS[0])
        files = {'automata_file':aut, 'transducer_file':''}
        aut_str = files['automata_file'].read()
        lines = program(ptype="PREFIX", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=None,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Fixed PREFIX Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output


        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above

        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
        aut.close()

    def test_CODE_CONSTRUCT_FIXED_SUFFIX(self):
        post = {'que':'3', 'prv':'1', 'fixed_type':'2', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()

        aut = openfile(REGS[0])
        files = {'automata_file':aut, 'transducer_file':''}
        aut_str = files['automata_file'].read()
        lines = program(ptype="SUFFIX", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=None,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Fixed SUFFIX Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
        aut.close()
    def test_CODE_CONSTRUCT_FIXED_INFIX(self):
        post = {'que':'3', 'prv':'1', 'fixed_type':'3', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()

        aut = openfile(REGS[0])
        files = {'automata_file':aut, 'transducer_file':''}
        aut_str = files['automata_file'].read()
        lines = program(ptype="INFIX", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=None,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Fixed INFIX Propert.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
        aut.close()
    def test_CODE_CONSTRUCT_FIXED_OUTFIX(self):
        post = {'que':'3', 'prv':'1', 'fixed_type':'4', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()

        aut = openfile(REGS[0])
        files = {'automata_file':aut, 'transducer_file':''}
        aut_str = files['automata_file'].read()
        lines = program(ptype="OUTFIX", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=None,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Fixed Outfix Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
        aut.close()
    def test_CODE_CONSTRUCT_FIXED_HYPERCODE(self):
        post = {'que':'3', 'prv':'1', 'fixed_type':'5', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        files = {'automata_file':aut}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()

        aut = openfile(REGS[0])
        files = {'automata_file':aut, 'transducer_file':''}
        aut_str = files['automata_file'].read()
        lines = program(ptype="HYPERCODE", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=None,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Fixed Hypercode Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
        aut.close()

    #################################################
    # This is disabled beacause of an error in FAdo #
    #################################################
    # def test_CODE_CONSTRUCT_FIXED_CODE(self):
    #     post = {'que':'3', 'prv':'1', 'fixed_type':'6', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
    #     aut = openfile(REGS[0])
    #     files = {'automata_file':aut}
    #     result = get_response(post, files, False)
    #     self.assertTrue(result.get('result'))
    #     aut.close()

    #     aut = openfile(REGS[0])
    #     files = {'automata_file':aut, 'transducer_file':''}
    #     aut_str = files['automata_file'].read()
    #     lines = program(ptype="CODE", test="MKCO", aname=aut_str,
    #                     strexp=None, sigma=None, tname=None,
    #                     s_num=self.alphabet_size, n_num=self.words,
    #                     l_num=self.word_length)
    #     request = 'Construct Fixed Code Property.'
    #     prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
    #     prog_vars, prog_vars_test = {}, {}
    #     #Execute program twice and Generate two automaton from the code construction output
    #     exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
    #     self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
    #     # We know that automata would always varify output becuase automata is generated from output

    #     # Same as above
    #     exec(prog, prog_vars_test, prog_vars_test)
    #     self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
    #     aut.close()

    def test_CODE_CONSTRUCT_TRAJ(self):
        post = {'que':'3', 'prv':'2', 'fixed_type':'0', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()
        t_file.close()

        aut = openfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        aut_str = files['automata_file'].read()
        t_str = files['transducer_file'].read()
        lines = program(ptype="TRAJECT", test="MKCO", aname=aut_str,
                        strexp="1*0*1*", sigma={'a', 'b', '0', '1'}, tname=t_str,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

        aut.close()
        t_file.close()

    def test_Code_CONSTRUCT_IAT(self):
        post = {'que':'3', 'prv':'2', 'fixed_type':'0', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}


        aut = openfile(REGS[0])
        t_file = openfile(IA_TRANSDUCER_NAMES_CONS[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()
        t_file.close()

        aut = openfile(REGS[0])
        t_file = openfile(IA_TRANSDUCER_NAMES_CONS[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        aut_str = files['automata_file'].read()
        t_str = files['transducer_file'].read()
        lines = program(ptype="INALT", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=t_str,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Input-altering Property'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


        aut.close()
        t_file.close()

    def test_Code_CONSTRUCT_CORR(self):
        post = {'que':'3', 'prv':'3', 'fixed_type':'0', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES_CONS[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()
        t_file.close()

        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES_CONS[1])
        files = {'automata_file':aut, 'transducer_file':t_file}
        aut_str = files['automata_file'].read()
        t_str = files['transducer_file'].read()
        lines = program(ptype="ERRCORR", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=t_str,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct error correction.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertFalse(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertFalse(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


        aut.close()
        t_file.close()

    def test_Code_CONSTRUCT_IPT(self):
        post = {'que':'3', 'prv':'3', 'fixed_type':'0',
                'n_int':self.words, 'l_int':self.word_length,
                's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES_CONS[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()
        t_file.close()

        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES_CONS[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        aut_str = files['automata_file'].read()
        t_str = files['transducer_file'].read()
        lines = program(ptype="INPRES", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=t_str,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct Input-preserving Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

        aut.close()
        t_file.close()

    def test_Code_CONSTRUCT_DET(self):
        post = {'que':'3', 'prv':'3', 'fixed_type':'0',
                'n_int':self.words, 'l_int':self.word_length,
                's_int':self.alphabet_size}
        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES_CONS[0])
        files = {'automata_file':aut, 'transducer_file':t_file}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()
        t_file.close()

        aut = openfile(REGS[0])
        t_file = openfile(IP_TRANSDUCER_NAMES_CONS[0])
        files = {'automata_file': aut, 'transducer_file': t_file}
        aut_str = files['automata_file'].read()
        t_str = files['transducer_file'].read()
        lines = program(ptype="ERRDET", test="MKCO", aname=aut_str,
                        strexp=None, sigma=None, tname=t_str,
                        s_num=self.alphabet_size, n_num=self.words,
                        l_num=self.word_length)
        request = 'Construct error detection.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program(lines, None, request)[:-38]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

        aut.close()
        t_file.close()