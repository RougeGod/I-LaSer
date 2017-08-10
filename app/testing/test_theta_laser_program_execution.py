"""Program Generation Theta Unit Tests"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.transducer.laser_gen import program_lines, gen_program
from app.testing.test_util import openfile, readfile

THETA_NAMES = ['test_files/theta-ab+cd.fa', 'test_files/theta-dna.fa']
TRAJ_NAMES = ['test_files/P-infix-ipt-dna.fa', 'test_files/1#0#.traj', 'test_files/1#0#1#.traj']
REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa']

THETAS = ['test_files/theta/DFA-acc+gtt.fa', 'test_files/theta/DFA-accgg+cgg.fa',
          'test_files/theta/NFA-wcc.fa', 'test_files/theta/DFA-accgg+cggt.fa']

# class MyTestCase(TestCase):
    # def test_CODE_CONSTRUCT_TRAJ(self):
    #     post = {'question':'2', 'property_type':'5',}
    #     aut = openfile(REGS[0])
    #     t_file = openfile(TRAJ_NAMES[0])
    #     files = {'automata_file':SimpleUploadedFile(aut.name, aut.read()), 'transducer_file':SimpleUploadedFile(t_file.name, t_file.read())}
    #     result = get_response(post, files, False)
    #     self.assertTrue(result.get('result'))
    #     aut.close()
    #     t_file.close()

    #     aut = openfile(REGS[0])
    #     t_file = openfile(TRAJ_NAMES[0])
    #     aut_str = files['automata_file'].read()
    #     t_str = files['transducer_file'].read()
    #     lines = program(ptype="TRAJECT", test="MKCO", aname=aut_str,
    #                     strexp="1*0*1*", sigma={'a', 'b', '0', '1'}, tname=t_str)
    #     request = 'Construct Trajectory property.'
    #     prog = "import sys \nsys.stdout = open('trash', 'w')\n" + gen_program(lines, None, request)[:-38]
    #     prog_vars, prog_vars_test = {}, {}
    #     #Execute program twice and Generate two automaton from the code construction output
    #     exec(prog, prog_vars, prog_vars)  #store prog variables in global and local dictonaries 'prog_vars'. Both are same otherwise local variables are stored as a class
    #     self.assertTrue(prog_vars['p'].satisfiesP(prog_vars['a'])) #Test is automata satisfies property and return boolean value
    #     # We know that automata would always varify output becuase automata is generated from output

    #     # Same as above
    #     exec(prog, prog_vars_test, prog_vars_test)
    #     self.assertTrue(prog_vars_test['p'].satisfiesP(prog_vars_test['a']))

    #     aut.close()
    #     t_file.close()
