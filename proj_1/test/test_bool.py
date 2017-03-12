#! /usr/local/bin Python3

import unittest
from proj_1.bool_re.bool_re import BoolRetrieval
from proj_1.bool_re.errors import CommandSyntaxError


class TestBoolRe(unittest.TestCase):
    '''Test functions and classes in module bool_re.
    '''

    def test_parser(self):
        '''Test parser function.
        '''

        bool_re = BoolRetrieval()
        command = 'A and B'
        tokens = bool_re.parser(command)
        test_tokens = [
                ('a', 'operand'),
                ('&', 'operator'),
                ('b', 'operand'),
                ('STOP', 'operator')
        ]
        self.assertSequenceEqual(tokens, test_tokens)

        command = 'A or B'
        tokens = bool_re.parser(command)
        test_tokens = [
                ('a', 'operand'),
                ('|', 'operator'),
                ('b', 'operand'),
                ('STOP', 'operator')
        ]
        self.assertSequenceEqual(tokens, test_tokens)

        command = 'A and not B'
        tokens = bool_re.parser(command)
        test_tokens = [
                ('a', 'operand'),
                ('^', 'operator'),
                ('b', 'operand'),
                ('STOP', 'operator')
        ]
        self.assertSequenceEqual(tokens, test_tokens)

        command = 'A! and B'
        with self.assertRaises(CommandSyntaxError):
            tokens = bool_re.parser(command)

        with self.assertRaises(ValueError):
            bool_re.parser('')

        with self.assertRaises(ValueError):
            bool_re.parser(None)

    def test_execute_cmd(self):
        cmd = 'a and the'
        bool_re = BoolRetrieval()
        tokens = bool_re.parser(cmd)
        print(tokens)
        result = bool_re.execute_command(tokens)
        exe_result = '(a AND the, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(result), exe_result)
