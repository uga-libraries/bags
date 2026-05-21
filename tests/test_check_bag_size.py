import os
import subprocess
import unittest
from test_functions import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the csv created by the test, if made"""
        test_folders = ['skip', 'small_enough', 'too_big']
        for test_folder in test_folders:
            csv_path = os.path.join('test_check_bag_size', test_folder, 'bag_size_check.csv')
            if os.path.exists(csv_path):
                os.remove(csv_path)

    def test_skip_files(self):
        """Test for when there are files (not included in the analysis) as well as bags in bag_dir"""
        # Make variables and run the script.
        script_path = os.path.join('..', 'check_bag_size.py')
        bag_dir = os.path.join(os.getcwd(), 'test_check_bag_size', 'skip')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_size_check.csv'))
        expected = [['Bag', 'Size_GB', 'Size_OK', 'Files', 'Files_OK'],
                    ['aip1_bag', '0.018', 'True', '1.0', 'True'],
                    ['aip2_bag', '270.0', 'False', '15000.0', 'False']]
        self.assertEqual(expected, result, "Problem with test for skip_files")
        
    def test_small_enough(self):
        """Test for when all bags in bag_dir have few enough files and GB"""
        # Make variables and run the script.
        script_path = os.path.join('..', 'check_bag_size.py')
        bag_dir = os.path.join(os.getcwd(), 'test_check_bag_size', 'small_enough')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_size_check.csv'))
        expected = [['Bag', 'Size_GB', 'Size_OK', 'Files', 'Files_OK'],
                    ['aip1_bag', '0.001234567', 'True', '61.5', 'True'],
                    ['aip2_bag', '99.999999999', 'True', '9999.5', 'True']]
        self.assertEqual(expected, result, "Problem with test for small_enough")

    def test_too_big(self):
        """Test for when all bags in bag_dir have too many files and/or GB"""
        # Make variables and run the script.
        script_path = os.path.join('..', 'check_bag_size.py')
        bag_dir = os.path.join(os.getcwd(), 'test_check_bag_size', 'too_big')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the csv contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_size_check.csv'))
        expected = [['Bag', 'Size_GB', 'Size_OK', 'Files', 'Files_OK'],
                    ['aip1_bag', '333.0', 'False', '1.0', 'True'],
                    ['aip2_bag', '2.7', 'True', '50000.0', 'False'],
                    ['aip3_bag', '100.0', 'False', '10000.0', 'False']]
        self.assertEqual(expected, result, "Problem with test for too_big")


if __name__ == '__main__':
    unittest.main()
