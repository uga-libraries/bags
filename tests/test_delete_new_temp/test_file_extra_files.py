import os
import unittest
from delete_new_temp import find_extra_files


class MyTestCase(unittest.TestCase):

    def test_function(self):
        bag_path = os.path.join(os.getcwd(), 'test_data', 'find_extra_files', 'extra_bag')
        extra_files = find_extra_files(bag_path)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
