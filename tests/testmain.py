import unittest
from code import Example


class TestExample(unittest.TestCase):

    def test_example_true(self):
        example = Example()
        result = example.example_function(True)
        self.assertTrue(result)

    def test_example_false(self):
        example = Example()
        result = example.example_function(False)
        self.assertFalse(result)

