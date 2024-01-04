import itertools
from math import sqrt


def issudokusolution(*, sudoku, solution):
    return True


class Sudoku:
    def __init__(self, *, cols, rows, values=None):
        if cols != rows:
            raise ValueError("cols != rows")

        self._colcount = cols
        self._rowcount = rows

        if values is None:
            self._cells = [None] * self.rowcount() * self.colcount()
        else:
            self._cells = values

    def rowcount(self):
        return self._rowcount

    def colcount(self):
        return self._colcount

    def at(self, *, col, row):
        if col >= self.colcount():
            raise ValueError(f"col={col}. Must be < {self.colcount()}")
        if row >= self.rowcount():
            raise ValueError(f"row={row}. Must be < {self.rowcount()}")
        idx = self._indexat(col=col, row=row)
        return self._cells[idx]

    def assign(self, *, col, row, value):
        idx = self._indexat(col=col, row=row)
        self._cells[idx] = value

    def _indexat(self, *, col, row):
        return row * self.colcount() + col

    def isempty(self):
        for c in self._cells:
            if c is not None:
                return False
        return True

    def isvalid(self):
        b = True
        b = b and self._arecolsvalid()
        b = b and self._arerowsvalid()
        b = b and self._areregionsvalid()
        return b

    def _arecolsvalid(self):
        for c in range(self.colcount()):
            vals = []
            for r in range(self.rowcount()):
                val = self.at(col=c, row=r)
                if val is not None and val in vals:
                    return False
                vals.append(val)
        return True

    def _arerowsvalid(self):
        for r in range(self.rowcount()):
            vals = []
            for c in range(self.colcount()):
                val = self.at(col=c, row=r)
                if val is not None and val in vals:
                    return False
                vals.append(val)
        return True

    def _areregionsvalid(self):
        for (a, b) in itertools.product(range(self._regioncount()), range(self._regioncount())):
            vals = []
            for (i, j) in itertools.product(range(self._regionsize()), range(self._regionsize())):
                c = a * self._regionsize() + i
                r = b * self._regionsize() + j
                val = self.at(col=c, row=r)
                if val is not None and val in vals:
                    return False
                vals.append(val)
        return True

    def _regioncount(self) -> int:
        # 4x4 -> 2x2 regions
        # 9x9 -> 3x3 regions
        # 16x16 -> 4x4 regions
        return int(sqrt(self.colcount()))

    def _regionsize(self) -> int:
        # there are as many regions as there are numbers in these regions
        return self._regioncount()