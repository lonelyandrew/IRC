#! /usr/local/bin Python3

from iitable import

debug = True

def excute_command(iv_table, command):
    if not debug:
        if iv_table is None:
            raise ValueErro('The Inverted Index Table should not be None.')
    main_q = []
    branch_q = []
    command.replace('AND NOT', '^')
    command.replace('AND', '&')
    command.replace('OR', '|')
    print(command)

def bi_and(chain_one, chain_two):
    

def bi_or(chain_one, chain_two):
    pass

def bi_not_and(chain_one, chain_two):
    pass

if __name__ == '__main__':
    doc_list = (process_doc(doc_loc(i), i) for i in range(1, 4))

    sorted_table = build_sorted_index_table(doc_list)
    iv_table = build_inverted_index_table(sorted_table)

    chain_one = random.choice(iv_table.items())[1]
    print(chain_one)
    chain_two = random.choice(iv_table.items())[1]
    while chain_one.word == chain_two.word:
        chain_two = random.choice(iv_table.items())[1]
    print(chain_two)
    print(WordChain.diff(chain_one, chain_two))
