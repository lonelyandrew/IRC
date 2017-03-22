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

    def test_parse(self):
        '''Test TokenParser.parse method.
        '''
        parser = TokenParser('a the dog')
        parser.parse()
        token = TokenParser.Token('athedog', TokenParser.TokenKind.WORD_TOKEN)
        token_end = TokenParser.Token('\0', TokenParser.TokenKind.EOL_TOKEN)
        result = [token, token_end]
        self.assertSequenceEqual(parser.token_list, result)

        parser.command = 'a&the'
        parser.parse()
        token_a = TokenParser.Token('a', TokenParser.TokenKind.WORD_TOKEN)
        token_and = TokenParser.Token('&', TokenParser.TokenKind.AND_TOKEN)
        token_the = TokenParser.Token('the', TokenParser.TokenKind.WORD_TOKEN)
        result = [token_a, token_and, token_the, token_end]
        self.assertSequenceEqual(parser.token_list, result)

        parser.command = '(a | the ^ dog)'
        parser.parse(overwrite=False)
        token_dog = TokenParser.Token('dog', TokenParser.TokenKind.WORD_TOKEN)
        l_par_kind = TokenParser.TokenKind.LEFT_PAREN_TOKEN
        r_par_kind = TokenParser.TokenKind.RIGHT_PAREN_TOKEN
        token_lpar = TokenParser.Token('(', l_par_kind)
        token_rpar = TokenParser.Token(')', r_par_kind)
        token_or = TokenParser.Token('|', TokenParser.TokenKind.OR_TOKEN)
        token_not = TokenParser.Token('^', TokenParser.TokenKind.NOT_TOKEN)
        result += [token_lpar, token_a, token_or, token_the, token_not,
                   token_dog, token_rpar, token_end]
        self.assertSequenceEqual(parser.token_list, result)

        parser.command = 'a ? the'
        with self.assertRaises(ValueError) as value_error:
            parser.parse()

        error_message = 'Unknown Character: ?.'
        self.assertEqual(str(value_error.exception), error_message)

        del parser.command
        self.assertFalse(hasattr(parser, '_command')) 
