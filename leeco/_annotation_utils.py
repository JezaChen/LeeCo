# -*- encoding:utf-8 -*-
import typing as _typing
import sys

__all__ = [
    'get_origin_type',
    'get_args',
    'is_optional',
    'get_optional_type',
    'match_type',
]


def get_origin_type(tp):
    if sys.version_info >= (3, 8):
        return _typing.get_origin(tp)

    if hasattr(tp, '__origin__'):
        return tp.__origin__
    return tp


def get_args(tp):
    if sys.version_info >= (3, 8):
        return _typing.get_args(tp)

    if hasattr(tp, '__args__'):
        return tp.__args__
    return ()


def is_optional(tp):
    return get_origin_type(tp) is _typing.Union and type(None) in get_args(tp)


def get_optional_type(tp):
    if get_origin_type(tp) is _typing.Union:
        args = get_args(tp)
        if len(args) == 2 and args[1] is type(None):
            return args[0]
        raise ValueError(f"Invalid Optional type: {tp}")


def match_type(input_type_annotation, desired_type) -> bool:
    underlying_type = input_type_annotation
    if is_optional(input_type_annotation):
        underlying_type = get_optional_type(input_type_annotation)
    return underlying_type == desired_type or get_origin_type(underlying_type) == desired_type


def get_elem_type(tp):
    if match_type(tp, list):
        return get_args(tp)[0]
    return None


if __name__ == '__main__':
    get_elem_type(list[int])
