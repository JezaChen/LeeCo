# -*- encoding:utf-8 -*-
import typing
import typing as _typing

__all__ = [
    'TreeNode',
    'ListNode',
]

T = _typing.TypeVar('T')


class TreeNode(typing.Generic[T]):
    """ Definition for a binary tree node commonly used in LeetCode problems."""

    val: T
    left: _typing.Optional[TreeNode]
    right: _typing.Optional[TreeNode]

    def __init__(self, val: T = T(), left: _typing.Optional[TreeNode] = None, right: _typing.Optional[TreeNode] = None):
        ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...


class ListNode(typing.Generic[T]):
    """ Definition for singly-linked list commonly used in LeetCode problems. """
    val: T
    next: _typing.Optional[TreeNode]

    def __init__(self, val: T = T(), next: _typing.Optional[TreeNode] = None): ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...
