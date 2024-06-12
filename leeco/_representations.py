# -*- encoding:utf-8 -*-
# The representation of data structures in LeetCode.
import abc as _abc
import typing
import typing as _typing

import leeco.data_structures as ds
from leeco._annotation_utils import match_type, get_elem_type

__all__ = [
    'BaseParser',
    'TrivialParser',
    'ListParser',
    'TreeNodeParser',
    'ListNodeParser',
]


def get_parser(type_annotation: typing.Type):
    parser = TrivialParser
    if match_type(type_annotation, str):
        parser = StringParser
    elif match_type(type_annotation, ds.TreeNode):
        parser = TreeNodeParser
    elif match_type(type_annotation, ds.ListNode):
        parser = ListNodeParser
    elif match_type(type_annotation, list):
        elem_type = get_elem_type(type_annotation)
        parser = ListParser[elem_type]
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
        if obj is None:
            return 'null'
        return repr(obj)


class StringParser(TrivialParser):
    @classmethod
    def to_str(cls, obj):
        import json
        return json.dumps(obj)


ListElemType = typing.TypeVar('ListElemType')

# elem type -> list parser
_ListParserCache = {}


class ListParser(BaseParser):
    """ A parser for list that uses eval to parse and str to serialize. """
    _ElementType = typing.Any

    @classmethod
    def split_list(cls, representation: str) -> typing.Iterator[typing.Any]:
        """ Split a list representation into a list of string representations of the elements.
        """
        # remove the first '[' and the last ']'
        representation = representation[1:-1]
        if not representation:
            return
        # split by ',' but ignore ',' inside brackets
        level = 0
        start = 0
        for i, c in enumerate(representation):
            if c == '[':
                level += 1
            elif c == ']':
                level -= 1
            elif c == ',' and not level:
                elem_str = representation[start:i].strip()
                yield elem_str
                start = i + 1
        last_elem_str = representation[start:].strip()
        if last_elem_str:  # sometimes the list ends with a comma
            yield last_elem_str

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
            # replace '\\' with '\\\\' before call TrivialParser.parse
            # e.g. eval('"\\"') or eval(r'"\"') will raise a SyntaxError
            input_str = input_str.replace('\\', '\\\\')
            # call the element parser to parse each element
            return get_parser(cls._ElementType).parse(input_str)
        parser = get_parser(elem_type)

        return [
            parser.parse(elem_str.strip())
            for elem_str in cls.split_list(representation)
        ]

    @classmethod
    def to_str(cls, obj: _typing.List) -> str:
        if not obj:
            return "[]"

        # detect the element type
        parser = get_parser(cls._ElementType if cls._ElementType is not typing.Any else type(obj[0]))

        return f"[{','.join(parser.to_str(elem) for elem in obj)}]"

    def __class_getitem__(cls, elem_type):
        # inherit the class and set the element type
        global _ListParserCache
        if elem_type not in _ListParserCache:
            _ListParserCache[elem_type] = type(
                f'{cls.__name__}[{elem_type}]',
                (cls,),
                {'_ElementType': elem_type}
            )

        return _ListParserCache[elem_type]


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


if __name__ == '__main__':
    print(ListParser.parse('[[1],[2,3]]', typing.List[typing.List[int]]))
