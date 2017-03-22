#! /usr/local/bin Python3

from proj_1.bool_re.token import TokenParser
from proj_1.bool_re.errors import CommandSyntaxError


class CommandParser:
    '''The parser to analyse the query command.
    '''

    def __init__(self, iitable, command=None):
        '''Init the CommandParser object with a command.

        Args:
            iitable: the iitable containing the wordchains
            command: the command of the parser.
        '''

        if not iitable:
            raise ValueError('invalid iitable.')
        self.iitable = iitable
        self.command = command
        self.token_list = []

    def parse_token(self):
        '''Parse the command into token list.

        Returns:
            save the tokens into self.token_list.
        '''
        token_parser = TokenParser(self.command)
        token_parser.parse()
        self.token_list = token_parser.token_list

    def parse(self):
        '''Execute the command which stored in the parser.

        Returns:
            return a result word chain.
        '''
        if not self.token_list:
            self.parse_token()
        value = self.parse_expression()
        return value

    def parse_expression(self):
        '''Calculate the expression.

        Returns:
            return a result word chain.
        '''

        value_left = self.parse_item()

        while True:
            token = self.token_list.popleft()

            if (token.kind != TokenParser.TokenKind.AND_TOKEN and
               token.kind != TokenParser.TokenKind.OR_TOKEN and
               token.kind != TokenParser.TokenKind.NOT_TOKEN):
                self.token_list = [token] + self.token_list
                break

            value_right = self.parse_item()
            if token.kind == TokenParser.TokenKind.AND_TOKEN:
                value_left = value_left.intersection(value_right)
            elif token.kind == TokenParser.TokenKind.OR_TOKEN:
                value_left = value_left.union(value_right)
            elif token.kind == TokenParser.TokenKind.NOT_TOKEN:
                value_left = value_left.diff(value_right)

        return value_left

    def parse_primary_item(self):
        '''Parse the primary word chain.

        Returns:
            return a word chain which parsed from the self.token_list.
        '''
        token = self.token_list.popleft()

        if token.kind == TokenParser.TokenKind.WORD_TOKEN:
            return self.iitable[token.literal]
        elif token.kind == TokenParser.TokenKind.LEFT_PAR_TOKEN:
            value = self.parse_expression()
            token = self.token_list.popleft()
            if token.kind == TokenParser.TokenKind.RIGHT_PAREN_TOKEN:
                return value
            else:
                raise CommandSyntaxError('No right parentheses.')
        else:
            self.token_list = [token] + self.token_list
            return None
