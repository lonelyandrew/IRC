#! /usr/bin/env python3

import re
import pandas as pd


class WordChain(object):

    def __init__(self, word):
        self.word = word
        self.freq = 0
        self.head = None


    def insert_node(self, node):
        if self.head is None:
            self.head = node
        else:
            prev = self.head
            while prev.next is not None:
                prev = prev.next
            prev.next = node
        self.freq += 1

    def __str__(self):
        chain_str = '(%s, freq:%d)' % (self.word, self.freq)
        if self.head is not None:
            node_to_print = self.head
            while node_to_print is not None:
                chain_str += ' --> '
                chain_str += str(node_to_print)
                node_to_print = node_to_print.next
        return chain_str
    
    class node(object):
        
        def __init__(self, doc_id):
            self.doc_id = doc_id
            self.next = None

        def __str__(self):
            return str(self.doc_id)

def process_doc(doc_location, doc_id):
    word_list = set()
    p = re.compile('[^\W_]+')
    with open(doc_location) as doc:
        for line in doc:
            word_list.update(p.findall(line.lower()))
    for word in word_list:
        yield word, doc_id


def build_sorted_index_table(doc_list):
    item_df = pd.DataFrame()
    for doc in doc_list:
        df = pd.DataFrame(doc)
        item_df = item_df.append(df, ignore_index=True)
    item_df.columns = ['term', 'id']
    item_df.sort_values(['term', 'id'], inplace=True)
    for row in item_df.itertuples(index=False, name=None):
        yield row


def build_inverted_index_table(sorted_table):
    iv_table = {}
    for word, doc_id in sorted_table:
        if word not in iv_table:
            iv_table[word] = WordChain(word)
        node = WordChain.node(doc_id)
        iv_table[word].insert_node(node)
    return iv_table


def add_node(head, node):
    search_node = head
    while search_node['next'] is not None:
        search_node = search_node['next']
    search_node['next'] = node


def doc_loc(doc_id):
    return ('/Users/andrewshi/Codes/Github/IRC/data/pp/pp_%s.txt' % doc_id)


if __name__ == '__main__':
    doc_list = (process_doc(doc_loc(i), i) for i in range(1, 4))

    sorted_table = build_sorted_index_table(doc_list)
    iv_table = build_inverted_index_table(sorted_table)

    for word, chain in iv_table.items():
       print(chain) 
