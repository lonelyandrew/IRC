#! /usr/local/bin Python3

from proj_1.bool_re.errors import CommandSyntaxError
from proj_1.iitable.iitable import WordChain
from proj_1.iitable.iitable import build_iitable
from proj_1.iitable.iitable import build_sitable
from proj_1.iitable.iitable import doc_loc
from proj_1.iitable.iitable import process_doc


class BoolRetrieval:
    '''Excute boolean retrieval with a command and a iitable.
    '''

    def __init__(self, command=None):
        '''Init the BoolRetrieval class.
        '''
        self.iitable = None
        self.cmd = command
        self.tokens = None

    def parse(self):
        '''Parse the text self.cmd into a queue of tokens.

        Raises:
            ValueError: when the self.cmd is absent.
            CommandSyntaxError: when the token is not alphanumeric.
        '''

        if not self.cmd:
            raise ValueError('Please feed a correct self.cmd.')

        operators = ['START', 'STOP', '&', '|', '^']
        self.cmd = self.cmd.lower()
        self.cmd = self.cmd.strip()
        self.cmd = self.cmd.replace('(', ' LEFT')
        self.cmd = self.cmd.replace(')', ' RIGHT')
        self.cmd = self.cmd.replace('and not', ' ^ ')
        self.cmd = self.cmd.replace('and', ' & ')
        self.cmd = self.cmd.replace('or', ' | ')

        tokens = self.cmd.split(' ')
        tokens = list(filter(lambda x: x != '', tokens))

        final_tokens = []
        for token in tokens:
            if token in operators:
                final_tokens.append((token, 'operator'))
            else:
                if token.isalnum():
                    final_tokens.append((token, 'operand'))
                else:
                    raise CommandSyntaxError('')
        final_tokens.append(('STOP', 'operator'))
        self.tokens = final_tokens

    def execute_command(self):
        '''Execute command in form of tokens.

        Args:
            tokens: A list of tokens of command.

        Return:
            The result of excution, normally a word chain.

        Raises:
            CommandSyntaxError: An CommandSyntaxError occurred when there is a
                syntax error in the command.
            ValueError: An ValueError occured when there is no command to
                execute.
        '''
        operator = None
        left_chain = None
        right_chain = None

        if not self.cmd:
            raise ValueError('Please feed a command.')
        if self.tokens is None:
            self.parse()
        for token in self.tokens:
            if left_chain is None and token[1] == 'operand':
                left_chain = self.get_table_item(token[0])
            elif left_chain is None and token[1] != 'operand':
                raise CommandSyntaxError('')
            elif operator is None and token[1] == 'operator':
                operator = token[0]
            elif operator is None and token[1] != 'operator':
                raise CommandSyntaxError('')
            elif right_chain is None and token[1] == 'operand':
                right_chain = self.get_table_item(token[0])
            elif right_chain is None and token[1] != 'operand':
                raise CommandSyntaxError('')
            elif token[1] == 'operator':
                left_chain = BoolRetrieval.binary_operation(
                        left_chain, operator, right_chain)
                right_chain = None
                operator = token[0]
            else:
                raise CommandSyntaxError('')

        return left_chain

    @staticmethod
    def binary_operation(operand_one, operator, operand_two):
        '''Excute binary operation.

        Args:
            operand_one: The first operand.
            operator: Operator has three options: ^, |, and &.
            operand_two: The second operand.

        Returns:
            A chain contains operating results.

        Raises:
            An CommandSyntaxError occurred when there is a
            syntax error in the command.
        '''

        if operator == '^':
            return WordChain.diff(operand_one, operand_two)
        elif operator == '|':
            return operand_one.union(operand_two)
        elif operator == '&':
            return WordChain.intersection(operand_one, operand_two)
        else:
            raise CommandSyntaxError('')

    @staticmethod
    def get_iitable():
        '''Build the inverted index table.

        Returns:
            An iitable.
        '''
        doc_path_list = []
        for i in range(3):
            doc_path_list.append(doc_loc(i+1))
        doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
        iitable = build_iitable(build_sitable(doc_list))
        return iitable

    def get_table_item(self, word):
        '''Get the word item in iitable.

        Args:
            word: The key of the item.

        Returns:
            A WordChain instance hold the word.

        Raises:
            ValueError: If the word is not in the table and not alphanumeric.
        '''
        if self.iitable is None:
            self.iitable = BoolRetrieval.get_iitable()
        if word in self.iitable:
            return self.iitable[word]
        elif word.isalnum():
            return WordChain(word)
        else:
            raise ValueError('The word is not alphanumeric.')
