#! /usr/local/bin Python3

from enum import Enum, unique, auto


class TokenParser:
    '''The class which can parse one command into a list of tokens.
    '''

    @unique
    class TokenKind(Enum):
        '''The token kind enum.
        '''
        LEFT_PAREN_TOKEN = auto()
        RIGHT_PAREN_TOKEN = auto()
        WORD_TOKEN = auto()
        AND_TOKEN = auto()
        OR_TOKEN = auto()
        DIFF_TOKEN = auto()
        EOL_TOKEN = auto()

    class Token:
        '''The element type of the parser result.
        '''

        def __init__(self, literal=None, kind=None):
            '''Init Class Token with literal and token kind.

            Args:
                literal: the str wich are in the command represent the token.
            '''
            self.literal = literal.strip() if literal is not None else None
            self.kind = kind

        def __str__(self):
            '''Represent toekn object as a str.
            '''
            token_kind = str(self.kind).split('.')[-1]
            return 'Token: {0} | {1}'.format(self.literal, token_kind)

    def __init__(self, command):
        '''Init parser with a command.

        Args:
            command: the command to be parsed.
        '''
        self.command = command.replace(' ', '')
        self.command = self.command.replace('\t', '')
        self.command = self.command.split('\n')[0]
        self.token_list = []

    def parse(self, overwrite=True):
        '''Parse the command.

        Args:
            overwrite: if True, clean the previous token list. Default True.
                       if False, append new tokens into the token list.
        Returns:
            Save the parsed token list into the self.token_list.

        Raises:
            ValueError: if an unknown char occured.
        '''

        word_register = []
        if overwrite:
            self.token_list = []

        for char in self.command:

            token = TokenParser.Token(char)

            if not char.isalnum(char) and len(word_register):
                word = word_register.join('')
                word_token = TokenParser.Token(word)
                word_token.kind = TokenParser.TokenKind.WORD_TOKEN
                self.token_list.append(word_token)

            if char == '(':
                token.kind = TokenParser.TokenKind.LEFT_PAREN_TOKEN
            elif char == ')':
                token.kind = TokenParser.TokenKind.RIGHT_PAREN_TOKEN
            elif char == '&':
                token.kind = TokenParser.TokenKind.AND_TOKEN
            elif char == '|':
                token.kind = TokenParser.TokenKind.OR_TOKEN
            elif char == '^':
                token.kind = TokenParser.TokenKind.DIFF_TOKEN
            elif char.isalnum(char):
                word_register.append(char)
            else:
                raise ValueError('Unknown Character.')

            self.token_list.append(token)
