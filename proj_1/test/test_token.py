#! /usr/local/bin Python3

import unittest
from proj_1.bool_re.token import TokenParser

class TestTokenParser(unittest.TestCase):
    '''Test the TokenParser class.
    '''

    def test_token(self):
        '''Test the nested class Token.
        '''

        token = TokenParser.Token()
        self.assertIsNone(token.literal)
        self.assertIsNone(token.kind)

        token = TokenParser.Token('test')
        self.assertEqual(token.literal, 'test')
        self.assertIsNone(token.kind)

        token = TokenParser.Token('test', TokenParser.TokenKind.WORD_TOKEN)
        self.assertIs(token.kind, TokenParser.TokenKind.WORD_TOKEN)

        token_str = 'Token: test | WORD_TOKEN'
        self.assertEqual(str(token), token_str)

    def test_parser_init(self):
        '''Test TokenParser constructor.
        '''

        command = 'a  & \t the \n | test'
        command_str = 'a&the'
        parser = TokenParser(command)
        self.assertEqual(parser.command, command_str)
        self.assertEqual(len(parser.token_list), 0)



