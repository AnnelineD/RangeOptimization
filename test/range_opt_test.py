import unittest
from random import randint

from src.base_calc import order, to_number
from src.range_optimization_nonrestricted import crange


def compare_range(start, stop, step, base) -> bool:
    print(start, stop, step, base)
    rn, l = crange(start, stop, step, base)

    wanted_range = list(range(start, stop, step))
    opt_range = [to_number(i, base) for i in (sorted(map(tuple, rn.paths())))]

    return wanted_range == opt_range

def compare_ranges(args) -> list[tuple]:
    return [a for a in args if not compare_range(*a)]



class HandpickedTests(unittest.TestCase):
    def test_only_one_path(self):
        tests = [(923, 931, 93, 10),
                 (75, 92, 19, 10)]

        self.assertListEqual([], compare_ranges(tests))

    def test_one_layer_only(self):
        tests = [(0, 9, 3, 10), (2, 98, 15, 10)]
        test_with_to_add = [(1000, 1009, 3, 10)]

        self.assertListEqual([], compare_ranges(tests + test_with_to_add))

    def test_no_intermediate_layers(self):
        tests = [(0, 99, 3, 10), (175, 764, 87, 10), (81050, 90985, 3374, 10)]
        test_with_to_add = [(1000, 1099, 3, 10)]

        self.assertListEqual([], compare_ranges(tests + test_with_to_add))

    def test_size_intermediate_layers_edge_case(self):
        tests = [(0, 292815, 8, 10), (94, 2000, 8, 10)]   # edge case for size intermediate layers!

        self.assertListEqual([], compare_ranges(tests))

    def test_root_is_one_path(self):
        tests = [(11111, 11112, 3, 10),
                 (123222, 123589, 20, 10),
                 (9999095, 9999995, 15, 20)]

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
            (94210, 94283, 24, 2),   # start_group reset
            (100000, 292815, 80, 10)
        ]

        self.assertListEqual([], compare_ranges(tests))

    def test_cases_of_previous_algorithm(self):
        tests = [(0, 1002, 3, 10), (0, 2130, 3, 10), (0, 5201, 3, 10)]
        dangly_edges = [(199, 301, 3, 10), (4125, 4129, 3, 10), (199, 321, 3, 10)]
        tests2 = [(827, 2977, 8, 10), (121, 1165, 3, 10), (841, 1275, 7, 10)]

        self.assertListEqual([], compare_ranges(tests + dangly_edges + tests2))

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


class GeneratedTestCases(unittest.TestCase):
    def param_generator(self, max_step = 99, base = None):
        if not base:
            base = randint(2, 200)

        step = randint(1, max_step)
        start = randint(0, 100000)
        stop = randint(start, 300000)

        return start, stop, step, base


    def test_base_10(self):
        tests = [self.param_generator(99, 10) for _ in range(100)]
        self.assertListEqual([], compare_ranges(tests))

    def test_base_16(self):
        tests = [self.param_generator(99, 16) for _ in range(100)]
        self.assertListEqual([], compare_ranges(tests))

    def test_random_bases(self):
        tests = [self.param_generator() for _ in range(100)]
        self.assertListEqual([], compare_ranges(tests))

    def test_big_step_base_10(self):
        tests = [self.param_generator(99999, 10) for _ in range(50)]
        self.assertListEqual([], compare_ranges(tests))

    def test_big_step_any_base(self):
        tests = [self.param_generator(99999) for _ in range(50)]
        self.assertListEqual([], compare_ranges(tests))


if __name__ == '__main__':
    unittest.main()
