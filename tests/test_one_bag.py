"""Tests for the script undo_one_bag.py

Unable to get the test to work if the bag requires renaming (ends with "_bag")
due to a permissions issue during the renaming.
"""
import os
import shutil
import subprocess
import unittest
from test_functions import make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete test files."""
        shutil.rmtree('test_copy')

    def test_no_rename(self):
        """Test for correct operation of the undo_one_bag.py script if no renaming is needed."""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join('test_undo_bags', 'aip_2_bag'), 'test_copy')

        # Runs the script.
        script_path = os.path.join('..', 'undo_one_bag.py')
        bag_path = os.path.join(os.getcwd(), 'test_copy')
        subprocess.run(f'python {script_path} {bag_path}', shell=True)

        # Tests that the contents of the folder are correct.
        result = make_directory_list(bag_path)
        expected = [os.path.join(bag_path, 'File_One.txt'),
                    os.path.join(bag_path, 'File_Two.txt')]
        self.assertEqual(expected, result, "Problem with test for no rename")


if __name__ == '__main__':
    unittest.main()
