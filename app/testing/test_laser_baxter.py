from unittest import TestCase, skipIf
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile, readfile, create_file_dictionary, exec_program
import sys

import logging

#testing these is very weird, by their nature, approximate maximality solutions involve
#randomization and will not return the same answer 100% of the time. Tests which depend
#on this randomness are run 20 times each. Tests which depend on randomness have "RNG"
#in their function name, though some tests do not depend on randomness and need only
#be run once, such as those that are truly maximal or nowhere near maximal

NFAs = ["test_files/ApproximatelyMaximalOutfix.fa", 'test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa',
        'test_files/ApproximatelyMaximalBifix.fa']
TRAJs = ["test_files/1#0#+0#1#.traj", "test_files/P-suffix.fa"]

AMAX_DEFAULTS = {"displacement": '0', "epsilon": "0.03", "dirichletT": "2.0001"}

SKIP_LONG_TESTS = True #if you mess with approximate maximality, set this to False, but otherwise leave it

class MyTestCase(TestCase):

    #runs function "func"" up to 20 times, looking for at least one "true" and one "false"
    #if it gets that, returns true, if not, returns false
    def random_function_repeater(self, func):
        oneTrue = False
        oneFalse = False
        for _ in range(20):
            if func():
                oneTrue = True
            else:
                oneFalse = True
            if oneTrue and oneFalse:
                return True
        return False

    @skipIf(SKIP_LONG_TESTS, "These tests take too long.")
    def test_lowEPS(self): #these should fail with more stringent epsilon == more words checked
        post = {"question": "4", "property_type": "1", "fixed_type": "3", "displacement": "0",
                "dirichletT": "2.0001", "epsilon": "0.0001", "automata_text": readfile(NFAs[3])}
        result = exec_program(post, {})
        self.assertFalse(result['answer'] is None) #make sure that there is a counterexample

        post = {"question": "4", "property_type": "1", "fixed_type": "5", "displacement": "0",
                "dirichletT": "2.0001", "epsilon": "0.0001", "automata_text": readfile(NFAs[0])}
        result = exec_program(post, {})
        self.assertFalse(result['answer'] is None)

    def test_highEPS(self):
        post = {"question": "4", "fixed_type": "5", "property_type": "1", "displacement": "0",
               "dirichletT": "2.0001", "epsilon": "0.3", "automata_text": readfile(NFAs[0])}
        result = get_response(post, {}, False)
        self.assertTrue(result["result"].startswith("Yes"))
        #theoretically this could fail by chance, but it didn't in 1000 attempts

        post = {"question": "4", "fixed_type": "3", "property_type": "1", "displacement": "0",
                "dirichletT": "2.0001", "epsilon": "0.3"}
        files = create_file_dictionary(aut_file=NFAs[3])
        result = get_response(post, files, False)
        self.assertTrue(result["result"].startswith("Yes"))

    @skipIf(SKIP_LONG_TESTS, "RNG test that takes forever")
    def test_bifixRNG(self):
        def singleBifixTest(): #approximately 73% chance of single test returning true.
            post = {"question": "4", "property_type": "1", "fixed_type": "3", "epsilon": "0.0015",
                    "displacement": "0", "dirichletT": "2.001"}
            files = create_file_dictionary(NFAs[3])
            result = get_response(post, files, False)
            return result["result"].startswith("Yes")
        self.assertTrue(self.random_function_repeater(singleBifixTest))



    def test_outfix_RNG(self): #about 1 in 1000000 that this fails by pure chance (with new prax)
        def singleOutfixTest(): #approximately 48% chance of single test returning true.
            post = {"question": "4", "property_type": "1", "fixed_type": "5"} | AMAX_DEFAULTS
            files = create_file_dictionary(NFAs[0])
            result = get_response(post, files, False)
            return result["result"].startswith("Yes")
        self.assertTrue(self.random_function_repeater(singleOutfixTest))

    def outfixTestTraj_RNG(self): #same as previous test but trajectory instead of fixed type
        def singleOutfixTrajTest():
            post = {"question": "4", "property_type": "2", "transducer_text": "0*1*0*"} | AMAX_DEFAULTS
            files = create_file_dictionary(NFAs[0])
            result = get_response(post, files, False)
            return result["result"].startswith("Yes")
        self.assertTrue(self.random_function_repeater(singleOutfixTrajTest))




    def test_truly_maximal(self):
        post = {'question': '4', 'property_type': '1', 'fixed_type': '5'} | AMAX_DEFAULTS #OUTFIX
        files = create_file_dictionary(aut_file=NFAs[2])
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith("Yes"))

        post = {'question': '4', 'property_type': '2', "automata_text": "a+ab+bb"} | AMAX_DEFAULTS
        files = create_file_dictionary(trans_file=TRAJs[1])
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith("Yes"))


