# -*- encoding:utf-8 -*-
import unittest


class TestTestcaseStructure(unittest.TestCase):
    def test_testcase_structure(self):
        from leeco.structs import TestCase

        # Test the metaclass _TestCaseMeta
        t = TestCase("input", "expected_output")
        t2 = TestCase(t)
        self.assertIs(t, t2)

        # Test the __init__ method
        t3 = TestCase("input", "expected_output")
        self.assertIsNot(t, t3)

        # Test the attributes
        self.assertEqual(t.input_str, "input")
        self.assertEqual(t.expected_output_str, "expected_output")
        self.assertEqual(t3.input_str, "input")
        self.assertEqual(t3.expected_output_str, "expected_output")

        # Test the __repr__ method
        self.assertEqual(repr(t), "TestCase(input, expected_output)")
        self.assertEqual(repr(t3), "TestCase(input, expected_output)")
        self.assertEqual(repr(t2), "TestCase(input, expected_output)")

