#! /usr/local/bin Python3

import unittest
from proj_1.bool_re.bool_re import BoolRetrieval
from proj_1.bool_re.errors import CommandSyntaxError


class TestBoolRe(unittest.TestCase):
    '''Test functions and classes in module bool_re.
    '''

    def test_parse(self):
        '''Test parse method.
        '''

        command = 'A and B'
        bool_re = BoolRetrieval(command=command)
        bool_re.parse()
        test_tokens = [
                ('a', 'operand'),
                ('&', 'operator'),
                ('b', 'operand'),
                ('STOP', 'operator')
        ]
        self.assertSequenceEqual(bool_re.tokens, test_tokens)

        bool_re.cmd = 'A or B'
        bool_re.parse()
        test_tokens = [
                ('a', 'operand'),
                ('|', 'operator'),
                ('b', 'operand'),
                ('STOP', 'operator')
        ]
        self.assertSequenceEqual(bool_re.tokens, test_tokens)

        bool_re.cmd = 'A and not B'
        bool_re.parse()
        test_tokens = [
                ('a', 'operand'),
                ('^', 'operator'),
                ('b', 'operand'),
                ('STOP', 'operator')
        ]
        self.assertSequenceEqual(bool_re.tokens, test_tokens)

        bool_re.cmd = 'A! and B'
        with self.assertRaises(CommandSyntaxError):
            bool_re.parse()

        bool_re.cmd = ''
        with self.assertRaises(ValueError):
            bool_re.parse()

        bool_re.cmd = None
        with self.assertRaises(ValueError):
            bool_re.parse()

    def test_execute_cmd(self):
        '''Test execute_command method.
        '''
        cmd = 'a and the'
        bool_re = BoolRetrieval(command=cmd)
        result = bool_re.execute_command()
        exe_result = '(a AND the, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(result), exe_result)
