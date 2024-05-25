# -*- encoding:utf-8 -*-
import typing
import typing as _typing
import types as _types
import sys

__all__ = [
    'get_origin',
    'get_args',
    'is_optional',
    'get_optional_type',
    'match_type',
]

try:
    from typing import get_origin
except ImportError:
    def get_origin(tp):
        """ get the origin of a generic class
        @note: e.g. List[int] -> list, Union[int, str] -> Union, Optional[int] -> Union
        """
        if hasattr(tp, '__origin__'):
            return tp.__origin__
        return tp

try:
    from typing import get_args
except ImportError:
    def get_args(tp):
        if hasattr(tp, '__args__'):
            return tp.__args__
        return ()


def is_optional(tp):
    orig = get_origin(tp)
    return (orig is _typing.Union or orig is _types.UnionType) and type(None) in get_args(tp)


def get_optional_type(tp):
    # todo rename to get_optional_inner_type or remove_optional
    orig = get_origin(tp)
    if orig is _typing.Union or orig is _types.UnionType:
        args = get_args(tp)
        if len(args) == 2:
            if args[0] is type(None):
                return args[1]
            elif args[1] is type(None):
                return args[0]
    raise ValueError(f"Invalid Optional type: {tp}")


def match_type(input_type_annotation, desired_type) -> bool:
    """
    Check if the input type annotation matches the desired type.
    @param input_type_annotation: only support basic types, Optional(or Union[x, None]), and List
    @param desired_type:
    @note:
    if input_type_annotation is Optional, the following two cases are considered as matching:
        1. desired_type is None
        2. desired_type is not None and is the same as the type inside Optional
            e.g. Optional[int] matches int
    if input_type is union, only support Optional[Union[x, None]]
    """
    underlying_type = input_type_annotation
    if is_optional(input_type_annotation):
        if desired_type is None or desired_type is type(None):
            return True
        underlying_type = get_optional_type(input_type_annotation)

    underlying_type_orig = get_origin(underlying_type)
    if (
            underlying_type == desired_type or
            underlying_type_orig is not None and underlying_type_orig == desired_type
    ):
        return True
    underlying_type_orig = get_origin(underlying_type)
    desired_type_orig = get_origin(desired_type)
    if underlying_type_orig is None or desired_type_orig is None:
        return False
    if underlying_type_orig != desired_type_orig:
        return False
    if underlying_type_orig is list:
        return not get_args(desired_type) or get_args(underlying_type) == get_args(desired_type)


def get_elem_type(tp):
    if match_type(tp, list):
        if is_optional(tp):
            tp = get_optional_type(tp)
        return get_args(tp)[0]
    return None


if __name__ == '__main__':
    print(get_elem_type(typing.List[typing.List[int]]))
