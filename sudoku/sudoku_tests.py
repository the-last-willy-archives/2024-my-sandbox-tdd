import csv
import unittest
from sudoku import issudokusolution, Sudoku


class IssudokusolutionTests(unittest.TestCase):
    def readcsv(self, filepath):
        pass

    def test_should_return_false_for_incorrect_solution(self):
        sud = Sudoku(cols=9, rows=9, values=self.readcsv("./data/sudoku0.csv"))
        sol = Sudoku(cols=9, rows=9, values=self.readcsv("./data/sudoku0-incorrect0.csv"))
        self.assertFalse(issudokusolution(sudoku=sud, solution=sol))

    def test_should_return_true_for_correct_solution(self):
        pass


class SudokuTests(unittest.TestCase):
    def _somesudoku(self):
        return Sudoku(rows=9, cols=9)

    def test_init_should_raise_valueerror_if_col_count_different_from_row_count(self):
        self.assertRaises(ValueError, lambda: Sudoku(rows=4, cols=9))

    def test_init_should_return_empty_sudoku(self):
        sudoku = Sudoku(cols=4, rows=4)
        self.assertTrue(sudoku.isvalid())

    def test_rowcount_should_return_row_count(self):
        sudoku = self._somesudoku()
        self.assertEqual(sudoku.rowcount(), 9)

    def test_colcount_should_return_col_count(self):
        sudoku = self._somesudoku()
        self.assertEqual(sudoku.colcount(), 9)

    def test_at_should_none(self):
        sudoku = self._somesudoku()
        self.assertIsNone(sudoku.at(col=2, row=3))

    def test_at_should_return_init_values(self):
        values = [0, 1, 2, 3]
        s = Sudoku(cols=2, rows=2, values=values)
        self.assertEqual(s.at(col=0, row=0), 0)
        self.assertEqual(s.at(col=1, row=0), 1)
        self.assertEqual(s.at(col=0, row=1), 2)
        self.assertEqual(s.at(col=1, row=1), 3)

    def test_at_should_return_value_assigned(self):
        sudoku = self._somesudoku()
        self.assertIsNone(sudoku.at(col=7, row=8))
        sudoku.assign(col=7, row=8, value=3)
        self.assertEqual(sudoku.at(col=7, row=8), 3)

    def test_at_should_raise_valueerrror_on_out_of_range(self):
        s = self._somesudoku()
        self.assertRaises(ValueError, lambda: s.at(col=11, row=13))

    def test_isvalid_should_return_true_for_empty_sudoku(self):
        sudoku = self._somesudoku()
        self.assertTrue(sudoku.isempty())
        self.assertTrue(sudoku.isvalid())

    def test_isvalid_should_return_false_if_same_number_on_row(self):
        sudoku = self._somesudoku()
        sudoku.assign(col=3, row=6, value=9)
        sudoku.assign(col=5, row=6, value=9)
        self.assertFalse(sudoku.isvalid())

    def test_isvalid_should_return_false_if_same_value_on_col(self):
        sudoku = self._somesudoku()
        sudoku.assign(col=2, row=2, value=8)
        sudoku.assign(col=2, row=7, value=8)
        self.assertFalse(sudoku.isvalid())

    def test_isvalid_should_return_false_if_same_value_on_region(self):
        sudoku = self._somesudoku()
        sudoku.assign(col=4, row=4, value=6)
        sudoku.assign(col=5, row=5, value=6)
        self.assertFalse(sudoku.isvalid())

    def test_isempty_should_return_false_after_assign(self):
        s = self._somesudoku()
        self.assertTrue(s.isempty())
        s.assign(col=2, row=3, value=4)
        self.assertFalse(s.isempty())
