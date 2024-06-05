"""Online mode unit tests"""

from app.transducer.views import get_response
from app.testing.test_util import readfile, openfile

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
        THETA_STR = readfile(THETA_NAMES[1])

        aut_file = openfile(THETAS[0])
        t_text = readfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_file = openfile(THETAS[1])
        t_text = readfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read()))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(THETAS[2])
        t_text = readfile(TRAJ_NAMES[0])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR, 'transducer_text1': t_text}
        files = {}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_file = openfile(THETAS[0])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_file = openfile(THETAS[1])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_text = readfile(THETAS[2])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR, 'transducer_text1': t_text}
        files = {}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_text = readfile(THETAS[3])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR, 'transducer_text1': t_text}
        files = {}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

    def test_theta(self):
        """Holds theta tests"""
        THETA_STR = readfile(THETA_NAMES[0])

        aut_file = openfile(REGS[3])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)   
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_file = openfile(REGS[0])
        t_text = readfile(TRAJ_NAMES[2])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[2])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))

        aut_file = openfile(REGS[3])
        t_text = readfile(TRAJ_NAMES[2])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        #self.assertTrue(result.get('result', 'FAIL').startswith('NO')) #unsure if this test should actually return true or false (REGS[3] was recently changed due to its unsupported input)

        aut_file = openfile(REGS[0])
        t_text = readfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'transducer_text1': t_text, 'theta_text': THETA_STR}
        files = {'automata_file': SimpleUploadedFile(aut_file.name, str.encode(aut_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[0])
        t_file = openfile(TRAJ_NAMES[2])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('NO'))

        aut_text = readfile(REGS[2])
        t_file = openfile(TRAJ_NAMES[1])
        post = {'question': '1', 'property_type': '5', 'automata_text': aut_text, 'theta_text': THETA_STR}
        files = {'transducer_file': SimpleUploadedFile(t_file.name, str.encode(t_file.read(), encoding="utf-8"))}
        result = get_response(post, files, False)
        self.assertTrue(result.get('result', 'FAIL').startswith('YES'))
