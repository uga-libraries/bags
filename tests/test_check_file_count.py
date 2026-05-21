import os
import shutil
import subprocess
import unittest
from test_functions import csv_to_list


def make_input(feature_dict):
    """Make a folder file_count_bag_dir with the subfolders and number of files indicated in the feature dictionary"""
    bag_dir = os.path.join(os.getcwd(), 'file_count_bag_dir')
    os.mkdir(bag_dir)
    for folder in feature_dict.keys():
        folder_path = os.path.join(bag_dir, folder)
        os.mkdir(folder_path)
        file_count = feature_dict[folder]
        for i in range(file_count):
            with open(os.path.join(folder_path, f'file_{i}.txt'), 'w') as f:
                f.write("Test file")


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copy of test data, if made"""
        bag_dir = os.path.join(os.getcwd(), 'file_count_bag_dir')
        if os.path.exists(bag_dir):
            shutil.rmtree(bag_dir)

    def test_nested_folders(self):
        """Test for when the folders in bag_dir contain other folders"""
        # Make test data and run the script.
        make_input({'a': 1, 'a/a': 2, 'b': 1000, 'b/b': 3000, 'b/b/b': 7000})
        script_path = os.path.join('..', 'check_file_count.py')
        bag_dir = os.path.join(os.getcwd(), 'file_count_bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'file_count_check.csv'))
        expected = [['Folder', 'Files', 'Files_OK'],
                    ['a', '3', 'True'],
                    ['b', '11000', 'False']]
        self.assertEqual(expected, result, "Problem with test for nested_folders")

    def test_skip_files(self):
        """Test for when there are files (not included) as well as folders in bag_dir"""
        # Make test data.
        make_input({'a': 1, 'b': 10, 'c': 10000})
        bag_dir = os.path.join(os.getcwd(), 'file_count_bag_dir')
        with open(os.path.join(bag_dir, 'file.txt'), 'w') as f:
            f.write("Test file")
        with open(os.path.join(bag_dir, 'metadata.csv'), 'w') as f:
            f.write("Test file")

        # Run the script.
        script_path = os.path.join('..', 'check_file_count.py')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'file_count_check.csv'))
        expected = [['Folder', 'Files', 'Files_OK'],
                    ['a', '1', 'True'],
                    ['b', '10', 'True'],
                    ['c', '10000', 'False']]
        self.assertEqual(expected, result, "Problem with test for skip_files")

    def test_small_enough(self):
        """Test for when every folder has fewer than the maximum 10,000 files"""
        # Make test data and run the script.
        make_input({'a': 1, 'b': 10, 'c': 1000})
        script_path = os.path.join('..', 'check_file_count.py')
        bag_dir = os.path.join(os.getcwd(), 'file_count_bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'file_count_check.csv'))
        expected = [['Folder', 'Files', 'Files_OK'],
                    ['a', '1', 'True'],
                    ['b', '10', 'True'],
                    ['c', '1000', 'True']]
        self.assertEqual(expected, result, "Problem with test for small_enough")

    def test_too_big(self):
        """Test for when every folder has equal to or more than the maximum 10,000 files"""
        # Make test data and run the script.
        make_input({'a': 10000, 'b': 10001})
        script_path = os.path.join('..', 'check_file_count.py')
        bag_dir = os.path.join(os.getcwd(), 'file_count_bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'file_count_check.csv'))
        expected = [['Folder', 'Files', 'Files_OK'],
                    ['a', '10000', 'False'],
                    ['b', '10001', 'False']]
        self.assertEqual(expected, result, "Problem with test for too_big")


if __name__ == '__main__':
    unittest.main()
