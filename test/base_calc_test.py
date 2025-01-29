import unittest

from src.base_calc import numberToBase, to_number


class MyTestCase(unittest.TestCase):
    def test_number_to_base(self):
        self.assertEqual([1, 3, 2, 4], numberToBase(1324, 10))

        self.assertEqual([0], numberToBase(0, 5))

        self.assertEqual([1, 0, 1, 0], numberToBase(10, 2))

        self.assertEqual([1234], numberToBase(1234, 1))

        print(numberToBase(94210, 2))

    def test_to_number(self):
        self.assertEqual(1324, to_number([1, 3, 2, 4], 10))

        self.assertEqual(0, to_number([0], 5))

        self.assertEqual(10, to_number([1, 0, 1, 0], 2))

        self.assertEqual(1234, to_number([1234], 1))

        print(to_number([1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 2))


if __name__ == '__main__':
    unittest.main()
