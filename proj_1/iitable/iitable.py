#! /usr/bin/env python3

import re
import os


class WordChain:
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
        self.tail = None

    def insert_node(self, node):
        '''Insert a node into the chain.

        Args:
            node: The node that will be inserted.

        Raises:
            ValueError: An error occured when the node is None,
                        or the node has a less id compared with the tail,
                        i.e. that the chain must be ordered.
        '''
        if node is None:
            raise ValueError('the inserting node cannot be None.')
        if self.tail is not None and self.tail.doc_id >= node.doc_id:
            raise ValueError('the inserting node have the wrong order.')
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.freq += 1

    def union(self, chain):
        '''Union two word chains.

        Args:
            chain: The chain to be unioned.

        Returns:
            A new chain which united self and chain.

        Raises:
            ValueError: when the chain to be unioned is itself.
        '''

        if self.word == chain.word:
            raise ValueError('the chain cannot be unioned with itself')
        node_one = self.head
        node_two = chain.head
        new_word = '{0!s} OR {1!s}'.format(self.word, chain.word)
        new_chain = WordChain(new_word)

        while (node_one is not None) and (node_two is not None):
            min_node = min(node_one, node_two)
            new_node = min_node.copy()
            new_chain.insert_node(new_node)
            if node_one < node_two:
                node_one = node_one.next
            elif node_one > node_two:
                node_two = node_two.next
            else:
                node_one = node_one.next
                node_two = node_two.next

        node_remain = node_one if node_two is None else node_two
        while node_remain is not None:
            new_node = node_remain.copy()
            new_chain.insert_node(new_node)
            node_remain = node_remain.next
        return new_chain

    def intersection(self, chain):
        '''Intersect two chains.

        Args:
            chain: The chain to be intersected.

        Returns:
            A new chain which intersect self and chain.

        Raises:
            ValueError: when the chain to be intersected is itself.
        '''
        if self.word == chain.word:
            raise ValueError('the chain cannot be intersected with itself')

        node_one = self.head
        node_two = chain.head
        new_word = '{0!s} AND {1!s}'.format(self.word, chain.word)
        new_chain = WordChain(new_word)

        while (node_one is not None) and (node_two is not None):
            if node_one == node_two:
                new_node = node_one.copy()
                new_chain.insert_node(new_node)
                node_one = node_one.next
                node_two = node_two.next
            elif node_one > node_two:
                node_two = node_two.next
            else:
                node_one = node_one.next

        return new_chain

    def diff(self, chain):
        '''Get a complement of chain in self.

        Args:
            chain: the compared chain.

        Returns:
           A new chain have elements which are in self but not in chain.

        Raises:
            ValueError: when the chain to be diffed is itself.
        '''
        if self.word == chain.word:
            raise ValueError('the chain cannot be compared with itself')

        node_one = self.head
        node_two = chain.head
        new_word = '{0!s} AND NOT {1!s}'.format(self.word, chain.word)
        new_chain = WordChain(new_word)

        while (node_one is not None) and (node_two is not None):
            if node_one == node_two:
                node_one = node_one.next
                node_two = node_two.next
            elif node_one < node_two:
                new_node = node_one.copy()
                new_chain.insert_node(new_node)
                node_one = node_one.next
            else:
                node_two = node_two.next

        while node_one is not None:
            new_node = node_one.copy()
            new_chain.insert_node(new_node)
            node_one = node_one.next

        return new_chain

    def __str__(self):
        chain_str = '({0!s}, freq:{1:d}) *'.format(self.word, self.freq)
        if self.head is not None:
            node_to_print = self.head
            while node_to_print is not None:
                chain_str += ' --> '
                chain_str += str(node_to_print)
                node_to_print = node_to_print.next
        return chain_str

    class Node(object):
        '''The nested class acts as a node in the chain.

        Attributes:
            doc_id: The id the doc which contains the word.
            next: The next node in the chain, if the node is at the end of the
                 chain, it will be None.
        '''

        def __init__(self, doc_id: int=0):
            '''Inits the node with an integer doc id.
            '''
            self.doc_id = doc_id
            self.next = None

        def __str__(self):
            return str(self.doc_id)

        def __lt__(self, other):
            return self.doc_id < other.doc_id

        def __gt__(self, other):
            return self.doc_id > other.doc_id

        def __eq__(self, other):
            return self.doc_id == other.doc_id

        def __le__(self, other):
            return self.doc_id <= other.doc_id

        def __ge__(self, other):
            return self.doc_id >= other.doc_id

        def __ne__(self, other):
            return self.doc_id != other.doc_id

        def copy(self):
            '''Return a new node with the same doc id.
            '''
            return WordChain.Node(self.doc_id)


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


def build_sitable(doc_list):
    '''Generate sorted index table with multilple docs.

    Args:
        doc_list: A list contains several process_doc generator.

    Yields:
       row: The single row of the sorted index table.
    '''
    items = []
    for doc in doc_list:
        for word, doc_id in doc:
            items.append((word, doc_id))
    items.sort()
    for item in items:
        yield item[0], item[1]


def build_iitable(sorted_table):
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
        node = WordChain.Node(doc_id)
        iv_table[word].insert_node(node)
    return iv_table

def fetch_iitable():
    '''Get the iitable with specific documents.
    '''
    doc_path_list = [doc_loc(i+1) for i in range(3)]
    doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
    return build_iitable(build_sitable(doc_list))


def doc_loc(doc_id):
    '''Get the location of the doc with certain id.

    Args:
        doc_id: The id of the doc, normally which is a number.

    Returns:
       A string of the absolute path to the doc file.
    '''
    file_name = '../data/pp_{0:d}.txt'.format(doc_id)
    path = os.path.join(os.path.dirname(__file__), file_name)
    return path
