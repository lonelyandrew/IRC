#! /usr/local/bin Python3

def parser(command):
    main_q = []
    branch_q = []
    command = command.strip()
    command = command.replace('AND NOT', '^')
    command = command.replace('AND', '&')
    command = command.replace('OR', '|')

    return command
