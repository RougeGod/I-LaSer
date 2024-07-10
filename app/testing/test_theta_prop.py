"""Online mode unit tests"""

from app.transducer.views import get_response
from app.testing.test_util import readfile, openfile, create_file_dictionary

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

THETA_NAMES = ['test_files/theta-ab+cd.fa', 'test_files/theta-dna.fa']
TRAJ_NAMES = ['test_files/P-infix-ipt-dna.fa', 'test_files/1#0#.traj', 'test_files/1#0#1#.traj']
REGS = ['test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/NFA-abx.fa', 'test_files/DFA-a+ab+bb.txt', 'test_files/NFA-ab#a.fa',
        'test_files/NFA-Even-b-words.fa', 'test_files/NFA-aaa+bbb.fa', 'test_files/NFA-a(aa)#.fa',
        'test_files/DFA-EvenParity50.fa']

THETAS = ['test_files/theta/DFA-acc+gtt.fa', 'test_files/theta/DFA-accgg+cgg.fa',
          'test_files/theta/NFA-wcc.fa', 'test_files/theta/DFA-accgg+cggt.fa']

#pylint:disable=C0111,C0301,C0103
class MyTestCase(TestCase):
    """Holds theta tests for the website"""

    def test_dna(self):
        """Holds DNA tests"""
        post = {'question': '1', 'property_type': '5'}
        files = create_file_dictionary(aut_file=THETAS[0], trans_file=TRAJ_NAMES[0], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        post = {'question': '1', 'property_type': '5'}
        files = create_file_dictionary(aut_file=THETAS[1], trans_file=TRAJ_NAMES[0], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(THETAS[2])
        t_text = readfile(TRAJ_NAMES[0])
        theta_text = readfile(THETA_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': theta_text, 'transducer_text1': t_text}
        files = {}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text}
        files = create_file_dictionary(aut_file=THETAS[0], theta_file=THETA_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))


        theta_str = readfile(THETA_NAMES[1])


        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': theta_str}
        files = create_file_dictionary(aut_file=THETAS[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_text = readfile(THETAS[2])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': theta_str, 'transducer_text1': t_text}
        files = {}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_text = readfile(THETAS[3])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': theta_str, 'transducer_text1': t_text}
        files = {}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_theta(self):
        """Holds theta tests"""
        THETA_STR = readfile(THETA_NAMES[0])


        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(aut_file=REGS[3])
        result = get_response(post, files, False)   
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        t_text = readfile(TRAJ_NAMES[2])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[0])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[2])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[2])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_file = openfile(REGS[3])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[2])
        result = get_response(post, files, False)
        #self.assertTrue(result.get('result', 'FAIL').startswith('NO')) #unsure if this test should actually return true or false (REGS[3] was recently changed due to its unsupported input)

        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(aut_file=REGS[0])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[0])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[2])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = create_file_dictionary(trans_file=TRAJ_NAMES[1])
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))
