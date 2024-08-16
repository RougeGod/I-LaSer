from django.test import TestCase
from app.transducer.expand_carets import expand_carets

inputs = ["5^35", "(a+b)^2", "hello^2", "((x+y)^2+z)^2", "33^4",
          "a^1", "(x^2+y)^3", "0^5", "(1+2+3)^2", "a^0",
          "^2",  "a^^2", "(abc)^1", "((a+b)^2)^2", "abc^",
          "3^a", "((x+y)^)^2", "hello^2bob", "(a+b^3)^2", "a^1b^2c^3",
          "a^3^2", "2^(3^2)", "(a^2)^2", "x^2y^3"]

outputs = ["5" * 35, "(a+b)(a+b)", "helloo", "((x+y)(x+y)+z)((x+y)(x+y)+z)", "33333",
           "a", "(xx+y)(xx+y)(xx+y)", '00000', "(1+2+3)(1+2+3)", "",
           "ERROR", "ERROR", "(abc)", "((a+b)(a+b))((a+b)(a+b))", "ERROR",
           "ERROR", "ERROR", "helloobob", "(a+bbb)(a+bbb)", "abbccc",
           "aaaa", "ERROR", "(aa)(aa)", "xxyyy"]

class TestExpansion(TestCase):
    def test_nonbracket(self):
        for test in (0, 2, 4, 5, 7, 9, 17, 19, 20, 23):
            self.assertEqual(expand_carets(inputs[test]), outputs[test])

    def test_brackets(self):
        for test in (1, 3, 6, 8, 12, 13, 18, 22):
            self.assertEqual(expand_carets(inputs[test]), outputs[test])

    def test_errors(self):
        for test in (10, 11, 14, 15, 16, 21):
            with self.assertRaises(ValueError):
                expand_carets(inputs[test])

if __name__ == "__main__":
    unittest.main()