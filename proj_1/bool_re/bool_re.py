#! /usr/local/bin Python3

def parser(command):
    main_q = []
    branch_q = []
    command.replace('AND NOT', '^')
    command.replace('AND', '&')
    command.replace('OR', '|')

    return command
