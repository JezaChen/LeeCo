# LeeCo: A utility for empowering debugging LeetCode problems locally in Python

[![PyPI version](https://badge.fury.io/py/leeco.svg)](https://badge.fury.io/py/leeco)

## Introduction

For some LeetCode problems related to Binary Tree, Linked List, etc.,
it is always difficult to debug the code locally with testcases provided by LeetCode,
since the input and output format is customized
(For example, the representation of a binary tree / linked list is a list of integers,
and the input of design problems is sequences of operations and parameters.)
and you may write a lot of test codes manually to debug the code locally.

This package provides a utility to help you debug the code locally with these testcases without
struggling with the input and output format.

## Installation

Just run the following command to install the package.

```bash
pip install leeco
```

## Usage

In most cases, You just add the `__main__` block in your code without modifying the original solution code.
And write the testcases in the `__main__` block as follows.

```python

# <Your solution code here>

if __name__ == "__main__":
    import leeco
    leeco.test("""
<Your testcases here, same as the input format of LeetCode>
    """)
```

If you define more than one outer function (whose name is not started with `_`) in `Solution` class, 
you should manually specify the main function (defined by LeetCode) to test.

```python
class Solution:
    def function1(self, ...):
        # The outer function defined by you
        pass

    def mainPoint(self, ...):
        # The main function defined by LeetCode
        pass


if __name__ == "__main__":
    import leeco

    leeco.inject(Solution.mainPoint)
    leeco.test("""
<Your testcases here, same as the input format of LeetCode>
    """)
```

For design problems, if you define more than one outer class (whose name is not started with `_`) in your code,
you should manually specify the main class (defined by LeetCode) to test.

```python
class YourClass:
    """ The class defined by you """
    
class MainClass:
    """ The main class defined by LeetCode """

if __name__ == "__main__":
    import leeco
    leeco.inject(MainClass)
    leeco.test("""
<Your testcases here, same as the input format of LeetCode>
""")
```

And then debug the code, add breakpoints and do anything you want with your favorite IDE or text editor.

## TODOs

- [ ] When parse the input of list, support calling the parser of the element type.
- [ ] Support the problems related to the probability.
- [x] Support the timing of the function.
- [ ] Support fetching the official testcases from LeetCode.
- [ ] Support the recursive parsing of the input, e.g., List[List[int]].
- [ ] Support the comparison of the output with the expected output.
- [ ] Only expose the `test` and `inject` function to the user.
- [x] Support the replacement of `ListNode` or `TreeNode` defined by the user.
- [ ] Unit tests.

