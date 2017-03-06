#! /usr/local/bin Python3

debug = True


def excute_command(iv_table, command):
    if not debug:
        if iv_table is None:
            raise ValueError('The Inverted Index Table should not be None.')
    main_q = []
    branch_q = []
    command.replace('AND NOT', '^')
    command.replace('AND', '&')
    command.replace('OR', '|')
    print(command)


def bi_and(chain_one, chain_two):
    pass


def bi_or(chain_one, chain_two):
    pass


def bi_not_and(chain_one, chain_two):
    pass


if __name__ == '__main__':
    pass
