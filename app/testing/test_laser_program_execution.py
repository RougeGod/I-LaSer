"""Unit Tests for the program execution"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.transducer.views import get_response
from app.transducer.laser_gen import program_lines, generate_program_file
from app.testing.test_util import openfile, readfile, create_file_dictionary

REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.fa', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity100.fa', 'test_files/REGEX-a#b.fa']
TRAJ_NAMES = ['test_files/1#0#1#.traj', 'test_files/1#0#.traj']
IA_TRANSDUCER_NAMES = ['test_files/P-infix.fa', 'test_files/P-suffix.fa']
IP_TRANSDUCER_NAMES = ['test_files/P-transpose-1.ipt.fa', 'test_files/TR-sub1.ab.fa',
                       'test_files/P-infix-ipt.fa', 'test_files/TR-del1.a.fa']

IA_TRANSDUCER_NAMES_CONS = ['test_files/construction/P-infix.fa',
                            'test_files/construction/P-suffix.fa']
IP_TRANSDUCER_NAMES_CONS = ['test_files/construction/P-transpose-1.ipt.fa',
                            'test_files/construction/TR-sub1.01.fa']

INPUT_REQUEST_LENGTH = 35

#pylint:disable=C0111,C0301,C0103,W0122
class MyTestCase(TestCase):
    """Holds test cases for laser program execution"""
    def setUp(self):
        self.words = 2
        self.word_length = 2
        self.alphabet_size = 2

    def test_TRAJsatNO(self):
        post = {'question':'1', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[3], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language does not satisfy the property")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language does not satisfy the property")


    def test_TRAJTsatYES(self):
        post = {'question':'1', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language satisfies the property")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language satisfies the property")



    def test_IATsatNO(self):
        post = {'question':'1', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language does not satisfy the property")

        files = create_file_dictionary(aut_file=REGS[3], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language does not satisfy the property")


    def test_IATsatYES(self):
        post = {'question':'1', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language satisfies the property")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language satisfies the property")


    def test_IPTsatNO(self):
        post = {'question':'1', 'property_type':'3'}
        files = create_file_dictionary(aut_file=REGS[3], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language does not satisfy the property")

        files = create_file_dictionary(aut_file=REGS[1], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language does not satisfy the property")


    def test_IPTsatYES(self):
        post = {'question':'1', 'property_type':'3'}
        files = create_file_dictionary(aut_file=REGS[4], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language satisfies the property")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language satisfies the property")


    def test_CORRsatNO(self):
        post = {'question':'1', 'property_type':'4'}
        files = create_file_dictionary(aut_file=REGS[9], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result').startswith("This query is too complex"))


    def test_TRAJmaxNO(self):
        post = {'question':'2', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")


    def test_TRAJTmaxYES(self):
        post = {'question':'2', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language is maximal with respect to the property.")


    def test_IATmaxNO(self):
        post = {'question':'2', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[5], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")


    def test_IATmaxYES(self):
        post = {'question':'2', 'property_type':'2'}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language is maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[2], trans_file=IA_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language is maximal with respect to the property.")

    def test_IPTmaxNO(self):
        post = {'question':'2', 'property_type':'3'}
        files = create_file_dictionary(aut_file=REGS[5], trans_file=IP_TRANSDUCER_NAMES[2])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")

    def test_IPTmaxYES(self):
        post = {'question':'2', 'property_type':'3'}
        files = create_file_dictionary(aut_file=REGS[2], trans_file=IP_TRANSDUCER_NAMES[2])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language is maximal with respect to the property.")


    def test_CORRmaxNO(self):
        post = {'question':'2', 'property_type':'4'}
        files = create_file_dictionary(aut_file=REGS[7], trans_file=IP_TRANSDUCER_NAMES[1])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "NO, the language is not maximal with respect to the property.")


    def test_CORRmaxYES(self):
        post = {'question':'2', 'property_type':'4'}
        files = create_file_dictionary(aut_file=REGS[8], trans_file=IP_TRANSDUCER_NAMES[3])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result'), "YES, the language is maximal with respect to the property.")


    def test_FIXED_IATsatNO(self):
        post = {'question':'1', 'property_type':'1', 'fixed_type':'1'}  # PREFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")

        post = {'question':'1', 'property_type':'1', 'fixed_type':'4'}  # INFIX
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")

    def test_FIXED_IATsatYES(self):
        post = {'question':'1', 'property_type':'1', 'fixed_type':'2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:27], "YES, the language satisfies")

        post = {'question':'1', 'property_type':'1', 'fixed_type':'5'}  # OUTFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:27], "YES, the language satisfies")

    def test_FIXED_IATmaxNO(self):
        post = {'question':'2', 'property_type':'1', 'fixed_type':'2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")

        post = {'question':'2', 'property_type':'1', 'fixed_type':'7'}  # HYPERCODE
        files = create_file_dictionary(aut_file=REGS[7])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")


    def test_FIXED_IATmaxYES(self):
        post = {'question':'2', 'property_type':'1', 'fixed_type':'2'}  # SUFFIX
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:20], "YES, the language is")

        post = {'question':'2', 'property_type':'1', 'fixed_type':'1'}  # PREFIX
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:20], "YES, the language is")


    def test_FIXED_CODEsatNO(self):
        post = {'question':'1', 'property_type':'1', 'fixed_type':'6'} #UD CODE
        files = create_file_dictionary(aut_file=REGS[6])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")

        post = {'question':'1', 'property_type':'1', 'fixed_type':'4'}
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:26], "NO, the language does not")

    def test_FIXED_CODEsatYES(self):
        post = {'question':'1', 'property_type':'1', 'fixed_type':'6'}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:27], "YES, the language satisfies")

        post = {'question':'1', 'property_type':'1', 'fixed_type':'5'}
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:27], "YES, the language satisfies")


    def test_FIXED_CODEmaxNO(self):
        post = {'question':'2', 'property_type':'1', 'fixed_type':'6'}
        files = create_file_dictionary(aut_file=REGS[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")

        post = {'question':'2', 'property_type':'1', 'fixed_type':'4'}
        files = create_file_dictionary(aut_file=REGS[5])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result')[:23], "NO, the language is not")

    def test_FIXED_CODEmaxYES(self):
        post = {'question':'2', 'property_type':'1', 'fixed_type':'6'}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:20], "YES, the language is")

        post = {'question':'2', 'property_type':'1', 'fixed_type':'5'}
        files = create_file_dictionary(aut_file=REGS[2])
        result = get_response(post, files, False)
        self.assertEqual(result.get('result')[:20], "YES, the language is")


    def test_CODE_CONSTRUCT_FIXED_PREFIX(self):
        post = {'question':'3', 'property_type':'1', 'fixed_type':'1', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="PREFIX", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=None,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Fixed PREFIX Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output


        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always verify output becuase automata is generated from output

        # Same as above

        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

    def test_CODE_CONSTRUCT_FIXED_SUFFIX(self):
        post = {'question':'3', 'property_type':'1', 'fixed_type':'2', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="SUFFIX", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=None,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Fixed SUFFIX Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


    def test_CODE_CONSTRUCT_FIXED_INFIX(self):
        post = {'question':'3', 'property_type':'1', 'fixed_type':'4', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="INFIX", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=None,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Fixed INFIX Propert.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


    def test_CODE_CONSTRUCT_FIXED_OUTFIX(self):
        post = {'question':'3', 'property_type':'1', 'fixed_type':'5', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="OUTFIX", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=None,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Fixed Outfix Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


    def test_CODE_CONSTRUCT_FIXED_HYPERCODE(self):
        post = {'question':'3', 'property_type':'1', 'fixed_type':'7', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="HYPERCODE", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=None,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Fixed Hypercode Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always verify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

    #################################################
    # This is disabled beacause of an error in FAdo #
    #################################################
    # def test_CODE_CONSTRUCT_FIXED_CODE(self):
    #     post = {'question':'3', 'property_type':'1', 'fixed_type':'6', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
    #     aut = openfile(REGS[0])
    #     files = {'automata_file':SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
    #     result = get_response(post, files, False)
    #     self.assertTrue(result.get('result'))
    #     aut.close()

    #     aut = openfile(REGS[0])
    #     files = {'automata_file':SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file':''}
    #     aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
    #     lines = program(ptype="CODE", test="MKCO", aut_str=aut_str,
    #                            strexp=None, sigma=None, t_str=None,
    #                            s_num=self.alphabet_size, n_num=self.words,
    #                            l_num=self.word_length)
    #     request = 'Construct Fixed Code Property.'
    #     prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
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
        post = {'question':'3', 'property_type':'2', 'fixed_type':'0', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[0])
        aut_str = bytes.decode(files['automata_file'].read(), encoding="utf-8") #these must always be strings not files
        t_str = bytes.decode(files['transducer_file'].read(), encoding="utf-8")
        lines = program_lines(ptype="TRAJECT", test="MKCO", aut_str=aut_str,
                              strexp="1*0*1*", sigma={'a', 'b', '0', '1'}, t_str=t_str,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

    def test_Code_CONSTRUCT_IAT(self):
        post = {'question':'3', 'property_type':'2', 'fixed_type':'0', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES_CONS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IA_TRANSDUCER_NAMES_CONS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        t_str = bytes.decode(files["transducer_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="INALT", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=t_str,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Input-altering Property'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


    # def test_Code_CONSTRUCT_CORR(self):
    #     post = {'question':'3', 'property_type':'3', 'fixed_type':'0', 'n_int':self.words, 'l_int':self.word_length, 's_int':self.alphabet_size}
    #     aut = openfile(REGS[0])
    #     t_file = openfile(IP_TRANSDUCER_NAMES_CONS[1])
    #     files = {'automata_file':SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file':SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
    #     result = get_response(post, files, False)
    #     self.assertTrue(result.get('result'))
    #     aut.close()
    #     t_file.close()

    #     aut = openfile(REGS[0])
    #     t_file = openfile(IP_TRANSDUCER_NAMES_CONS[1])
    #     files = {'automata_file':SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")), 'transducer_file':SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
    #     aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
    #     t_str = bytes.decode(files["transducer_file"].read(), encoding="utf-8")
    #     lines = program_lines(ptype="ERRCORR", test="MKCO", aut_str=aut_str,
    #                           strexp=None, sigma=None, t_str=t_str,
    #                           s_num=self.alphabet_size, n_num=self.words,
    #                           l_num=self.word_length)
    #     request = 'Construct error correction.'
    #     prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
    #     prog_vars, prog_vars_test = {}, {}
    #     # Execute program twice and Generate two automaton from the code construction output
    #     exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
    #     self.assertFalse(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
    #     # We know that automata would always varify output becuase automata is generated from output

    #     # Same as above
    #     exec(prog, prog_vars_test, prog_vars_test)
    #     self.assertFalse(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))


    #     aut.close()
    #     t_file.close()

    def test_Code_CONSTRUCT_IPT(self):
        post = {'question':'3', 'property_type':'3', 'fixed_type':'0',
                'n_int':self.words, 'l_int':self.word_length,
                's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES_CONS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES_CONS[0])
        aut_str = bytes.decode(files["automata_file"].read(), encoding="utf-8")
        t_str = bytes.decode(files["transducer_file"].read(), encoding="utf-8")
        lines = program_lines(ptype="INPRES", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=t_str,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct Input-preserving Property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

    def test_Code_CONSTRUCT_DET(self):
        post = {'question':'3', 'property_type':'3', 'fixed_type':'0',
                'n_int':self.words, 'l_int':self.word_length,
                's_int':self.alphabet_size}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=IP_TRANSDUCER_NAMES_CONS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(REGS[0])
        t_str = readfile(IP_TRANSDUCER_NAMES_CONS[0])
        lines = program_lines(ptype="ERRDET", test="MKCO", aut_str=aut_str,
                              strexp=None, sigma=None, t_str=t_str,
                              s_num=self.alphabet_size, n_num=self.words,
                              l_num=self.word_length)
        request = 'Construct error detection.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:-INPUT_REQUEST_LENGTH]
        prog_vars, prog_vars_test = {}, {}
        #Execute program twice and Generate two automaton from the code construction output
        exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
        # We know that automata would always varify output becuase automata is generated from output

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))
