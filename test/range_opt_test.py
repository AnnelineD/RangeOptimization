import unittest
from random import randint

from src.base_calc import order
from src.range_optimization_nonrestricted import crange, to_number_special


def compare_range(start, stop, step, base) -> bool:
    rn, l = crange(start, stop, step, base)

    wanted_range = list(range(start, stop, step))
    opt_range = [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))]

    return wanted_range == opt_range

def compare_ranges(args) -> list[tuple]:
    return [a for a in args if not compare_range(*a)]



class HandpickedTests(unittest.TestCase):
    def test_only_one_path(self):
        tests = [(923, 931, 93, 10),
                 (75, 92, 19, 10)]

        self.assertListEqual([], compare_ranges(tests))

    def test_size_intermediate_layers_edge_case(self):
        tests = [(0, 292815, 8, 10)]   # edge case for size intermediate layers!

        self.assertListEqual([], compare_ranges(tests))

    def test_minimal_sequence(self):
        tests = [(1087, 9000, 87, 10),  # minimal_seq(r1)
                 (1087, 9000, 15, 10)]

        self.assertListEqual([], compare_ranges(tests))

    def test_previously_wrong(self):
        tests = [
            (611, 30000, 37, 10),
            (730, 3000, 2, 10),
            (7, 3000, 69, 10),
            (312, 15000, 15, 10),
            (10, 15, 5, 10),
            (47, 91, 15, 10),
            (47, 200, 15, 10),
            (101, 229, 66, 10),
            (121, 1165, 3, 10),
        ]

        self.assertListEqual([], compare_ranges(tests))

    def test_separate_nodes_cases(self):
        """Seperate start/stop examples

        | start | stop  | TO | start | stop  | example        |
        |-------|-------|----|-------|-------|----------------|
        | True  | True  |    | True  | True  | (88, 2186, 15) |
        | True  | False |    | True  | True  | (88, 2100, 15) |
        | True  | False |    | True  | False | (88, 9990, 15) |
        | False | True  |    | True  | True  | (312, 9990, 15)|
        | False | True  |    | False | True  | (10, 2186, 15) |
        | False | False |    | False | False | (10, 9990, 15) |
        | False | False |    | True  | False | (312, 9990, 15)|
        | False | False |    | False | True  | (10, 15000, 15), (10, 150000, 15)|
        | False | False |    | True  | True  | (312, 15000, 15)|

        """


        test_all_cases = [(88, 2186, 15, 10),
                          (88, 2100, 15, 10),
                          (88, 9990, 15, 10),

                          (10, 2186, 15, 10),
                          (10, 9990, 15, 10),
                          (312, 9990, 15, 10),
                          (10, 15000, 15, 10),
                          (10, 150000, 15, 10),
                          (312, 15000, 15, 10)
                          ]

        self.assertListEqual([], compare_ranges(test_all_cases))


class AutomaticTestCase(unittest.TestCase):
    def param_generator(self, base = None):
        if not base:
            base = randint(1, 200)

        step = randint(1, 99)
        start = randint(0, 100)
        stop = randint(start, 300000)

        return start, stop, step, base


    def test_base_10(self):
        tests = [self.param_generator(10) for _ in range(100)]
        self.assertListEqual([], compare_ranges(tests))

    def test_base_16(self):
        tests = [self.param_generator(16) for _ in range(100)]
        self.assertListEqual([], compare_ranges(tests))

    def test_random_bases(self):
        tests = [self.param_generator() for _ in range(100)]
        self.assertListEqual([], compare_ranges(tests))


if __name__ == '__main__':
    unittest.main()
