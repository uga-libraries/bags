"""Test for the script undo_all_bags.py"""
import os
import shutil
import subprocess
import unittest
from test_functions import make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete test files."""
        shutil.rmtree(os.path.join(os.getcwd(), 'test_undo_bags'))

    def test_script(self):
        """Test for correct operation of the undo_all_bags.py script."""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_undo_bags_copy'),
                        os.path.join(os.getcwd(), 'test_undo_bags'))

        # Runs the script.
        script_path = os.path.join('..', 'undo_all_bags.py')
        bag_dir = os.path.join(os.getcwd(), 'test_undo_bags')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests that the contents of the folders are correct.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'aip_1'),
                    os.path.join(bag_dir, 'aip_1', 'Test File.txt'),
                    os.path.join(bag_dir, 'aip_2'),
                    os.path.join(bag_dir, 'aip_2', 'File_One.txt'),
                    os.path.join(bag_dir, 'aip_2', 'File_Two.txt')]
        self.assertEqual(expected, result, "Problem with test for undo_all_bags script")


if __name__ == '__main__':
    unittest.main()
