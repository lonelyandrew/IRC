#! /usr/bin/env python3

import re
import pandas as pd
import random


class WordChain(object):
    '''The element in inverted index table that hold a word.

    Attributes:
        word: The word of the chain.
        freq: How many docs that the word appear, namely frequence.
        head: The first node in the Chain.
    '''

    def __init__(self, word, freq=0):
        '''Inits the chain with a word.
        '''
        self.word = word
        self.freq = freq
        self.head = None

    def insert_node(self, node):
        '''Insert a node into the chain.

        Args:
            node: The node that will be inserted.
        '''
        if self.head is None:
            self.head = node
        else:
            prev = self.head
            while prev.next is not None:
                prev = prev.next
            prev.next = node
        self.freq += 1

    def union(chain_one, chain_two):
        node_one = chain_one.head
        node_two = chain_two.head
        merged_word = '%s AND %s' % (chain_one.word, chain_two.word)
        merged_chain = WordChain(merged_word)
        tail = merged_chain.head

        while node_one is not None and node_two is not None:
            merged_chain.freq += 1
            min_node = min(node_one, node_two)
            new_node = WordChain.node(min_node.doc_id)
            if tail is None:
                merged_chain.head = new_node
            else:
                tail.next = new_node
            tail = new_node
            if node_one < node_two:
                node_one = node_one.next
            elif node_one > node_two:
                node_two = node_two.next
            else:
                node_one = node_one.next
                node_two = node_two.next

        if node_one is not None or node_two is not None:
            node_remain = node_one if node_two is None else node_two
            while node_remain is not None:
                merged_chain.freq += 1
                new_node = WordChain.node(node_remain.doc_id)
                if tail is None:
                    merged_chain.head = new_node
                else:
                    tail.next = new_node
                tail = new_node
                node_remain = node_remain.next
        print('* ' * 40)
        return merged_chain

    def intersection(chain_one, chain_two):
        node_one = chain_one.head
        node_two = chain_two.head
        merged_word = '%s OR %s' % (chain_one.word, chain_two.word)
        merged_chain = WordChain(merged_word)
        tail = merged_chain.head

        while (node_one is not None) and (node_two is not None):
            if node_one == node_two:
                merged_chain.freq += 1
                new_node = WordChain.node(node_one.doc_id)
                if tail is None:
                    merged_chain.head = new_node
                else:
                    tail.next = new_node
                    tail = new_node
            if node_one > node_two:
                node_two = node_two.next
            elif node_one < node_two: 
                node_one = node_one.next
            else:
                node_one = node_one.next
                node_two = node_two.next

        return merged_chain

    def difference(chain_one, chain_two):
        pass

    def __str__(self):
        chain_str = '(%s, freq:%d) O' % (self.word, self.freq)
        if self.head is not None:
            node_to_print = self.head
            while node_to_print is not None:
                chain_str += ' --> '
                chain_str += str(node_to_print)
                node_to_print = node_to_print.next
        return chain_str

    class node(object):
        '''The nested class acts as a node in the chain.

        Attributes:
            doc_id: The id the doc which contains the word.
            next: The next node in the chain, if the node is at the end of the
                 chain, it will be None.
        '''

        def __init__(self, doc_id=0):
            '''Inits the node with the doc id.
            '''
            self.doc_id = doc_id
            self.next = None

        def __str__(self):
            return str(self.doc_id)

        def __cmp__(self, other):
            return self.doc_id - other.doc_id


def process_doc(doc_location, doc_id):
    '''Process the single doc into pairs of word and doc id.

    Args:
        doc_location: The location of the doc.
        doc_id: The id of the doc.

    Yields:
       word: The word appears in the doc.
       doc_id: The id of the doc.
    '''

    word_list = set()
    p = re.compile('[^\W_]+')
    with open(doc_location) as doc:
        for line in doc:
            word_list.update(p.findall(line.lower()))
    for word in word_list:
        yield word, doc_id


def build_sorted_index_table(doc_list):
    '''Generate sorted index table with multilple docs.

    Args:
        doc_list: A list contains several process_doc generator.

    Yields:
       row: The single row of the sorted index table.
    '''
    item_df = pd.DataFrame()
    for doc in doc_list:
        df = pd.DataFrame(doc)
        item_df = item_df.append(df, ignore_index=True)
    item_df.columns = ['term', 'id']
    item_df.sort_values(['term', 'id'], inplace=True)
    for row in item_df.itertuples(index=False, name=None):
        yield row


def build_inverted_index_table(sorted_table):
    '''Build the inverted index table with a sorted table.

    Args:
        sorted_table: The sorted table built before with docs.

    Returns:
        A dict whose keyis are words and the value of the
        single key is a word chain.
    '''
    iv_table = {}
    for word, doc_id in sorted_table:
        if word not in iv_table:
            iv_table[word] = WordChain(word)
        node = WordChain.node(doc_id)
        iv_table[word].insert_node(node)
    return iv_table


def doc_loc(doc_id):
    '''Get the location of the doc with certain id.

    Args:
        doc_id: The id of the doc, normally which is a number.

    Returns:
       A string of the absolute path to the doc file.
    '''
    return ('/Users/andrewshi/Codes/Github/IRC/data/pp/pp_%s.txt' % doc_id)


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
    print(WordChain.intersection(chain_one, chain_two))
