#! /usr/local/bin Python3

def parser(command):
    '''Parse the text command into a queue of tokens.

    Args:
        command: A text command whose operands are divided by spaces.

    Returns:
        A list of tokens those are ordered.
    '''
    main_q = []
    branch_q = []
    command = command.strip()
    command = command.replace('AND NOT', '^')
    command = command.replace('AND', '&')
    command = command.replace('OR', '|')

    tokens = command.split(' ')

    return tokens
