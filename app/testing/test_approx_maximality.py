from unittest import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile

#testing these is very weird, by their nature, approximate maximality solutions involve
#randomization and will not return the same answer 100% of the time. Tests which depend
#on this randomness are run 20 times each. Tests which depend on randomness have "RNG"
#in their function name, though some tests do not depend on randomness and need only 
#be run once, such as those that are already maximal

NFAs = ["test_files/ApproximatelyMaximalOutfix.fa"]
TRAJs = ["test_files/1#0#+0#1#.traj"]

AMAX_DEFAULTS = {"displacement": '1', "epsilon": "0.03", "dirichletT": "2.0001"}

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
           
    def test_outfix_RNG(self): #about 1 in 1000000 that this fails by pure chance
        def singleOutfixTest(): #approximately 48% chance of single test returning true. 
            aut = openfile(NFAs[0])
            post = {"question": "4", "property_type": "1", "fixed_type": "4"} | AMAX_DEFAULTS
            files = {"automata_file": SimpleUploadedFile(aut.name, str.encode(aut.read(), encoding="utf-8"))}
            result = get_response(post, files, False)
            raise NotImplementedError(result)
            return result["result"].startswith("YES")
        self.assertTrue(self.random_function_repeater(singleOutfixTest))
