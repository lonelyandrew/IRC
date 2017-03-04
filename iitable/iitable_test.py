#! /usr/local/bin Python3

import unittest
from iitable import process_doc, build_sitable


def test_data_loc(doc_id):
    return '/Users/andrewshi/Codes/Github/IRC/data/test_data%d.txt' % doc_id


class TestIITable(unittest.TestCase):

    def test_process_doc(self):
        doc_path = '/Users/andrewshi/Codes/Github/IRC/data/test_data.txt'
        for word, doc_id in process_doc(doc_path, 1):
            self.assertTrue(word.isalnum())
            self.assertEqual(doc_id, 1)

    def test_build_sitable(self):
        doc_one = process_doc(test_data_loc(1), 1)
        doc_two = process_doc(test_data_loc(2), 2)
        sitable = build_sitable([doc_one, doc_two])
        word_list = []
        for row in sitable:
            word_list.append(row)
        self.assertEqual(len(word_list), 30)
        self.assertTrue((('job', 2) in word_list))
        self.assertEqual(word_list[-1][0], 'true')
        self.assertEqual(word_list[0][0], 'a')
        for row in word_list:
            if row[0] == 'job':
                self.assertEqual(row[1], 2)
            elif row[0] == 'artist':
                self.assertEqual(row[1], 2)

    def test_build_iitable(self):
        pass

if __name__ == '__main__':
    unittest.main()
