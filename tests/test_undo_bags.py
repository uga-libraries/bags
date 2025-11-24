"""Test for the script undo_bags.py"""
import os
import shutil
import subprocess
import unittest
from test_functions import make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete test files, if present"""
        test_dir = os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir')
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_one(self):
        """Test for when there is one bag in bag_dir"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_undo_bags', 'one_copy'),
                        os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir'))

        # Runs the script.
        script_path = os.path.join('..', 'undo_bags.py')
        bag_dir = os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests that the contents of the folders are correct.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'aip_1'),
                    os.path.join(bag_dir, 'aip_1', 'Test File.txt')]
        self.assertEqual(expected, result, "Problem with test for one")

    def test_two(self):
        """Test for when there are two bags in bag_dir"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_undo_bags', 'two_copy'),
                        os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir'))

        # Runs the script.
        script_path = os.path.join('..', 'undo_bags.py')
        bag_dir = os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests that the contents of the folders are correct.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'aip_1'),
                    os.path.join(bag_dir, 'aip_1', 'Test File.txt'),
                    os.path.join(bag_dir, 'aip_2'),
                    os.path.join(bag_dir, 'aip_2', 'File_One.txt'),
                    os.path.join(bag_dir, 'aip_2', 'File_Two.txt')]
        self.assertEqual(expected, result, "Problem with test for two")


if __name__ == '__main__':
    unittest.main()
