# -*- encoding:utf-8 -*-
import typing
import inspect
import sys

__all__ = ['inject', 'test']

_main_point = None  # type: typing.Optional[typing.Callable]
_main_point_cls = None  # type: typing.Optional[typing.Type]


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class _TreeNodeParser:
    from collections import deque

    @classmethod
    def parse_tree_node(cls, node: typing.List[typing.Optional[int]]) -> typing.Optional[TreeNode]:
        if not node:
            return None
        root = TreeNode(node[0])
        nodes = cls.deque()
        nodes.append(root)
        i = 1
        while i < len(node):
            cur = nodes.popleft()
            if cur is None:
                continue
            if node[i] is not None:
                cur.left = TreeNode(node[i])
                nodes.append(cur.left)
            else:
                nodes.append(None)
            i += 1
            if i >= len(node):
                raise ValueError("Invalid tree node list")
            if node[i] is not None:
                cur.right = TreeNode(node[i])
                nodes.append(cur.right)
            else:
                nodes.append(None)
            i += 1
        return root

    @classmethod
    def tree_node_to_list(cls, root: typing.Optional[TreeNode]) -> typing.List[typing.Optional[int]]:
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
        return ans


def inject(main_point: typing.Callable):
    global _main_point, _main_point_cls
    _main_point_cls = vars(sys.modules[main_point.__module__])[main_point.__qualname__.split('.')[0]]
    _main_point = main_point


def test(input_expression: str, expected_result: str = ""):
    global _main_point, _main_point_cls

    if _main_point is None or _main_point_cls is None:
        raise RuntimeError("Please inject main_point first")

    input_lines = input_expression.strip().split('\n')
    input_args = [eval(line.strip()) for line in input_lines]
    signature = inspect.signature(_main_point)
    if len(input_args) % (len(signature.parameters) - 1) != 0:
        raise ValueError("The number of input arguments is not a multiple of the number of parameters")
    for i in range(0, len(input_args), len(signature.parameters) - 1):
        instance = _main_point_cls()
        result = _main_point(instance, *input_args[i:i + len(signature.parameters) - 1])
        print(result)


def _get_outer_methods(cls):
    outer_methods = []
    for name, obj in cls.__dict__.items():
        if inspect.isfunction(obj) and not name.startswith('_'):
            outer_methods.append(obj)
    return outer_methods


def _try_dynamic_inject():
    import inspect
    stack = inspect.stack()
    # 找到是在何处调用了当前模块
    for frame_info in stack:
        if frame_info.filename == __file__:
            continue
        if frame_info.filename.endswith('.py'):
            if 'Solution' in frame_info.frame.f_globals:
                SolutionCls = frame_info.frame.f_globals['Solution']
                # 如果里面只有一个外部函数，那么就默认为main_point
                outer_methods = _get_outer_methods(SolutionCls)
                if len(outer_methods) == 1:
                    inject(outer_methods[0])
            break


# _try_dynamic_inject()

if __name__ == '__main__':
    print(_TreeNodeParser.tree_node_to_list(_TreeNodeParser.parse_tree_node([1, 2, 3, 4, 5, 6, 7])))
