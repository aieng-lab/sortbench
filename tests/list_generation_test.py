import unittest

import sortbench.util.data_utils as data_utils

class TestListGeneration(unittest.TestCase):

    def test_integer_list(self):
        # Test integer list generation
        min_value = 0
        max_value = 1000
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'integer', min_value=min_value, max_value=max_value)
        self.assertEqual(len(lst), num_samples)
        for val in lst:
            self.assertTrue(type(val) == int)
            self.assertTrue(min_value <= val <= max_value)
    
    def test_float_list(self):
        # Test float list generation
        min_value = 0
        max_value = 1000
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'float', min_value=min_value, max_value=max_value)
        self.assertEqual(len(lst), num_samples)
        for val in lst:
            self.assertTrue(type(val) == float)
            self.assertTrue(min_value <= val <= max_value)

    def test_string_list(self):
        # Test string list generation
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'string')
        self.assertEqual(len(lst), num_samples)
        for val in lst:
            self.assertTrue(type(val) == str)
            self.assertTrue(val.isascii())

    def test_word_list(self):
        # Test word list generation
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'word')
        self.assertEqual(len(lst), num_samples)
        for val in lst:
            self.assertTrue(type(val) == str)

    def test_number_string_list(self):
        # Test number string list generation
        min_value = 0
        max_value = 1000
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'number_string', min_value=min_value, max_value=max_value)
        self.assertEqual(len(lst), num_samples)
        for val in lst:
            self.assertTrue(type(val) == str)

    def test_prefix_string_list(self):
        # Test prefix string list generation
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'prefix_string')
        self.assertEqual(len(lst), num_samples)
        for val in lst:
            self.assertTrue(type(val) == str)
            firstChar = val[0]
            self.assertTrue(val.startswith(firstChar*3))

    def test_duplicates(self):
        # Test list generation with duplicates
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'integer', duplicates=True)
        self.assertEqual(len(lst), num_samples)
        for i, val in enumerate(lst):
            self.assertTrue(type(val) == int)
            if i % 2 == 0:
                self.assertEqual(val, lst[i+1])

    def test_sorted(self):
        # Test sorted list generation
        num_samples = 10
        lst = data_utils.generate_unsorted_list(num_samples, 'integer', sorted=True)
        self.assertEqual(len(lst), num_samples)
        for i in range(1, num_samples):
            self.assertTrue(lst[i-1] <= lst[i])
