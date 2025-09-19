import os
import unittest
from delete_new_temp import find_extra_files


class MyTestCase(unittest.TestCase):

    def test_extra_not_temp(self):
        bag_path = os.path.join(os.getcwd(), 'extra_not_temp_bag')
        extra_files = find_extra_files(bag_path)
        expected = ['data/Extra.txt', 'data/Folder/Extra2.txt']
        self.assertEqual(expected, extra_files, "Problem with test for extra_not_temp")

    def test_extra_temp(self):
        bag_path = os.path.join(os.getcwd(), 'extra_temp_bag')
        extra_files = find_extra_files(bag_path)
        expected = ['data/.Document.txt', 'data/Document.tmp', 'data/Folder/Thumbs.db']
        self.assertEqual(expected, extra_files, "Problem with test for extra_temp")

    def test_no_extra(self):
        bag_path = os.path.join(os.getcwd(), 'no_extra_bag')
        extra_files = find_extra_files(bag_path)
        expected = []
        self.assertEqual(expected, extra_files, "Problem with test for extra_not_temp")


if __name__ == '__main__':
    unittest.main()
