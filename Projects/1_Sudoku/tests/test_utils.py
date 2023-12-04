import unittest

from solution import diagonal, reverse_diagonal


class TestDiagonal(unittest.TestCase):

    #  Should return a list of diagonal elements from given rows and columns
    def test_diagonal_elements(self):
        rows = ['A', 'B', 'C']
        cols = ['1', '2', '3']
        expected_result = ['A1', 'B2', 'C3']
        self.assertEqual(expected_result, diagonal(rows, cols))

    #  Should return an empty list when both rows and cols are empty
    def test_empty_rows_and_cols(self):
        rows = []
        cols = []
        expected_result = []
        self.assertEqual(expected_result, diagonal(rows, cols))

    #  Should return a list with single element when both rows and cols have only one element
    def test_single_element(self):
        rows = ['A']
        cols = ['1']
        expected_result = ['A1']
        self.assertEqual(expected_result, diagonal(rows, cols))

    #  Should raise an AssertionError when rows and cols have different lengths
    def test_different_lengths_assertion_error(self):
        rows = ['A', 'B', 'C']
        cols = ['1', '2', '3', '4']
        with self.assertRaises(AssertionError):
            diagonal(rows, cols)

    #  Should return a list of diagonal elements when rows and cols have the same elements
    def test_same_elements(self):
        rows = ['A', 'B', 'C']
        cols = ['A', 'B', 'C']
        expected_result = ['AA', 'BB', 'CC']
        self.assertEqual(expected_result, diagonal(rows, cols))


class TestReverseDiagonal(unittest.TestCase):

    #  Should return a list of concatenated elements from _rows and _cols in reverse diagonal order
    def test_concatenated_elements_reverse_diagonal_order(self):
        _rows = ['A', 'B', 'C']
        _cols = ['1', '2', '3']
        expected_result = ['A3', 'B2', 'C1']
        self.assertEqual(reverse_diagonal(_rows, _cols), expected_result)

    #  Should return an empty list when given empty lists for _rows and _cols
    def test_empty_lists(self):
        _rows = []
        _cols = []
        expected_result = []
        self.assertEqual(reverse_diagonal(_rows, _cols), expected_result)

    #  Should return a list of one element when given a single element list for _rows and _cols
    def test_single_element_lists(self):
        _rows = ['A']
        _cols = ['1']
        expected_result = ['A1']
        self.assertEqual(reverse_diagonal(_rows, _cols), expected_result)

    #  Should return a list of two elements when given two element lists for _rows and _cols
    def test_two_element_lists(self):
        _rows = ['A', 'B']
        _cols = ['1', '2']
        expected_result = ['A2', 'B1']
        self.assertEqual(reverse_diagonal(_rows, _cols), expected_result)

    #  Should raise an AssertionError when given lists of different lengths
    def test_different_length_lists(self):
        _rows = ['A', 'B', 'C']
        _cols = ['1', '2']
        with self.assertRaises(AssertionError):
            reverse_diagonal(_rows, _cols)

    #  Should return a list of three elements when given three element lists for _rows and _cols
    def test_three_element_lists(self):
        _rows = ['A', 'B', 'C']
        _cols = ['1', '2', '3']
        expected_result = ['A3', 'B2', 'C1']
        self.assertEqual(reverse_diagonal(_rows, _cols), expected_result)

    #  Should return a list of n elements when given n element lists for _rows and _cols
    def test_n_element_lists(self):
        _rows = ['A', 'B', 'C', 'D']
        _cols = ['1', '2', '3', '4']
        expected_result = ['A4', 'B3', 'C2', 'D1']
        self.assertEqual(reverse_diagonal(_rows, _cols), expected_result)


if __name__ == '__main__':
    unittest.main()
