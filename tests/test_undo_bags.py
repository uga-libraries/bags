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

    def test_hierarchy(self):
        """Test for when there is a bag deeper in the hierarchy of bag_dir that should not be undone"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_undo_bags', 'hierarchy_copy'),
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
                    os.path.join(bag_dir, 'aip_2', 'File_Two.txt'),
                    os.path.join(bag_dir, 'folder'),
                    os.path.join(bag_dir, 'folder', 'keep_bag'),
                    os.path.join(bag_dir, 'folder', 'keep_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'folder', 'keep_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'folder', 'keep_bag', 'data'),
                    os.path.join(bag_dir, 'folder', 'keep_bag', 'data', 'Test File.txt'),
                    os.path.join(bag_dir, 'folder', 'keep_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'folder', 'keep_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for hierarchy")

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

    def test_unexpected_error(self):
        """Test for when a bag has other files and a folder mixed with the bag metadata files"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_undo_bags', 'unexpected_error_copy'),
                        os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir'))

        # Runs the script.
        script_path = os.path.join('..', 'undo_bags.py')
        bag_dir = os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests that the contents of the folders are correct.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'aip_1_bag'),
                    os.path.join(bag_dir, 'aip_1_bag', 'a_extra_file.txt'),
                    os.path.join(bag_dir, 'aip_1_bag', 'aip_1_FITS'),
                    os.path.join(bag_dir, 'aip_1_bag', 'aip_1_FITS', 'FITS Placeholder.txt'),
                    os.path.join(bag_dir, 'aip_1_bag', 'data'),
                    os.path.join(bag_dir, 'aip_1_bag', 'data', 'Test File.txt'),
                    os.path.join(bag_dir, 'aip_1_bag', 'extra_file2.txt'), ]
        self.assertEqual(expected, result, "Problem with test for unexpected_error")

    def test_validation_error(self):
        """Test for when there are two bags in bag_dir and one is not valid (is not undone)"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_undo_bags', 'validation_error_copy'),
                        os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir'))

        # Runs the script.
        script_path = os.path.join('..', 'undo_bags.py')
        bag_dir = os.path.join(os.getcwd(), 'test_undo_bags', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests that the contents of the folders are correct.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'not_valid_bag'),
                    os.path.join(bag_dir, 'not_valid_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'not_valid_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'not_valid_bag', 'data'),
                    os.path.join(bag_dir, 'not_valid_bag', 'data', 'Test File.txt'),
                    os.path.join(bag_dir, 'not_valid_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'not_valid_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'valid'),
                    os.path.join(bag_dir, 'valid', 'File_One.txt'),
                    os.path.join(bag_dir, 'valid', 'File_Two.txt')]
        self.assertEqual(expected, result, "Problem with test for validation_error")


if __name__ == '__main__':
    unittest.main()
