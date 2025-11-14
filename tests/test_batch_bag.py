import os
import shutil
import subprocess
import unittest
from test_functions import csv_to_list, make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copy of test data (bagged or not), if made"""
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        if os.path.exists(bag_dir):
            shutil.rmtree(bag_dir)

    def test_bag_all(self):
        """Test for when all folders should be bagged"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_batch_bag', 'bag_all'),
                        os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'batch_bag.py')
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the directory contents.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'aip1_bag'),
                    os.path.join(bag_dir, 'aip1_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'data'),
                    os.path.join(bag_dir, 'aip1_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'aip2_bag'),
                    os.path.join(bag_dir, 'aip2_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'data'),
                    os.path.join(bag_dir, 'aip2_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'data', 'aip2_subfolder'),
                    os.path.join(bag_dir, 'aip2_bag', 'data', 'aip2_subfolder', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'bag_validation_log.csv')]
        self.assertEqual(expected, result, "Problem with test for bag_all, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag', 'Valid?', 'Notes'],
                    ['aip1_bag', 'True', 'Valid'],
                    ['aip2_bag', 'True', 'Valid'],
                    ['bag_validation_log.csv', 'TBD', 'Skipped']]
        self.assertEqual(expected, result, "Problem with test for bag_all, log")

    def test_restart(self):
        """Test for when the script is restarted and skips any already bagged"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_batch_bag', 'restart'),
                        os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'batch_bag.py')
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the directory contents.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'A Text Document.txt'),
                    os.path.join(bag_dir, 'aip1_bag'),
                    os.path.join(bag_dir, 'aip1_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'data'),
                    os.path.join(bag_dir, 'aip1_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'aip2_bag'),
                    os.path.join(bag_dir, 'aip2_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'data'),
                    os.path.join(bag_dir, 'aip2_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'data', 'aip2_subfolder'),
                    os.path.join(bag_dir, 'aip2_bag', 'data', 'aip2_subfolder', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip2_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'aip3_bag'),
                    os.path.join(bag_dir, 'aip3_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip3_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip3_bag', 'data'),
                    os.path.join(bag_dir, 'aip3_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip3_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip3_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'aip4_bag'),
                    os.path.join(bag_dir, 'aip4_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip4_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip4_bag', 'data'),
                    os.path.join(bag_dir, 'aip4_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip4_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip4_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'bag_validation_log.csv')]
        self.assertEqual(expected, result, "Problem with test for restart, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag', 'Valid?', 'Notes'],
                    ['A Text Document.txt', 'TBD', 'Skipped'],
                    ['aip1_bag', 'True', 'Valid'],
                    ['aip2_bag', 'False', 'bagit error'],
                    ['A Text Document.txt', 'TBD', 'Skipped'],
                    ['aip3_bag', 'True', 'Valid'],
                    ['aip4_bag', 'True', 'Valid'],
                    ['bag_validation_log.csv', 'TBD', 'Skipped']]
        self.assertEqual(expected, result, "Problem with test for restart, log")

    def test_skip_bags(self):
        """Test for when not all folders should be bagged"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_batch_bag', 'skip_bags'),
                        os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'batch_bag.py')
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the directory contents.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'bag_validation_log.csv'),
                    os.path.join(bag_dir, 'folder1_bag'),
                    os.path.join(bag_dir, 'folder1_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'folder1_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'folder1_bag', 'data'),
                    os.path.join(bag_dir, 'folder1_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'folder1_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'folder1_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'folder2_bags'),
                    os.path.join(bag_dir, 'folder2_bags', 'folder2a'),
                    os.path.join(bag_dir, 'folder2_bags', 'folder2a', 'Test_File.txt'),
                    os.path.join(bag_dir, 'folder2_bags', 'folder2b'),
                    os.path.join(bag_dir, 'folder2_bags', 'folder2b', 'Test_File.txt'),
                    os.path.join(bag_dir, 'folder3_bag'),
                    os.path.join(bag_dir, 'folder3_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'folder3_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'folder3_bag', 'data'),
                    os.path.join(bag_dir, 'folder3_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'folder3_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'folder3_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for skip_bags, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag', 'Valid?', 'Notes'],
                    ['bag_validation_log.csv', 'TBD', 'Skipped'],
                    ['folder1_bag', 'True', 'Valid'],
                    ['folder2_bags', 'TBD', 'Skipped'],
                    ['folder3_bag', 'True', 'Valid']]
        self.assertEqual(expected, result, "Problem with test for skip_bags, log")

    def test_skip_files(self):
        """Test for when the bag_dir includes loose files (not bagged)"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_batch_bag', 'skip_files'),
                        os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'batch_bag.py')
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the directory contents.
        # This is just testing for folders, so it won't list the loose files.
        result = make_directory_list(bag_dir)
        expected = [os.path.join(bag_dir, 'Test_File.txt'),
                    os.path.join(bag_dir, 'a test file.txt'),
                    os.path.join(bag_dir, 'aip1_bag'),
                    os.path.join(bag_dir, 'aip1_bag', 'bag-info.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'bagit.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'data'),
                    os.path.join(bag_dir, 'aip1_bag', 'data', 'Test_File.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'manifest-md5.txt'),
                    os.path.join(bag_dir, 'aip1_bag', 'tagmanifest-md5.txt'),
                    os.path.join(bag_dir, 'bag_validation_log.csv')]
        self.assertEqual(expected, result, "Problem with test for skip_files, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag', 'Valid?', 'Notes'],
                    ['a test file.txt', 'TBD', 'Skipped'],
                    ['aip1_bag', 'True', 'Valid'],
                    ['bag_validation_log.csv', 'TBD', 'Skipped'],
                    ['Test_File.txt', 'TBD', 'Skipped']]
        self.assertEqual(expected, result, "Problem with test for skip_files, log")


if __name__ == '__main__':
    unittest.main()
