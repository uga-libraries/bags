import os
import re
import shutil
import unittest
from delete_new_temp import delete_temp


def make_directory_list(path):
    """Makes a list of the full paths of all files remaining in the bag data folder after deletion"""
    dir_list = []
    for root, dirs, files in os.walk(os.path.join(path, 'data')):
        for file in files:
            root_from_data = re.search(rf"{'data'}.*", root).group()
            dir_list.append(os.path.join(root_from_data, file))
    return dir_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copies of test data, if made"""
        bags = ['test_extra_not_temp_bag', 'test_extra_temp_bag', 'test_no_extra_bag']
        for bag in bags:
            if os.path.exists(os.path.join(os.getcwd(), bag)):
                shutil.rmtree(os.path.join(os.getcwd(), bag))

    def test_extra_not_temp(self):
        # Make a copy of the test data, since the function deletes files.
        bag_path = os.path.join(os.getcwd(), 'extra_not_temp_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_extra_not_temp_bag')
        shutil.copytree(bag_path, new_bag_path)
        extra_files = ['data/Extra.txt', 'data/Folder/Extra2.txt']
        not_deleted = delete_temp(new_bag_path, extra_files)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Extra.txt', 'data\\Folder\\Document.txt', 'data\\Folder\\Extra2.txt']
        self.assertEqual(expected, result, "Problem with test for extra_not_temp, directory")

        # Test for the returned list.
        expected = ['data/Extra.txt', 'data/Folder/Extra2.txt']
        self.assertEqual(expected, not_deleted, "Problem with test for extra_not_temp, list")

    def test_extra_temp(self):
        # Make a copy of the test data, since the function deletes files.
        bag_path = os.path.join(os.getcwd(), 'extra_temp_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_extra_temp_bag')
        shutil.copytree(bag_path, new_bag_path)
        extra_files = ['data/.Document.txt', 'data/Document.tmp', 'data/Folder/Thumbs.db']
        not_deleted = delete_temp(new_bag_path, extra_files)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for extra_temp, directory")

        # Test for the returned list.
        expected = []
        self.assertEqual(expected, not_deleted, "Problem with test for extra_temp, list")

    def test_no_extra(self):
        # Make a copy of the test data, since the function deletes files.
        bag_path = os.path.join(os.getcwd(), 'no_extra_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_no_extra_bag')
        shutil.copytree(bag_path, new_bag_path)
        extra_files = []
        not_deleted = delete_temp(new_bag_path, extra_files)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for no_extra, directory")

        # Test for the returned list.
        expected = []
        self.assertEqual(expected, not_deleted, "Problem with test for no_extra, list")


if __name__ == '__main__':
    unittest.main()
