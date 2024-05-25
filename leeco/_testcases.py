# -*- encoding:utf-8 -*-
import typing as _typing


__all__ = ['TestCase']


class _TestCaseMeta(type):
    """ A metaclass for TestCase that allows the following usage:
    >>> t = TestCase("input", "expected_output")
    >>> t2 = TestCase(t)  # It will return t itself, without creating a new instance.
    >>> assert t is t2
    """

    def __call__(cls, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], cls):
            return args[0]
        return super().__call__(*args, **kwargs)


class TestCase(metaclass=_TestCaseMeta):
    """ A class for test case. """
    @_typing.overload
    def __init__(self, input_str: str, expected_output_str: str = ''): ...

    @_typing.overload
    def __init__(self, test_case: 'TestCase'): ...

    def __init__(self, input_str: str, expected_output_str: str = ''):
        self.input_str = input_str
        self.expected_output_str = expected_output_str

    def __repr__(self):
        return f"TestCase({self.input_str}, {self.expected_output_str})"
