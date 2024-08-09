from unittest import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile, readfile, create_file_dictionary
import sys

import logging

#testing these is very weird, by their nature, approximate maximality solutions involve
#randomization and will not return the same answer 100% of the time. Tests which depend
#on this randomness are run 20 times each. Tests which depend on randomness have "RNG"
#in their function name, though some tests do not depend on randomness and need only 
#be run once, such as those that are truly maximal or nowhere near maximal

NFAs = ["test_files/ApproximatelyMaximalOutfix.fa", 'test_files/DFA-a+ab+bb.fa', 'test_files/NFA-aa+ab+ba+bb.fa', 
        'test_files/ApproximatelyMaximalBifix.fa']
TRAJs = ["test_files/1#0#+0#1#.traj"]

AMAX_DEFAULTS = {"displacement": '0', "epsilon": "0.03", "dirichletT": "2.0001"}

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
     
    def test_lowEPS(self):
        post = {"queestion": "4", "fixed_type": ""}

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
        self.assertFalse(result["error_message"])
        
          
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
        self.assertTrue(self.random_function_repeater(singleOutfixTestTraj))

 
    def test_truly_maximal(self):
        post = {'question': '2', 'property_type': '1', 'fixed_type': '5'} #OUTFIX
        files = create_file_dictionary(aut_file=NFAs[2])
        result = get_response(post, files, False)
        self.assertTrue(result['result'].startswith, "Yes,")

    def test_nothing(self):
        return True

        
