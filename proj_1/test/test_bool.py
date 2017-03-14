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

        cmd = 'a and 60'
        bool_re = BoolRetrieval(command=cmd)
        result = bool_re.execute_command()
        exe_result = '(a AND 60, freq:1) * --> 3'
        self.assertEqual(str(result), exe_result)

        cmd = 'a or the'
        bool_re = BoolRetrieval(command=cmd)
        result = bool_re.execute_command()
        exe_result = '(a OR the, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(result), exe_result)

        cmd = 'a and not the'
        bool_re = BoolRetrieval(command=cmd)
        result = bool_re.execute_command()
        exe_result = '(a AND NOT the, freq:0) *'
        self.assertEqual(str(result), exe_result)

        bool_re.cmd = ''
        with self.assertRaises(ValueError):
            bool_re.execute_command()

        bool_re.cmd = None
        with self.assertRaises(ValueError):
            bool_re.execute_command()

        bool_re.cmd = 'and w b'
        with self.assertRaises(CommandSyntaxError):
            bool_re.execute_command()

        bool_re.cmd = 'w b and'
        with self.assertRaises(CommandSyntaxError):
            bool_re.execute_command()

        bool_re.cmd = 'a and the the'
        with self.assertRaises(CommandSyntaxError):
            bool_re.execute_command()

        bool_re.cmd = 'a and and'
        with self.assertRaises(CommandSyntaxError):
            bool_re.execute_command()

    def test_bin_operation(self):
        '''Test binary_operation method.
        '''
        bool_re = BoolRetrieval()
        operand_one = bool_re.get_table_item('a')
        operand_two = bool_re.get_table_item('the')
        operator = '*'

        with self.assertRaises(CommandSyntaxError):
            bool_re.binary_operation(operand_one, operator, operand_two)

    def test_get_item(self):
        '''Test get_table_item method.
        '''
        bool_re = BoolRetrieval()
        item = bool_re.get_table_item('deepen')

        self.assertEqual(item.word, 'deepen')
        self.assertIs(item.head, None)
        self.assertEqual(item.freq, 0)

        with self.assertRaises(ValueError):
            bool_re.get_table_item('!test')
