#! /usr/local/bin Python3

import unittest
from proj_1.iitable.iitable import process_doc
from proj_1.iitable.iitable import WordChain
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

    def test_word_chain_insert(self):
        new_chain = WordChain('test')
        new_node = WordChain.node()
        self.assertEqual(new_node.doc_id, 0)
        new_chain.insert_node(new_node)
        self.assertEqual(new_chain.head, new_node)
        self.assertEqual(new_chain.tail, new_node)
        self.assertEqual(new_chain.freq, 1)

        another_node = WordChain.node(1)
        self.assertEqual(another_node.doc_id, 1)
        new_chain.insert_node(another_node)
        self.assertEqual(new_chain.freq, 2)
        self.assertEqual(new_chain.head.doc_id, 0)
        self.assertEqual(new_chain.tail.doc_id, 1)
        self.assertIs(new_chain.tail.next, None)
        self.assertIs(new_chain.head.next, new_chain.tail)

        third_node = WordChain.node(-1)
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

    def test_process_doc(self):
        print(DATA_FILE_DIR)
        doc_path = os.path.join(DATA_FILE_DIR, 'test_data.txt')
        for word, doc_id in process_doc(doc_path, 1):
            self.assertTrue(word.isalnum())
            self.assertEqual(doc_id, 1)

    # def test_build_sitable(self):
    #    test_docs = []
    #    for i in range(2):
    #        file_name = 'test_data%d.txt' % (i + 1)
    #        doc_path = os.path.join(DATA_FILE_DIR, file_name)
    #        test_docs.append(doc_path)
    #    doc_one = process_doc(test_docs[0])
    #    doc_two = process_doc(test_docs[1])
    #    sitable = build_sitable([doc_one, doc_two])
    #    word_list = []
    #    for row in sitable:
    #        word_list.append(row)
    #    self.assertEqual(len(word_list), 30)
    #    self.assertTrue((('job', 2) in word_list))
    #    self.assertEqual(word_list[-1][0], 'true')
    #    self.assertEqual(word_list[0][0], 'a')
    #    for row in word_list:
    #        if row[0] == 'job':
    #            self.assertEqual(row[1], 2)
    #        elif row[0] == 'artist':
    #            self.assertEqual(row[1], 2)

    def test_build_iitable(self):
        pass

if __name__ == '__main__':
    unittest.main()
