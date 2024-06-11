# -*- encoding:utf-8 -*-
import typing as _typing

__all__ = [
    'TreeNode',
    'ListNode',
]


class TreeNode:
    """ Definition for a binary tree node commonly used in LeetCode problems."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{type(self).__name__}(val={self.val})'

    def __str__(self):
        return repr(self)


class ListNode:
    """ Definition for singly-linked list commonly used in LeetCode problems. """

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next  # type: _typing.Optional[ListNode]

    def __repr__(self):
        return f'{type(self).__name__}(val={self.val})'

    def __str__(self):
        return repr(self)
