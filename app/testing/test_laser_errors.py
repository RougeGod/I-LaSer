from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile, readfile, create_file_dictionary, exec_program
from unittest import skipIf
from FAdo.common import PropertyNotSatisfied
import re

'''This module tests for graceful error handling of invalid input to LaSer'''

TEST_FILES_FA = ["test_files/NFA-a(aa)#.fa", "test_files/error/MultipleFA.fa", "test_files/DFA-a+ab+bb.txt"]
#the first one shouldn't satisfy any code property

#trajectories and transducers
TRAJ_FILES = ['test_files/0#1#0#.traj', 'test_files/1#0#.traj', "test_files/P-infix-ipt.fa", "test_files/construction/TR-sub1.01.fa", "test_files/TR-sub1.ab.fa"]

CONSTRUCTION_DEFAULTS = {"s_int": "4", "l_int": "4", "n_int": "4"}
AMAX_DEFAULTS = {"epsilon": "0.05", "dirichletT": "2.001", "displacement": "1"}



class MyTestCase(TestCase):

    #test for input-preserving properties when input altering property is selected
    def test_IAPwhenIPP(self):
        post = {"question": "1", "property_type": "2"}
        files = create_file_dictionary(TEST_FILES_FA[2], TRAJ_FILES[4])
        result = get_response(post, files, False)
        self.assertTrue(result["error_message"].startswith("This is an input-preserving"))
        

    #test AMAX without required parameters or out of range parameters
    def test_AMAX_badParams(self):
        post = {"question": "4", "property_type": "1", "fixed_type": "2"}
        files = create_file_dictionary(TEST_FILES_FA[2], TRAJ_FILES[4])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Invalid Approximation Parameters")

        post = {"question": "4", "property_type": "1", "fixed_type": "2", "dirichletT": "0.5",
                "displacement": "0", "epsilon": "0.05"} #too small T
        files = create_file_dictionary(TEST_FILES_FA[2], TRAJ_FILES[4])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Invalid Approximation Parameters")

        post = {"question": "4", "property_type": "1", "fixed_type": "2", "dirichletT": "2.001",
                "displacement": "-2", "epsilon": "0.05"} #negative displacement
        files = create_file_dictionary(TEST_FILES_FA[2], TRAJ_FILES[4])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Invalid Approximation Parameters")

        post = {"question": "4", "property_type": "1", "fixed_type": "2", "dirichletT": "2.001",
                "displacement": "0", "epsilon": "12"} #too large epsilon
        files = create_file_dictionary(TEST_FILES_FA[2], TRAJ_FILES[4])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Invalid Approximation Parameters")
        

    #test for non-satisfaction raising error on (approximate) maximality for UD code, bifix Code, trajectory, transducer, theta
    def test_propertyNotSatisfied(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "ERROR: The language does not satisfy the property.")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '3'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "ERROR: The language does not satisfy the property.")

        post = {'question': '4', 'property_type': '1', 'fixed_type': '3'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "ERROR: The language does not satisfy the property.")

    #same thign, but for code generation. Because this is an error with calculation,
    #it should still generate the code, but that code should fail
    def test_propertyNotSatisfiedGEN(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '5'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        with self.assertRaises(PropertyNotSatisfied):
            exec_program(post, files)

        post = {'question': '2', 'property_type': '2'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[0])
        with self.assertRaises(PropertyNotSatisfied):
            exec_program(post, files)

        post = {'question': '4', 'property_type': '1', 'fixed_type': "7"} | AMAX_DEFAULTS
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = exec_program(post, files)
        self.assertEquals(result["answer"], "Property not satisfied.")



#test caret operator invalid (multiple)
    def test_RegexCaretMisplaced(self):
        post = {"question": "1", "property_type": "1", "fixed_type": "2", "automata_text": "6^(90)"}
        files = {}
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Could not find the number of repititions.")

        post = {"question": "1", "property_type": "1", "fixed_type": "2", "automata_text": "64^a"}
        files = {}
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Could not find the number of repititions.")

        post = {"question": "1", "property_type": "1", "fixed_type": "2", "automata_text": "76)^5"}
        files = {}
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Could not find the matching left bracket.")

#test for the automaton's alphabet not being a subset of the transducer's
    def test_constructionAlphabetSymbolMismatch(self):
        post = {"question": "3", "property_type": "3", "s_int": "2", "l_int": "2", "n_int": "4"}
        files = create_file_dictionary(trans_file=TRAJ_FILES[2])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "The transducer's alphabet does not match the construction alphabet.")

    #test construction with an S that's too large for the transducer
    def test_constructionAlphabetSizeMismatch(self):
        post = {"question": "3", "property_type": "3"} | CONSTRUCTION_DEFAULTS
        files = create_file_dictionary(trans_file=TRAJ_FILES[3])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "The construction alphabet is larger than the transducer's alphabet.")
    
    @skipIf(True, "Getting generated code to check construction alphabets is a problem for the future")
    def test_constructionAlphabetMismatches_GEN(self):
        post = {"question": "3", "property_type": "3", "s_int": "2", "l_int": "2", "n_int": "4"}
        files = create_file_dictionary(trans_file=TRAJ_FILES[3])
        result = exec_program(post, files)
        self.assertEquals(result["answer"], "The construction alphabet is larger than the transducer's alphabet.")

    #test for not having a question or having question 0 selected
    #question 0 does not produce a result, result is left as None
    def test_noQuestion(self):
        post = {"property_type": "2"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[2])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please select a question.")

        post = {"property_type": "1", "fixed_type": "2", "question": "5"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[3])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please select a question.")

        post = {"property_type": "1", "fixed_type": "2", "question": "0"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[3])
        result = get_response(post, files, False)
        self.assertEquals(result, None)

    #test prop-type == 0 / no prop-type, everything else fine (one for each question)
    def test_noProperty(self):
        post = {"question": "1", "property_type": "0", 'fixed_type': "5"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please provide a property.")

        post = {"question": "1"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[1])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please select a property type.")

    #test prop-type > 5 or non-implemented proptype/question combinations
    #more theoretical and really shouldn't be triggered by use of the website or app, but it is possible for client to
    #manipulate JS, or maybe send raw POST requests, so have something in those cases
    def test_propertyTooHigh(self):
        post = {'question': '1', 'property_type': '6', 'fixed_type': '7'} #fixed type is here and valid but shouldn't matter
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[2])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please select a property type.")

        #more interesting, Django does not auto-drop these properties since they're legal for other questions
        post = {'question': '2', 'property_type': '5', 'fixed_type': '3', "theta_text": readfile("test_files/theta-dna.fa")}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "This feature has not yet been implemented.") #if adding maximality of theta-properties, remove this test.

        post = {'question': '3', 'property_type': '5', 'n_int': 5, 'l_int': 8, 's_int': 2}
        files = create_file_dictionary(trans_file=TRAJ_FILES[1], theta_file="test_files/theta-dna.fa")
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "This feature has not yet been implemented.")

#test prop-type == 1, no fixed type (with and without transducer)
    def test_noFixedType(self):
        post = {"question": "1", "property_type": "1"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Error creating property.")

    #test epsilon transition in DFA (epsilon transitions are only for nondeterministic automata)
    def test_epsilonDFA(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '6',
                'automata_text': readfile("test_files/error/EpsilonDFA.fa")}
        files = {}
        result = get_response(post, files, False)
        self.assertEquals(result['error_message'], "This should be an NFA, not a DFA.")

    #similar to previous. NFAs may have more than one state transition per input symbol, but
    #DFAs may not.
    def test_nondeterministicDFA(self):
        post = {'question': '1', 'property_type': '1', 'fixed_type': '7',
                'automata_text': readfile("test_files/error/NondeterministicDFA.fa")}
        files = {}
        result = get_response(post, files, False)
        self.assertEquals(result['error_message'], "This should be an NFA, not a DFA.")

    #user should not be allowed to enter multiple languages in the automaton area
    def test_multipleAutomaton(self):
        post = {'question': '2', 'property_type': "3"}
        files = create_file_dictionary(aut_file = TEST_FILES_FA[1], trans_file=TRAJ_FILES[2])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Only one automaton may be inputted at a time.")
