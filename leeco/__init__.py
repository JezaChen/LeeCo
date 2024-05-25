# -*- encoding:utf-8 -*-
import typing
import inspect
import sys
import types

__all__ = [
    # main functions
    'inject', 'test',
    # data structures
    'ListNode', 'TreeNode',
    # test case
    'TestCase', 'Result'
]

from leeco._annotation_utils import is_optional, get_optional_type, match_type
from leeco._representations import ListParser, TreeNodeParser, TrivialParser, ListNodeParser, get_parser
from leeco.structs import TestCase, Result
from leeco._timeit_utils import timeit_block
from leeco.data_structures import ListNode, TreeNode

_main_point = None  # type: typing.Optional[types.MethodType | typing.Type]


def inject(main_point: typing.Callable):
    global _main_point
    _main_point = main_point


def _dump_output(output, annotation=None) -> str:
    output_type = type(output)
    if annotation is not None and annotation is not inspect.Parameter.empty:
        output_type = annotation
        if is_optional(annotation):
            output_type = get_optional_type(annotation)

    parser = get_parser(output_type)
    return parser.to_str(output)


_InputType = typing.TypeVar('_InputType')


def _parse_input(input_str: str, input_type_annotation: typing.Type[_InputType]) -> _InputType:
    parser = get_parser(input_type_annotation)
    return parser.parse(input_str)


def _parse_params(input_str_list: typing.List[str], param_list: typing.List[inspect.Parameter]) -> typing.List:
    if len(input_str_list) != len(param_list):
        raise ValueError("The number of input strings is not equal to the number of parameters")
    return [_parse_input(input_str, param.annotation) for input_str, param in zip(input_str_list, param_list)]


def _test_design(testcase: TestCase):
    global _main_point

    assert _main_point is not None
    input_lines = testcase.input_str.strip().split('\n')
    if len(input_lines) % 2:
        raise ValueError("The input expression must have 2 lines for each test case")

    for case_commands_input, case_params_input in zip(input_lines[::2], input_lines[1::2]):
        commands = TrivialParser.parse(case_commands_input.strip())
        params = TrivialParser.parse(case_params_input.strip())

        ins = None
        result = []

        with timeit_block(testcase.timeit):
            for command, param in zip(commands, params):
                try:
                    if command == _main_point.__name__:  # create instance
                        ins = _main_point(*param)
                        result.append(None)
                    else:  # call method
                        method = getattr(ins, command)
                        result.append(method(*param))
                except TypeError as e:
                    raise TypeError(f"Error occurred when calling `{command}` with `{param}`") from e
        print(_dump_output(result))


def _test_solution(testcase: TestCase) -> typing.List[Result]:
    cls = vars(sys.modules[_main_point.__module__])[_main_point.__qualname__.split('.')[0]]
    input_lines = testcase.input_str.strip().split('\n')
    raw_input_args = [line.strip() for line in input_lines]

    signature = inspect.signature(_main_point)
    if len(raw_input_args) % (len(signature.parameters) - 1) != 0:
        raise ValueError("The number of input arguments is not a multiple of the number of parameters")

    results = []

    for i in range(0, len(raw_input_args), len(signature.parameters) - 1):
        instance = cls()
        params = _parse_params(raw_input_args[i:i + len(signature.parameters) - 1],
                               list(signature.parameters.values())[1:])
        try:
            with timeit_block(testcase.timeit):
                raw_result = _main_point(instance, *params)
            res_obj = Result(raw_result, signature.return_annotation)
            results.append(res_obj)
            # print the output if needed
            if testcase.print_output:
                print(res_obj)
        except TypeError as e:
            raise TypeError(f"Error occurred when calling `{_main_point.__name__}` with `{params}`") from e

    return results


if sys.version_info >= (3, 9):
    ResultList = list[Result]
else:
    ResultList = typing.List[Result]


def test(*args, **kwargs) -> ResultList:
    global _main_point

    testcase = TestCase(*args, **kwargs)
    if _main_point is None:
        # Try to find the default main points to injects
        _try_dynamic_inject()

    # After the dynamic inject, the main is still None, raise an error
    if _main_point is None:
        raise RuntimeError("Please inject main_point first")
    if inspect.isclass(_main_point):
        # may be a design problem
        return _test_design(testcase)
    else:
        # may be a regular algorithm problem
        return _test_solution(testcase)


def _get_outer_methods(cls):
    outer_methods = []
    for name, obj in cls.__dict__.items():
        if inspect.isfunction(obj) and not name.startswith('_'):
            outer_methods.append(obj)
    return outer_methods


_leetCodeDataStructureClassNames = (
    'ListNode', 'TreeNode',
    # 'TreeLinkNode', 'UndirectedGraphNode'
)


def _try_dynamic_inject():
    top_level_environment = sys.modules['__main__']
    top_level_env_dict = top_level_environment.__dict__

    # replace the data structure class if it is defined in the file
    for cls_name in _leetCodeDataStructureClassNames:
        if cls_name in top_level_env_dict:
            cls = top_level_env_dict[cls_name]
            # patch the __repr__ and __str__ methods
            cls.__repr__ = cls.__str__ = (
                lambda ins: f'{type(ins).__name__}(val={ins.val if "val" in ins.__dict__ else "???"})'
            )
            import leeco.data_structures as ds
            setattr(ds, cls_name, cls)

    if 'Solution' in top_level_env_dict:
        # Found the Solution class, try to inject the main point method
        SolutionCls = top_level_environment.Solution
        # If there is only one outer method, inject it
        outer_methods = _get_outer_methods(SolutionCls)
        if len(outer_methods) == 1:
            inject(outer_methods[0])
        else:
            print("Since there are multiple outer methods defined in the Solution class, "
                  "you need to inject the main point manually")
    else:
        # May be a design problem, try to find the class
        classes = inspect.getmembers(top_level_environment, inspect.isclass)
        # Filter the class which is defined in the file and not a private class
        # todo exclude the data structure classes
        classes = [cls for name, cls in classes if cls.__module__ == '__main__' and not name.startswith('_')]
        if len(classes) == 1:
            inject(classes[0])
        else:
            print("Since there are multiple classes defined in the file, you need to inject the main point manually")
