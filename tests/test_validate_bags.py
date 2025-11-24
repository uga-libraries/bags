"""Tests for the script validate_bags.py"""
import os
import subprocess
import unittest
from test_functions import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the bag validation report, if made"""
        tests = ['all_invalid', 'all_valid', 'mix', 'one']
        for test in tests:
            report_path = os.path.join(os.getcwd(), 'test_validate_bags', test, 'bag_validation_log.csv')
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_all_invalid(self):
        """Test for when there are multiple bags in the directory, all invalid."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_dir = os.path.join('test_validate_bags', 'all_invalid')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Bag_Valid', 'Errors'],
                    [os.path.join(bag_dir, 'aip_1_bag'), 'False',
                     'Payload-Oxum validation failed. Expected 1 files and 19 bytes but found 1 files and 42 bytes'],
                    [os.path.join(bag_dir, 'aip_2_bag'), 'False',
                     'Payload-Oxum validation failed. Expected 2 files and 51 bytes but found 1 files and 26 bytes']]
        self.assertEqual(expected, result, "Problem with test for all invalid")

    def test_all_valid(self):
        """Test for when there are multiple bags in the directory, all valid."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_dir = os.path.join('test_validate_bags', 'all_valid')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Bag_Valid', 'Errors'],
                    [os.path.join(bag_dir, 'aip_1_bag'), 'True', 'BLANK'],
                    [os.path.join(bag_dir, 'aip_2_bag'), 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for all valid")

    def test_mix(self):
        """Test for when there are multiple things in the directory: valid bag, invalid bag, and not a bag."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_dir = os.path.join('test_validate_bags', 'mix')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Bag_Valid', 'Errors'],
                    [os.path.join(bag_dir, 'aip_1_bag'), 'True', 'BLANK'],
                    [os.path.join(bag_dir, 'aip_2_bag'), 'False',
                     'Payload-Oxum validation failed. Expected 2 files and 51 bytes but found 1 files and 25 bytes']]
        self.assertEqual(expected, result, "Problem with test for mix")

    def test_one(self):
        """Test for when there is only one bag in the directory, which is valid."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_dir = os.path.join('test_validate_bags', 'one')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Tests the log contents.
        result = csv_to_list(os.path.join(bag_dir, 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Bag_Valid', 'Errors'],
                    [os.path.join(bag_dir, 'aip_1_bag'), 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for one valid")


if __name__ == '__main__':
    unittest.main()
