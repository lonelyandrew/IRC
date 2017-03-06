#! /usr/local/bin Python3

import unittest
from proj_1.iitable.iitable import process_doc, build_sitable
import os


DATA_FILE_DIR = os.path.join(os.path.dirname(__file__), 'test_data/')

class TestIITable(unittest.TestCase):

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
