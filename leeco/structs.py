# -*- encoding:utf-8 -*-
import typing
import typing as _typing
import inspect as _inspect
from leeco._annotation_utils import is_optional, get_optional_type
from leeco._representations import get_parser

__all__ = ['TestCase', 'Result']


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
    def __init__(self, input_str: str, expected_output_str: str = '', timeit: bool = False, print_output: bool = True):
        ...

    @_typing.overload
    def __init__(self, test_case: 'TestCase'): ...

    def __init__(self, input_str: str, expected_output_str: str = '', timeit: bool = False, print_output: bool = True):
        self.input_str = input_str
        self.expected_output_str = expected_output_str
        self.timeit = timeit
        self.print_output = print_output

    def __repr__(self):
        return f"TestCase({self.input_str}, {self.expected_output_str})"


def _dump_output(output, annotation=None) -> str:
    output_type = type(output)
    if annotation is not None and annotation is not _inspect.Parameter.empty:
        output_type = annotation
        if is_optional(annotation):
            output_type = get_optional_type(annotation)

    parser = get_parser(output_type)
    return parser.to_str(output)


class Result:
    def __init__(self, raw: typing.Any, return_annotation: typing.Type = None):
        self._raw = raw
        self._return_annotation = return_annotation

    def raw(self) -> typing.Any:
        return self._raw

    def formatted(self) -> str:
        return _dump_output(self._raw, self._return_annotation)

    def __str__(self):
        return self.formatted()

    def __repr__(self):
        return f"Result({self._raw!r})"
