#! /usr/local/bin Python3

import unittest
from proj_1.bool_re.bool_re import parser

class TestBoolRe(unittest.TestCase):

    def test_parser(self):
        cmd = 'A AND B AND C'
        cmd_parsed = 'A & B & C'
        self.assertEqual(parser(cmd), cmd_parsed)

        cmd = 'and AND and OR or AND NOT and not'
        cmd_parsed = 'and & and | or ^ and not'
        self.assertEqual(parser(cmd), cmd_parsed)
        
