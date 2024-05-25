# -*- encoding:utf-8 -*-
# The representation of data structures in LeetCode.
import abc as _abc
import typing
import typing as _typing

import leeco.data_structures as ds
from leeco._annotation_utils import match_type

__all__ = [
    'BaseParser',
    'TrivialParser',
    'ListParser',
    'TreeNodeParser',
    'ListNodeParser',
]


def get_parser(type_annotation: typing.Type):
    parser = TrivialParser
    if match_type(type_annotation, ds.TreeNode):
        parser = TreeNodeParser
    if match_type(type_annotation, ds.ListNode):
        parser = ListNodeParser
    if match_type(type_annotation, list):
        parser = ListParser
    return parser


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


ListElemType = typing.TypeVar('ListElemType')


class ListParser(BaseParser):
    """ A parser for list that uses eval to parse and str to serialize. """

    @classmethod
    def parse(
            cls,
            representation: str,
            elem_type: typing.Optional[typing.Type[ListElemType]] = None
    ) -> _typing.List[_typing.Optional[ListElemType]]:
        representation = representation.strip()
        if not representation or representation[0] != '[' or representation[-1] != ']':
            raise ValueError("Invalid list format")

        if elem_type is None:
            # replace 'null' with 'None'
            input_str = representation.replace('null', 'None', -1)
            # call the trivial parser
            return TrivialParser.parse(input_str)

        representation = representation[1:-1]
        if not representation:
            return []
        parser = get_parser(elem_type)

        return [
            parser.parse(elem_str.strip())
            for elem_str in representation.split(',')
        ]

    @classmethod
    def to_str(cls, obj: _typing.List) -> str:
        if not obj:
            return "[]"

        # detect the element type
        elem_type = type(obj[0])
        parser = get_parser(elem_type)

        return f"[{','.join(parser.to_str(elem) for elem in obj)}]"


class _TreeNodeParseHelper:
    from collections import deque

    @classmethod
    def parse_tree_node(cls, nodes: _typing.List[_typing.Optional[int]]) -> _typing.Optional[ds.TreeNode]:
        if not nodes:
            return None
        root = ds.TreeNode(nodes[0])
        q = cls.deque()
        q.append(root)
        i = 1
        while i < len(nodes):
            cur = q.popleft()
            if cur is None:
                continue
            if nodes[i] is not None:
                cur.left = ds.TreeNode(nodes[i])
                q.append(cur.left)
            else:
                q.append(None)
            i += 1
            if i >= len(nodes):
                break
            if nodes[i] is not None:
                cur.right = ds.TreeNode(nodes[i])
                q.append(cur.right)
            else:
                q.append(None)
            i += 1
        return root

    @classmethod
    def tree_node_to_list(cls, root: _typing.Optional[ds.TreeNode]) -> _typing.List[_typing.Optional[int]]:
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
    def parse(cls, representation: str) -> _typing.Optional[ds.TreeNode]:
        nodes = ListParser.parse(representation)
        return _TreeNodeParseHelper.parse_tree_node(nodes)

    @classmethod
    def to_str(cls, obj: _typing.Optional[ds.TreeNode]) -> str:
        nodes = _TreeNodeParseHelper.tree_node_to_list(obj)
        return ListParser.to_str(nodes)


class ListNodeParser(BaseParser):
    """ A parser for ListNode that uses eval to parse and str to serialize. """

    @classmethod
    def parse(cls, representation: str) -> _typing.Optional[ds.ListNode]:
        nodes = ListParser.parse(representation)
        if not nodes:
            return None
        dummy = ds.ListNode(-1)
        cur = dummy
        for val in nodes:
            cur.next = ds.ListNode(val)
            cur = cur.next
        return dummy.next

    @classmethod
    def to_str(cls, obj: _typing.Optional[ds.ListNode]) -> str:
        nodes = []
        cur = obj
        while cur:
            nodes.append(cur.val)
            cur = cur.next
        return ListParser.to_str(nodes)
