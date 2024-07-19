from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile, readfile, create_file_dictionary
import re

'''This module tests for graceful error handling of invalid input to LaSer'''

TEST_FILES_FA = ["test_files/NFA-a(aa)#.fa"]
#the first one shouldn't satisfy any code property

#trajectories and transducers
TRAJ_FILES = ['test_files/0#1#0#.traj', 'test_files/1#0#.traj', "test_files/P-infix-ipt.fa", "test_files/construction/TR-sub1.01.fa"]

class MyTestCase(TestCase):

    #test for non-satisfaction raising error on maximality for UD code, bifix Code, trajectory, transducer, theta
    def test_propertyNotSatisfied(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '6'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "ERROR: The language does not satisfy the property.")

        post = {'question': '2', 'property_type': '1', 'fixed_type': '3'}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "ERROR: The language does not satisfy the property.")

#test caret operator invalid (multiple)

#test for the automaton's alphabet not being a subset of the transducer's

    #test construction with an S that's too large for the transducer
    def test_constructionAlphabetMismatch(self):
        post = {"question": "3", "property_type": "3"}
        files = create_file_dictionary(trans_file=TRAJ_FILES[3])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "The construction alphabet is larger than the transducer's alphabet.")

    #test for not having a question or having question 0 selected
    def test_noQuestion(self):
        post = {"property_type": "2"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[2])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please select a question.")

        post = {"property_type": "1", "fixed_type": "2", "question": "0"}
        files = create_file_dictionary(aut_file=TEST_FILES_FA[0], trans_file=TRAJ_FILES[3])
        result = get_response(post, files, False)
        self.assertEquals(result["error_message"], "Please select a question.")
        
        


#test prop-type == 0 / no prop-type, everything else fine (one for each question)

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
        post = {'question': '2', ''} #TODO