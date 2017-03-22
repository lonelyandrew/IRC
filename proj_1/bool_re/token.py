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
        NOT_TOKEN = auto()
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

        def __eq__(self, other):
            return (self.literal == other.literal and self.kind == other.kind)

    def __init__(self, command):
        '''Init parser with a command.

        Args:
            command: the command to be parsed.
        '''
        self.command = command
        self.token_list = []

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value.replace(' ', '')
        self._command = self._command.replace('\t', '')
        self._command = self._command.split('\n')[0]

    @command.deleter
    def command(self):
        del self._command

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

            if not char.isalnum() and len(word_register):
                word = ''.join(word_register)
                word_register = []
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
                token.kind = TokenParser.TokenKind.NOT_TOKEN
            elif char.isalnum():
                word_register.append(char)
                continue
            else:
                raise ValueError('Unknown Character: {0}.'.format(char))
            self.token_list.append(token)

        if len(word_register):
            word = ''.join(word_register)
            word_token = TokenParser.Token(word)
            word_token.kind = TokenParser.TokenKind.WORD_TOKEN
            self.token_list.append(word_token)

        end_token = TokenParser.Token('\0', TokenParser.TokenKind.EOL_TOKEN)
        self.token_list.append(end_token)
