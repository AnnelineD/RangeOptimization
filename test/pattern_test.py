import unittest

from src.pattern import minimal_seq


class MyTestCase(unittest.TestCase):
    def test_minimal_seq(self):
        self.assertEqual(minimal_seq([25, 24, 25, 24]), [25, 24])
        self.assertEqual(minimal_seq([4, 4, 4]), [4])
        self.assertEqual(minimal_seq([1, 2, 3]), [1, 2, 3])
        self.assertEqual(minimal_seq([]), [])


if __name__ == '__main__':
    unittest.main()
