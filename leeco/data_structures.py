# -*- encoding:utf-8 -*-

class TreeNode:
    """ Definition for a binary tree node commonly used in LeetCode problems."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    """ Definition for singly-linked list commonly used in LeetCode problems. """

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
