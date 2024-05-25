# -*- encoding:utf-8 -*-
import typing


class MyCalendar:
    def __init__(self):
        self._arr = []  # type: typing.List[typing.Tuple[int, int]]

    def book(self, start: int, end: int) -> bool:
        lo, hi = 0, len(self._arr) - 1

        while lo <= hi:
            mid = (lo + hi) >> 1
            if self._arr[mid][0] >= end:
                hi = mid - 1
            else:
                lo = mid + 1
        if hi != -1 and self._arr[hi][1] > start:
            return False
        self._arr.insert(hi + 1, (start, end))
        return True


if __name__ == '__main__':
    import leeco
    leeco.test("""
["MyCalendar", "book", "book", "book"]
[[], [10, 20], [15, 25], [20, 30]]
["MyCalendar","book","book","book","book","book","book","book","book","book","book"]
[[],[47,50],[33,41],[39,45],[33,42],[25,32],[26,35],[19,25],[3,8],[8,13],[18,27]]
    """)
