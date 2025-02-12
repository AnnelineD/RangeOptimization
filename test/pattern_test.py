import unittest

from src.pattern import minimal_seq, pattern_ext, repetition_ext, repetition_offset, one_up, pattern


class PatternGenerationTests(unittest.TestCase):
    def test_minimal_seq(self):
        self.assertEqual(minimal_seq([25, 24, 25, 24]), [25, 24])
        self.assertEqual(minimal_seq([4, 4, 4]), [4])
        self.assertEqual(minimal_seq([1, 2, 3]), [1, 2, 3])
        self.assertEqual(minimal_seq([1, 2, 3, 1, 2]), [1, 2, 3])       # TODO this is not desirable
        self.assertEqual(minimal_seq([]), [])

    def test_pattern_generation(self):
        self.assertEqual([0, 3, 6, 9, 2, 5, 8, 1, 4, 7], pattern(3, 0, 10))
        self.assertEqual([1, 4, 7, 0, 3, 6, 9, 2, 5, 8], pattern(3, 1, 10))
        self.assertEqual([2, 5, 8, 1, 4, 7, 0, 3, 6, 9], pattern(3, 2, 10))

        self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], pattern(7, 0, 10))

        self.assertEqual([0, 15, 30, 45, 60, 75, 90, 5, 20, 35, 50, 65, 80, 95, 10, 25, 40, 55, 70, 85], pattern_ext(15, 0, 10))
        self.assertEqual([0, 89, 78, 67, 56, 45, 34, 23, 12, 1, 90, 79, 68, 57, 46, 35, 24, 13, 2, 91, 80, 69, 58, 47, 36, 25, 14, 3, 92, 81, 70, 59, 48, 37, 26, 15, 4, 93, 82, 71, 60, 49, 38, 27, 16, 5, 94, 83, 72, 61, 50, 39, 28, 17, 6, 95, 84, 73, 62, 51, 40, 29, 18, 7, 96, 85, 74, 63, 52, 41, 30, 19, 8, 97, 86, 75, 64, 53, 42, 31, 20, 9, 98, 87, 76, 65, 54, 43, 32, 21, 10, 99, 88, 77, 66, 55, 44, 33, 22, 11],
                         pattern_ext(89, 0, 10))

        self.assertEqual([0], pattern(0, 0, 10))
        self.assertEqual([3], pattern(0, 3, 10))

        self.assertEqual([0, 5], pattern(5, 0, 10))

    def test_repetition_generation(self):
        self.assertEqual([4, 3, 3], repetition_offset(3, 0, 10))
        self.assertEqual([3, 4, 3], repetition_offset(3, 1, 10))
        self.assertEqual([3, 3, 4], repetition_offset(3, 2, 10))

        self.assertEqual([2, 1, 2, 1, 2, 1, 1], repetition_offset(7, 0, 10))
        self.assertEqual([2, 1, 2, 1, 1, 2, 1], repetition_offset(7, 1, 10))
        self.assertEqual([2, 1, 1, 2, 1, 2, 1], repetition_offset(7, 2, 10))
        self.assertEqual([1, 2, 1, 2, 1, 2, 1], repetition_offset(7, 3, 10))
        self.assertEqual([1, 2, 1, 2, 1, 1, 2], repetition_offset(7, 4, 10))

        self.assertEqual([0], repetition_offset(0, 5, 10))

    def test_one_up(self):
        # e.g. 23
        # pattern(3) = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
        # repetition(5) = [4, 3, 3]
        # pattern: [0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
        # one_up : [0, 2, 4, 6, 9, 1, 3, 6, 8, 0, 3, 5, 7, 9, 2, 4, 6, 9, 1, 3, 6, 8, 0, 2, 5, 7, 9, 2, 4, 6]
        self.assertEqual([0, 2, 4, 6, 9, 1, 3, 6, 8, 0, 3, 5, 7, 9, 2, 4, 6, 9, 1, 3, 6, 8, 0, 2, 5, 7, 9, 2, 4, 6, 9, 1, 3, 5, 8, 0, 2, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 8, 0, 2, 5, 7, 9, 1, 4, 6, 8, 1, 3, 5, 8, 0, 2, 4, 7, 9, 1, 4, 6, 8, 1, 3, 5, 7, 0, 2, 4, 7, 9, 1, 4, 6, 8, 0, 3, 5, 7, 0, 2, 4, 7, 9, 1, 3, 6, 8, 0, 3, 5, 7],
                         (one_up([4, 3, 3], 10, 2)[:100]))


        # e.g. 25
        # pattern(5) = [0, 5]
        # repetition(5) = [2]
        # pattern: 0 5 0 5 0 5 0 5
        # one_up : 0 2 5 7 0 2 5 7
        self.assertEqual([0, 2, 5, 7]*50, one_up([2], 10, 2))

        print(minimal_seq(one_up([4, 3, 3], 10, 0)))



if __name__ == '__main__':
    unittest.main()
