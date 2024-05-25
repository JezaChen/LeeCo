# -*- encoding:utf-8 -*-
""" Utilities for measuring execution time cost. """

import contextlib
import dataclasses
import typing

__all__ = [
    'TimeCost',
    'timeit_block'
]


@dataclasses.dataclass
class TimeCost:
    """ The time cost of a function. """
    enable: bool
    start: float = 0
    end: float = 0

    def set_result(self, start, end):
        self.start = start
        self.end = end

    @property
    def duration(self):
        """ The duration of the time cost, in seconds. """
        return self.end - self.start

    def __str__(self):
        return f'{self.duration:.6f}s'

    def __repr__(self):
        return f'{type(self).__name__}(duration={str(self)})'


@contextlib.contextmanager
def timeit_block(enable: bool = True, output: bool = True):
    import time
    cost = TimeCost(enable)
    if enable:
        start = time.time()
        yield cost
        end = time.time()
        cost.set_result(start, end)
        if output:
            print(f"==> Time cost: {cost.duration * 1_000:.3f}ms")
    else:
        yield cost
