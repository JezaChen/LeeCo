# -*- encoding:utf-8 -*-
import typing
import inspect
import sys

__all__ = ['inject', 'test']

from leeco._annotation_utils import is_optional, get_optional_type, match_type
from leeco._representations import ListParser, TreeNodeParser, TrivialParser, ListNodeParser, get_parser
from leeco.data_structures import TreeNode, ListNode

_main_point = None  # type: typing.Optional[typing.Callable]
_main_point_cls = None  # type: typing.Optional[typing.Type]


def inject(main_point: typing.Callable):
    global _main_point, _main_point_cls
    if inspect.isclass(main_point):
        _main_point_cls = main_point
        _main_point = None
    else:
        _main_point_cls = vars(sys.modules[main_point.__module__])[main_point.__qualname__.split('.')[0]]
        _main_point = main_point


def dump_output(output, annotation=None) -> str:
    output_type = type(output)
    if annotation is not None and annotation is not inspect.Parameter.empty:
        output_type = annotation
        if is_optional(annotation):
            output_type = get_optional_type(annotation)

    parser = get_parser(output_type)
    return parser.to_str(output)


_InputType = typing.TypeVar('_InputType')


def parse_input(input_str: str, input_type_annotation: typing.Type[_InputType]) -> _InputType:
    parser = get_parser(input_type_annotation)
    return parser.parse(input_str)


def parse_params(input_str_list: typing.List[str], param_list: typing.List[inspect.Parameter]) -> typing.List:
    if len(input_str_list) != len(param_list):
        raise ValueError("The number of input strings is not equal to the number of parameters")
    return [parse_input(input_str, param.annotation) for input_str, param in zip(input_str_list, param_list)]


def _test_design(input_expression: str, expected_result: str = ""):
    global _main_point_cls

    assert _main_point_cls is not None
    input_lines = input_expression.strip().split('\n')
    if len(input_lines) % 2:
        raise ValueError("The input expression must have 2 lines for each test case")

    for case_commands_input, case_params_input in zip(input_lines[::2], input_lines[1::2]):
        commands = TrivialParser.parse(case_commands_input.strip())
        params = TrivialParser.parse(case_params_input.strip())

        ins = None
        result = []

        for command, param in zip(commands, params):
            if command == _main_point_cls.__name__:  # create instance
                ins = _main_point_cls()
                result.append(None)
            else:  # call method
                method = getattr(ins, command)
                result.append(method(*param))
        print(dump_output(result))


def test(input_expression: str, expected_result: str = ""):
    global _main_point, _main_point_cls

    if _main_point is None and _main_point_cls is None:
        _try_dynamic_inject()
    if _main_point is None and _main_point_cls is None:
        raise RuntimeError("Please inject main_point first")
    if _main_point is None:
        # may be a design problem
        return _test_design(input_expression, expected_result)

    input_lines = input_expression.strip().split('\n')
    raw_input_args = [line.strip() for line in input_lines]

    signature = inspect.signature(_main_point)
    if len(raw_input_args) % (len(signature.parameters) - 1) != 0:
        raise ValueError("The number of input arguments is not a multiple of the number of parameters")

    for i in range(0, len(raw_input_args), len(signature.parameters) - 1):
        instance = _main_point_cls()
        params = parse_params(
            raw_input_args[i:i + len(signature.parameters) - 1],
            list(signature.parameters.values())[1:]
        )
        result = _main_point(instance, *params)
        print(dump_output(result, signature.return_annotation))


def _get_outer_methods(cls):
    outer_methods = []
    for name, obj in cls.__dict__.items():
        if inspect.isfunction(obj) and not name.startswith('_'):
            outer_methods.append(obj)
    return outer_methods


def _try_dynamic_inject():
    top_level_environment = sys.modules['__main__']

    if 'Solution' in top_level_environment.__dict__:
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
        classes = [cls for name, cls in classes if cls.__module__ == '__main__' and not name.startswith('_')]
        if len(classes) == 1:
            inject(classes[0])
        else:
            print("Since there are multiple classes defined in the file, you need to inject the main point manually")
