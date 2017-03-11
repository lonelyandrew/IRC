#! /usr/local/bin Python3

import unittest
from proj_1.bool_re.bool_re import parser
from proj_1.bool_re.errors import CommandSyntaxError


class TestBoolRe(unittest.TestCase):
    '''Test functions and classes in module bool_re.
    '''

    def test_parser(self):
        command = 'A and B'
        tokens = parser(command)
        test_tokens = [('a', 'operand'), ('&', 'operator'), ('b', 'operand')]
        self.assertSequenceEqual(tokens, test_tokens)

        command = 'A or B'
        tokens = parser(command)
        test_tokens = [('a', 'operand'), ('|', 'operator'), ('b', 'operand')]
        self.assertSequenceEqual(tokens, test_tokens)

        command = 'A and not B'
        tokens = parser(command)
        test_tokens = [('a', 'operand'), ('^', 'operator'), ('b', 'operand')]
        self.assertSequenceEqual(tokens, test_tokens)

        command = 'A! and B'
        with self.assertRaises(CommandSyntaxError):
            tokens = parser(command)

        with self.assertRaises(ValueError):
            parser('')

        with self.assertRaises(ValueError):
            parser(None)
