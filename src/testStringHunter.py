#!/usr/bin/python
import StringIO
import argparse
import os
import stringHunter
import unittest

class TestStringHunter(unittest.TestCase):
    def setUp(self):
        self.context = stringHunter.StringHunter()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("rootDirectory")
        self.out = StringIO.StringIO()


    def test_DirectoryDoesNotExist_Error(self):
        args = self.parser.parse_args(["Fake\Directory"])
        self.assertFalse(self.context.hunt(args, self.out))
        self.assertIn("does not exist", self.out.getvalue().strip())


    def test_PassingNonDirectory_Error(self):
        args = self.parser.parse_args([os.path.realpath(__file__)])
        self.assertFalse(self.context.hunt(args, self.out))
        self.assertIn("not a directory", self.out.getvalue().strip())


    def test_ValidDirectory_PrintsMatchedFiles(self):
        args = self.parser.parse_args([os.path.abspath("testFiles")])
        self.assertEqual(5, self.context.hunt(args, self.out)[0])


    def test_ValidDirectory_PrintsMatchedLines(self):
        args = self.parser.parse_args([os.path.abspath("testFiles")])
        self.assertEqual(10, self.context.hunt(args, self.out)[1])
      
      
if __name__ == '__main__':
    unittest.main()