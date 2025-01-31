import unittest

from src.pattern import minimal_seq, pattern_ext


class PatternGenerationTests(unittest.TestCase):
    def test_minimal_seq(self):
        self.assertEqual(minimal_seq([25, 24, 25, 24]), [25, 24])
        self.assertEqual(minimal_seq([4, 4, 4]), [4])
        self.assertEqual(minimal_seq([1, 2, 3]), [1, 2, 3])
        self.assertEqual(minimal_seq([]), [])

    def test_pattern_generation(self):
        self.assertEqual([0, 3, 6, 9, 2, 5, 8, 1, 4, 7], pattern_ext(3, 0, 10))
        self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], pattern_ext(7, 0, 10))
        self.assertEqual([0, 15, 30, 45, 60, 75, 90, 5, 20, 35, 50, 65, 80, 95, 10, 25, 40, 55, 70, 85], pattern_ext(15, 0, 10))
        self.assertEqual([0, 89, 78, 67, 56, 45, 34, 23, 12, 1, 90, 79, 68, 57, 46, 35, 24, 13, 2, 91, 80, 69, 58, 47, 36, 25, 14, 3, 92, 81, 70, 59, 48, 37, 26, 15, 4, 93, 82, 71, 60, 49, 38, 27, 16, 5, 94, 83, 72, 61, 50, 39, 28, 17, 6, 95, 84, 73, 62, 51, 40, 29, 18, 7, 96, 85, 74, 63, 52, 41, 30, 19, 8, 97, 86, 75, 64, 53, 42, 31, 20, 9, 98, 87, 76, 65, 54, 43, 32, 21, 10, 99, 88, 77, 66, 55, 44, 33, 22, 11],
                         pattern_ext(89, 0, 10))

        self.assertEqual([0], pattern_ext(0, 0, 10))
        self.assertEqual([3], pattern_ext(0, 3, 10))


if __name__ == '__main__':
    unittest.main()
