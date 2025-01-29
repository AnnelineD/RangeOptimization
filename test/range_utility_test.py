import unittest

from src.range_utility import find_last_number_of_range, find_group, strip_equal_start, number_of_nodes_per_layer


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(find_last_number_of_range(0, 100, 7), 98)
        self.assertEqual(find_last_number_of_range(1, 100, 7), 99)
        self.assertEqual(find_last_number_of_range(2, 100, 7), 93)

        self.assertEqual(find_last_number_of_range(0, 100, 3), 99)
        self.assertEqual(find_last_number_of_range(1, 100, 3), 97)
        self.assertEqual(find_last_number_of_range(2, 100, 3), 98)
        self.assertEqual(find_last_number_of_range(3, 100, 3), 99)

        self.assertEqual(find_last_number_of_range(100, 1234, 87), 1231)

    def test_find_group(self):
        self.assertEqual(find_group([0, 1, 2, 3, 4], [2, 2, 1], 0), (0, 0))
        self.assertEqual(find_group([0, 1, 2, 3, 4], [2, 2, 1], 1), (0, 1))
        self.assertEqual(find_group([0, 1, 2, 3, 4], [2, 2, 1], 2), (1, 0))
        self.assertEqual(find_group([0, 1, 2, 3, 4], [2, 2, 1], 3), (1, 1))
        self.assertEqual(find_group([0, 1, 2, 3, 4], [2, 2, 1], 4), (2, 0))

    def test_strip_start(self):
        self.assertEqual(strip_equal_start([0, 1, 2, 3], [0, 1, 3, 4]), ([2, 3], [3, 4], [0, 1]))
        self.assertEqual(strip_equal_start([0, 1, 2, 3], [1, 1, 2, 3]), ([0, 1, 2, 3], [1, 1, 2, 3], []))

    def test_num_nodes_per_layer(self):
       self.assertEqual(number_of_nodes_per_layer([0, 0, 0, 0], [1, 0, 0, 0], 5, 10), [1, 1])
       self.assertEqual(number_of_nodes_per_layer([0, 0, 0], [1, 0, 0], 5, 10), [1])
       self.assertEqual(number_of_nodes_per_layer([0, 0], [1, 0], 5, 10), [])
       self.assertEqual(number_of_nodes_per_layer([0], [1], 5, 10), [])

if __name__ == '__main__':
    unittest.main()
