# -*- encoding:utf-8 -*-
import typing
import sys
from .structs import TestCase, Result

if sys.version_info >= (3, 9):
    ResultList = list[Result]
else:
    ResultList = typing.List[Result]


def inject(main_point: typing.Callable): ...


@typing.overload
def test(input_str: str, expected_output_str: str = '', timeit: bool = False, print_output: bool = True) -> ResultList:
    ...


@typing.overload
def test(testcase: TestCase, /) -> None: ...
