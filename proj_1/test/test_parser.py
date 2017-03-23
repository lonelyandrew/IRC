#! /usr/local/bin Python3

import unittest
from proj_1.bool_re.parser import CommandParser
from proj_1.bool_re.token import TokenParser
from proj_1.iitable.iitable import fetch_iitable
from collections import deque
from proj_1.bool_re.errors import CommandSyntaxError


class TestParser(unittest.TestCase):
    '''Test the CommandParser class.
    '''

    def setUp(self):
        '''Set up the iitable.
        '''
        self.iitable = fetch_iitable()

    def test_init(self):
        '''Test CommandParser.__init__ method.
        '''
        parser = CommandParser(self.iitable)

        self.assertIsNone(parser.command)
        self.assertEqual(len(parser.token_list), 0)
        self.assertEqual(self.iitable, parser.iitable)

        command = 'a & the'
        parser = CommandParser(self.iitable, command)
        self.assertEqual(parser.command, command)

        with self.assertRaises(ValueError) as value_error:
            parser = CommandParser(None)
        self.assertEqual(str(value_error.exception), 'invalid iitable.')

    def test_primary_item(self):
        '''Test CommandParser.parse_primary_item method
        '''
        command = 'a & the'
        parser = CommandParser(self.iitable, command)

        token_parser = TokenParser(command)
        token_parser.parse()
        parser.token_list = deque(token_parser.token_list)

        item = parser.parse_primary_item()
        self.assertEqual(item.word, 'a')
        self.assertEqual(item.freq, 3)

        item = parser.parse_primary_item()
        self.assertIsNone(item)
        self.assertEqual(len(parser.token_list), 3)

        parser.token_list.popleft()

        item = parser.parse_primary_item()
        self.assertEqual(item.word, 'the')
        self.assertEqual(item.freq, 3)
        self.assertEqual(len(parser.token_list), 1)

        command = 'a & (a | the)'
        parser.command = command

        token_parser = TokenParser(command)
        token_parser.parse()
        parser.token_list = deque(token_parser.token_list)

        parser.token_list.popleft()
        parser.token_list.popleft()

        item = parser.parse_primary_item()
        self.assertEqual(item.word, 'a OR the')
        self.assertEqual(item.freq, 3)

        command = '(a ^ the) & the'
        parser.command = command
        token_parser = TokenParser(command)
        token_parser.parse()
        parser.token_list = deque(token_parser.token_list)

        item = parser.parse_primary_item()
        self.assertEqual('a AND NOT the', item.word)
        self.assertEqual(item.freq, 0)

        command = '(a ^ the'
        parser.command = command
        token_parser = TokenParser(command)
        token_parser.parse()
        parser.token_list = deque(token_parser.token_list)

        with self.assertRaises(CommandSyntaxError) as error:
            parser.parse_primary_item()
        self.assertEqual(str(error.exception), 'No right parentheses.')
