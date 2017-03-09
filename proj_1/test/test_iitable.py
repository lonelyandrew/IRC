#! /usr/local/bin Python3

import unittest
from proj_1.iitable.iitable import process_doc
from proj_1.iitable.iitable import WordChain
from proj_1.iitable.iitable import doc_loc
from proj_1.iitable.iitable import build_sitable
from proj_1.iitable.iitable import build_iitable
import os


DATA_FILE_DIR = os.path.join(os.path.dirname(__file__), 'test_data/')


class TestIITable(unittest.TestCase):

    def test_word_chain_init(self):
        new_chain = WordChain('test')
        self.assertEqual(new_chain.word, 'test')
        self.assertEqual(new_chain.freq, 0)
        self.assertIs(new_chain.head, None)
        self.assertIs(new_chain.tail, None)

        new_chain = WordChain('unit', freq=10)
        self.assertEqual(new_chain.freq, 10)

    def test_word_chain_insert_and_str(self):
        new_chain = WordChain('test')
        new_node = WordChain.Node()
        self.assertEqual(new_node.doc_id, 0)
        new_chain.insert_node(new_node)
        self.assertEqual(new_chain.head, new_node)
        self.assertEqual(new_chain.tail, new_node)
        self.assertEqual(new_chain.freq, 1)

        another_node = WordChain.Node(1)
        self.assertEqual(another_node.doc_id, 1)
        new_chain.insert_node(another_node)
        self.assertEqual(new_chain.freq, 2)
        self.assertEqual(new_chain.head.doc_id, 0)
        self.assertEqual(new_chain.tail.doc_id, 1)
        self.assertIs(new_chain.tail.next, None)
        self.assertIs(new_chain.head.next, new_chain.tail)

        new_chain_str = '(test, freq:2) * --> 0 --> 1'
        self.assertEqual(str(new_chain), new_chain_str)

        chain_one = WordChain('test')
        chain_one_str = '(test, freq:0) *'
        self.assertEqual(str(chain_one), chain_one_str)

        third_node = WordChain.Node(-1)
        with self.assertRaises(ValueError) as wrong_order:
            new_chain.insert_node(third_node)
        self.assertEqual(
                str(wrong_order.exception),
                'the inserting node have the wrong order.')

        with self.assertRaises(ValueError) as wrong_order:
            new_chain.insert_node(None)
        self.assertEqual(
                str(wrong_order.exception),
                'the inserting node cannot be None.')

    def test_node_init(self):
        node = WordChain.Node()
        self.assertEqual(node.doc_id, 0)
        self.assertIsNone(node.next)
        new_node = WordChain.Node('test')
        self.assertEqual(new_node.doc_id, 'test')

        node.next = new_node
        self.assertIs(node.next, new_node)

    def test_node_copy(self):
        node = WordChain.Node(1)
        new_node = node.copy()
        self.assertEqual(node.doc_id, new_node.doc_id)
        self.assertIsNot(node, new_node)

    def test_node_str(self):
        new_node = WordChain.Node()
        self.assertEqual(str(new_node), '0')

    def test_node_cmp(self):
        node_one = WordChain.Node(1)
        node_two = WordChain.Node(2)
        node_three = WordChain.Node(1)
        node_four = WordChain.Node(2)

        self.assertNotEqual(node_one, node_two)
        self.assertEqual(node_one, node_three)
        self.assertLessEqual(node_one, node_two)
        self.assertLessEqual(node_one, node_three)
        self.assertGreater(node_two, node_one)
        self.assertGreaterEqual(node_two, node_four)

    def test_doc_loc(self):
        file_path = doc_loc(1)
        self.assertTrue(os.path.exists(file_path))

    def test_process_doc(self):
        print(DATA_FILE_DIR)
        doc_path = os.path.join(DATA_FILE_DIR, 'test_data.txt')
        word_count = 0
        for word, doc_id in process_doc(doc_path, 1):
            self.assertTrue(word.isalnum())
            self.assertEqual(doc_id, 1)
            word_count += 1
        self.assertEqual(word_count, 15)

    def test_build_sitable(self):
        doc_path_list = []
        for i in range(3):
            file_name = 'test_data%d.txt' % (i + 1)
            doc_path_list.append(os.path.join(DATA_FILE_DIR, file_name))
        doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
        item_count = 0
        pre_word = ''
        pre_id = 0
        for word, doc_id in build_sitable(doc_list):
            self.assertGreaterEqual(word, pre_word)
            if word == pre_word:
                self.assertGreater(doc_id, pre_id)
            pre_word = word
            pre_id = doc_id
            item_count += 1
        self.assertEqual(item_count, 49)

    def test_build_iitable(self):
        doc_path_list = []
        for i in range(3):
            file_name = 'test_data%d.txt' % (i + 1)
            doc_path_list.append(os.path.join(DATA_FILE_DIR, file_name))
        doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
        iitable = build_iitable(build_sitable(doc_list))
        chain_a = iitable['a']
        self.assertEqual('a', chain_a.word)
        self.assertEqual(chain_a.freq, 3)
        chain_deepen = iitable['deepen']
        self.assertEqual(chain_deepen.word, 'deepen')
        self.assertEqual(chain_deepen.freq, 1)

    def test_chain_union(self):
        doc_path_list = []
        for i in range(3):
            file_name = 'test_data%d.txt' % (i + 1)
            doc_path_list.append(os.path.join(DATA_FILE_DIR, file_name))
        doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
        iitable = build_iitable(build_sitable(doc_list))

        chain = WordChain.union(iitable['a'], iitable['in'])
        chain_str = '(a OR in, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.union(iitable['a'], iitable['deepen'])
        chain_str = '(a OR deepen, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.union(iitable['a'], WordChain('test'))
        chain_str = '(a OR test, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.union(WordChain('test'), iitable['a'])
        chain_str = '(test OR a, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.union(iitable['nature'], iitable['a'])
        chain_str = '(nature OR a, freq:3) * --> 1 --> 2 --> 3'
        self.assertEqual(str(chain), chain_str)

    def test_chain_intersection(self):
        doc_path_list = []
        for i in range(3):
            file_name = 'test_data%d.txt' % (i + 1)
            doc_path_list.append(os.path.join(DATA_FILE_DIR, file_name))
        doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
        iitable = build_iitable(build_sitable(doc_list))

        chain = WordChain.intersection(iitable['a'], iitable['deepen'])
        chain_str = '(a AND deepen, freq:1) * --> 2'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.intersection(iitable['nature'], iitable['deepen'])
        chain_str = '(nature AND deepen, freq:0) *'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.intersection(iitable['nature'], WordChain('test'))
        chain_str = '(nature AND test, freq:0) *'
        self.assertEqual(str(chain), chain_str)

    def test_chain_diff(self):
        doc_path_list = []
        for i in range(3):
            file_name = 'test_data%d.txt' % (i + 1)
            doc_path_list.append(os.path.join(DATA_FILE_DIR, file_name))
        doc_list = (process_doc(doc_path_list[i], i + 1) for i in range(3))
        iitable = build_iitable(build_sitable(doc_list))

        chain = WordChain.diff(iitable['a'], iitable['deepen'])
        chain_str = '(a AND NOT deepen, freq:2) * --> 1 --> 3'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.diff(iitable['nature'], iitable['deepen'])
        chain_str = '(nature AND NOT deepen, freq:1) * --> 3'
        self.assertEqual(str(chain), chain_str)

        chain = WordChain.diff(iitable['nature'], WordChain('test'))
        chain_str = '(nature AND NOT test, freq:1) * --> 3'
        self.assertEqual(str(chain), chain_str)
