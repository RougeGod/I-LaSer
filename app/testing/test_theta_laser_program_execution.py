"""Program Generation Theta Unit Tests"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.transducer.views import get_response
from app.transducer.laser_gen import program_lines, generate_program_file
from app.testing.test_util import openfile, readfile, create_file_dictionary

THETA_NAMES = ['test_files/theta-ab+cd.fa', 'test_files/theta-dna.fa']
TRAJ_NAMES = ['test_files/P-infix-ipt-dna.fa', 'test_files/1#0#.traj', 'test_files/1#0#1#.traj']
REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa', 'test_files/REGEX-a#b.fa']

THETAS = ['test_files/theta/DFA-acc+gtt.fa', 'test_files/theta/DFA-accgg+cgg.fa',
          'test_files/theta/NFA-wcc.fa', 'test_files/theta/DFA-accgg+cggt.fa']

SIGMAS = [{'a', 'b', 'c', 'd'}, {'a', 'c', 'g', 't'}]

INPUT_REQ = -35

# pylint:disable=W0122,C0301,C0111
class MyTestCase(TestCase):
    """Containers Test Cases for Theta-Transducer Program Generation"""
    def test_theta_program_generation(self):
        """Testing Theta Program Generation"""
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[0], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result') or result.get('error_message').find("should be a subset") != -1)

        aut_str = readfile(REGS[0])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars, prog_vars_test = {}, {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEquals(prog_vars["answer"], (None, None))

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertEquals(prog_vars_test['p'].Aut.inIntersection(prog_vars_test['a']).outIntersection(prog_vars_test['theta_aut']).nonEmptyW(), (None, None))

    def test_2(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        #changed to reflect the new restriction that the automaton's alphabet should be a subset of the transducer's
        self.assertTrue(result.get('error_message').find("should be a subset") != -1)
        aut_str = readfile(REGS[1])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars, prog_vars_test = {}, {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEqual(prog_vars["answer"], (None, None))


    def test_3(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[2], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('error_message').startswith("The automaton's alphabet should be a subset")) #again gives the error about the automaton's alphabet not being a subset, which is correct

        aut_str = readfile(REGS[1])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[0])

        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEqual(prog_vars['answer'], (None, None))


    def test_4(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        aut = openfile(REGS[3])
        t_file = openfile(TRAJ_NAMES[0])
        files = create_file_dictionary(aut_file=REGS[3], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('error_message'))

        aut_str = readfile(REGS[3])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEquals(prog_vars['answer'], (None, None))


    def test_5(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result') or result.get('error_message').find("should be a subset") != -1)

        aut_str = readfile(REGS[1])
        t_str = readfile(TRAJ_NAMES[1])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="TRAJECT", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars, prog_vars_test = {}, {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEqual(prog_vars['answer'], (None, None))

        # Same as above
        exec(prog, prog_vars_test, prog_vars_test)
        self.assertEquals(prog_vars_test['p'].Aut.inIntersection(prog_vars_test['a']).outIntersection(prog_vars_test['theta_aut']).nonEmptyW(), (None, None))


    def test_6(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[1], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result') or result.get("error_message").find("should be a subset"))

        aut_str = readfile(REGS[0])
        t_str = readfile(TRAJ_NAMES[1])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="TRAJECT", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEqual(prog_vars['answer'], (None, None))

    def test_7(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[4], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(REGS[1])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEquals(prog_vars['answer'], (None, None))

    def test_8(self):
        th_str = readfile(THETA_NAMES[0])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=REGS[10], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(REGS[10])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[0])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str, aut_type="str2regexp",
                              sigma=SIGMAS[0], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEquals(prog_vars['answer'], (None, None))


    def test_theta_1(self):
        post = {'question':'1', 'property_type':'5'}
        files = create_file_dictionary(aut_file=THETAS[0], trans_file=TRAJ_NAMES[0], theta_file = THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[0])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEquals(prog_vars['answer'], (None, None))

    def test_theta_2(self):
        aut = openfile(THETAS[1])
        t_file = openfile(TRAJ_NAMES[0])
        th_str = readfile(THETA_NAMES[1])

        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = {
            'automata_file':SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8")),
            'transducer_file':SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))
        }
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))
        aut.close()
        t_file.close()

        aut_str = readfile(THETAS[1])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        ans = prog_vars['answer'] != (None, None)
        self.assertTrue(ans)

    def test_theta_3(self):
        post = {'question':'1', 'property_type':'5'}
        files = create_file_dictionary(aut_file=THETAS[3], trans_file=TRAJ_NAMES[0], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[3])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEquals(prog_vars['answer'], (None, None))

    def test_theta_4(self):
        post = {'question':'1', 'property_type':'5'}
        files = create_file_dictionary(aut_file=THETAS[3], trans_file=TRAJ_NAMES[0], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[3])
        t_str = readfile(TRAJ_NAMES[0])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="INPRES", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars, prog_vars_test = {}, {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEquals(prog_vars['answer'], (None, None))

    def test_theta_5(self):
        th_str = readfile(THETA_NAMES[1])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=THETAS[0], trans_file=TRAJ_NAMES[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[0])
        t_str = readfile(TRAJ_NAMES[1])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="TRAJECT", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars, prog_vars_test = {}, {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        ans = prog_vars['answer'] == (None, None)
        self.assertTrue(ans)

    def test_theta_6(self):
        post = {'question':'1', 'property_type':'5'}
        files = create_file_dictionary(aut_file=THETAS[1], trans_file=TRAJ_NAMES[1], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[1])
        t_str = readfile(TRAJ_NAMES[1])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="TRAJECT", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEquals(prog_vars['answer'], (None, None))

    def test_theta_7(self):
        th_str = readfile(THETA_NAMES[1])
        post = {'question':'1', 'property_type':'5', 'theta_text':th_str}
        files = create_file_dictionary(aut_file=THETAS[2], trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[2])
        t_str = readfile(TRAJ_NAMES[1])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="TRAJECT", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertEquals(prog_vars['answer'], (None, None))

    def test_theta_8(self):
        post = {'question':'1', 'property_type':'5'}
        files = create_file_dictionary(aut_file=THETAS[3], trans_file=TRAJ_NAMES[1], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result'))

        aut_str = readfile(THETAS[3])
        t_str = readfile(TRAJ_NAMES[1])
        theta_str = readfile(THETA_NAMES[1])
        lines = program_lines(ptype="TRAJECT", test="NONEMPTYW", aut_str=aut_str,
                              sigma=SIGMAS[1], t_str=t_str, theta_str=theta_str)
        request = 'Construct Trajectory property.'
        prog = "import sys \nsys.stdout = open('trash', 'w')\n" + generate_program_file(lines, None, request)[:INPUT_REQ]
        prog_vars = {}
        #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
        exec(prog, prog_vars, prog_vars)
        self.assertNotEquals(prog_vars['answer'], (None, None))
