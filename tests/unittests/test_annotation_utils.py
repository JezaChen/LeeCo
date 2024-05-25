# -*- encoding:utf-8 -*-
import unittest
import sys
from typing import Optional, Union, List


class TestAnnotationUtils(unittest.TestCase):
    def test_is_optional(self):
        from leeco._annotation_utils import is_optional

        self.assertTrue(is_optional(Optional[int]))
        self.assertTrue(is_optional(Union[int, None]))
        self.assertTrue(is_optional(Union[None, int]))
        self.assertTrue(is_optional(Union[int, str, None]))
        if sys.version_info >= (3, 9):
            self.assertTrue(is_optional(int | None))
        self.assertFalse(is_optional(int))
        self.assertFalse(is_optional(None))
        self.assertFalse(is_optional(Union[int, str]))
        self.assertFalse(is_optional(List[int]))

    def test_get_optional_type(self):
        from leeco._annotation_utils import get_optional_type

        self.assertEqual(get_optional_type(Optional[int]), int)
        self.assertEqual(get_optional_type(Union[int, None]), int)
        self.assertEqual(get_optional_type(Union[None, int]), int)
        if sys.version_info >= (3, 9):
            self.assertEqual(get_optional_type(int | None), int)
        with self.assertRaises(ValueError):
            get_optional_type(Union[int, str, None])
        with self.assertRaises(ValueError):
            get_optional_type(int)
        with self.assertRaises(ValueError):
            get_optional_type(None)
        with self.assertRaises(ValueError):
            get_optional_type(Union[int, str])

    def test_match_type(self):
        from leeco._annotation_utils import match_type

        # test basic types
        self.assertTrue(match_type(int, int))
        self.assertTrue(match_type(str, str))
        self.assertTrue(match_type(None, None))
        self.assertFalse(match_type(int, str))
        self.assertFalse(match_type(int, None))
        self.assertFalse(match_type(None, int))
        self.assertFalse(match_type(int, list))
        self.assertFalse(match_type(int, List[int]))

        # test optional
        self.assertTrue(match_type(Optional[int], int))
        self.assertTrue(match_type(Optional[int], None))
        self.assertTrue(match_type(Union[int, None], int))
        self.assertTrue(match_type(Union[None, int], int))
        if sys.version_info >= (3, 9):
            self.assertTrue(match_type(int | None, int))
        self.assertTrue(match_type(None | int, int))
        self.assertFalse(match_type(Optional[int], str))
        self.assertFalse(match_type(Optional[int], List[int]))
        self.assertFalse(match_type(Union[int, None], str))
        self.assertFalse(match_type(Union[int, None], List[int]))

        # test union
        # in these case, if the union contains more than one type except None, it will return False
        self.assertFalse(match_type(Union[int, str], int))
        self.assertFalse(match_type(Union[int, str], str))
        self.assertFalse(match_type(Union[int, str], List[int]))
        with self.assertRaises(ValueError):
            self.assertFalse(match_type(Optional[Union[int, str]], Union[int, str]))

        # test list
        self.assertTrue(match_type(List[int], list))
        self.assertTrue(match_type(List[int], List))
        self.assertFalse(match_type(List[List[int]], List[int]))
        self.assertFalse(match_type(List[List[int]], List[List[str]]))

        # test optional list
        self.assertTrue(match_type(Optional[List[int]], list))
        self.assertTrue(match_type(Optional[List[int]], List[int]))
        self.assertTrue(match_type(Union[List[int], None], list))
        self.assertTrue(match_type(Union[List[int], None], List[int]))
        if sys.version_info >= (3, 9):
            self.assertTrue(match_type(List[int] | None, list))
            self.assertTrue(match_type(List[int] | None, List[int]))

        self.assertFalse(match_type(List[int], int))
        self.assertFalse(match_type(List[int], str))
        self.assertFalse(match_type(List[int], List[str]))
        self.assertFalse(match_type(Optional[List[int]], int))
        self.assertFalse(match_type(Optional[List[int]], str))
        self.assertFalse(match_type(Optional[List[int]], List[str]))
        self.assertFalse(match_type(Union[List[int], None], int))
        self.assertFalse(match_type(Union[List[int], None], str))
        self.assertFalse(match_type(Union[List[int], None], List[str]))
        if sys.version_info >= (3, 9):
            self.assertFalse(match_type(List[int] | None, int))
            self.assertFalse(match_type(List[int] | None, str))
            self.assertFalse(match_type(List[int] | None, List[str]))

        with self.assertRaises(ValueError):
            match_type(Union[int, str, None], int)

    def test_get_elem_type(self):
        from leeco._annotation_utils import get_elem_type

        self.assertEqual(get_elem_type(List[int]), int)
        self.assertEqual(get_elem_type(List[List[int]]), List[int])
        self.assertEqual(get_elem_type(Optional[List[int]]), int)
        self.assertEqual(get_elem_type(Union[List[int], None]), int)
        self.assertEqual(get_elem_type(Union[None, List[int]]), int)
        if sys.version_info >= (3, 9):
            self.assertEqual(get_elem_type(List[int] | None), int)
            self.assertEqual(get_elem_type(None | List[int]), int)
        self.assertEqual(get_elem_type(int), None)
        self.assertEqual(get_elem_type(Optional[int]), None)
        self.assertEqual(get_elem_type(Union[List[int], List[str]]), None)
        self.assertEqual(get_elem_type(Union[List[int], int]), None)
