#! /usr/local/bin Python3

import unittest
from proj_2.lev_dist.lev_dist import lev_distance


class TestLevDist(unittest.TestCase):
    '''Test lev_dist.py.
    '''

    def test_lev_deist(self):
        '''Test the lev_distance function in lev_dist.py
        '''
        str_one = ''
        str_two = ''
        self.assertEqual(lev_distance(str_one, str_two), 0)

        str_one = 'fast'
        str_two = 'cats'
        self.assertEqual(lev_distance(str_one, str_two), 3)

        str_one = 'OSLO'
        str_two = 'SNOW'
        self.assertEqual(lev_distance(str_one, str_two), 3)

        str_one = 'cat'
        str_two = 'catcat'
        self.assertEqual(lev_distance(str_one, str_two), 3)
