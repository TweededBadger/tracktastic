
from unittest import TestCase
import unittest


class MyTestCase(TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
