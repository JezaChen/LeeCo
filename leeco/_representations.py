# -*- encoding:utf-8 -*-
# The representation of data structures in LeetCode.
import abc as _abc
import typing as _typing

from leeco.data_structures import TreeNode, ListNode

__all__ = [
    'BaseParser',
    'TrivialParser',
    'ListParser',
    'TreeNodeParser',
    'ListNodeParser',
]


class BaseParser(_abc.ABC):
    @classmethod
    @_abc.abstractmethod
    def parse(cls, representation: str):
        pass

    @classmethod
    @_abc.abstractmethod
    def to_str(cls, obj):
        pass


class TrivialParser(BaseParser):
    """ A trivial parser that uses eval to parse and str to serialize. """

    @classmethod
    def parse(cls, representation: str):
        return eval(representation)

    @classmethod
    def to_str(cls, obj):
        return str(obj)


class ListParser(BaseParser):
    """ A parser for list that uses eval to parse and str to serialize. """

    @classmethod
    def parse(cls, representation: str) -> _typing.List[_typing.Optional[int]]:
        representation = representation.strip()
        if not representation or representation[0] != '[' or representation[-1] != ']':
            raise ValueError("Invalid list format")
        # replace 'null' with 'None'
        input_str = representation.replace('null', 'None', -1)
        return TrivialParser.parse(input_str)

    @classmethod
    def to_str(cls, obj: _typing.List) -> str:
        return (
            TrivialParser.to_str(obj)
            .replace('None', 'null')
            .replace(' ', '')
            .replace('True', 'true')
            .replace('False', 'false')
        )


class _TreeNodeParseHelper:
    from collections import deque

    @classmethod
    def parse_tree_node(cls, nodes: _typing.List[_typing.Optional[int]]) -> _typing.Optional[TreeNode]:
        if not nodes:
            return None
        root = TreeNode(nodes[0])
        q = cls.deque()
        q.append(root)
        i = 1
        while i < len(nodes):
            cur = q.popleft()
            if cur is None:
                continue
            if nodes[i] is not None:
                cur.left = TreeNode(nodes[i])
                q.append(cur.left)
            else:
                q.append(None)
            i += 1
            if i >= len(nodes):
                break
            if nodes[i] is not None:
                cur.right = TreeNode(nodes[i])
                q.append(cur.right)
            else:
                q.append(None)
            i += 1
        return root

    @classmethod
    def tree_node_to_list(cls, root: _typing.Optional[TreeNode]) -> _typing.List[_typing.Optional[int]]:
        if not root:
            return []

        nodes = cls.deque()
        nodes.append(root)

        ans = []

        while nodes:
            cur = nodes.popleft()
            ans.append(cur.val if cur is not None else None)
            if cur:
                nodes.append(cur.left)
                nodes.append(cur.right)

        while ans and ans[-1] is None:
            ans.pop()

        return ans


class TreeNodeParser(BaseParser):
    """ A parser for TreeNode that uses eval to parse and str to serialize. """

    @classmethod
    def parse(cls, representation: str) -> _typing.Optional[TreeNode]:
        nodes = ListParser.parse(representation)
        return _TreeNodeParseHelper.parse_tree_node(nodes)

    @classmethod
    def to_str(cls, obj: _typing.Optional[TreeNode]) -> str:
        nodes = _TreeNodeParseHelper.tree_node_to_list(obj)
        return ListParser.to_str(nodes)


class ListNodeParser(BaseParser):
    """ A parser for ListNode that uses eval to parse and str to serialize. """

    @classmethod
    def parse(cls, representation: str) -> _typing.Optional[ListNode]:
        nodes = ListParser.parse(representation)
        if not nodes:
            return None
        dummy = ListNode(-1)
        cur = dummy
        for val in nodes:
            cur.next = ListNode(val)
            cur = cur.next
        return dummy.next

    @classmethod
    def to_str(cls, obj: _typing.Optional[ListNode]) -> str:
        nodes = []
        cur = obj
        while cur:
            nodes.append(cur.val)
            cur = cur.next
        return ListParser.to_str(nodes)
