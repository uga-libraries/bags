"""Tests for the script validate_bags.py"""
import os
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def test_all_invalid(self):
        """Test for when there are multiple bags in the directory, all invalid."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_directory = os.path.join('test_validate_bags', 'all_invalid')
        script_output = subprocess.run(f'python {script_path} {bag_directory}', stdout=subprocess.PIPE, shell=True)

        # Tests that the script output is correct.
        # Tests if key information is in the string rather than the entire string
        # because bagit.py output includes the exact time of the error, so it is different every time the test is run.
        output = script_output.stdout.decode('utf-8')
        result = [f'Bag invalid:  {os.path.join(bag_directory, "aip_1_bag")}' in output,
                  'Payload-Oxum validation failed. Expected 1 files and 19 bytes but found 1 files and 28 bytes' in output,
                  f'Bag invalid:  {os.path.join(bag_directory, "aip_2_bag")}' in output,
                  'Payload-Oxum validation failed. Expected 2 files and 51 bytes but found 1 files and 26 bytes' in output]
        expected = [True, True, True, True]
        self.assertEqual(result, expected, "Problem with test for all invalid")

    def test_all_valid(self):
        """Test for when there are multiple bags in the directory, all valid."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_directory = os.path.join('test_validate_bags', 'all_valid')
        script_output = subprocess.run(f'python {script_path} {bag_directory}', stdout=subprocess.PIPE, shell=True)

        # Tests that the script output is correct.
        expected_output = f'\r\nBag valid:  {os.path.join(bag_directory, "aip_1_bag")}\r\n\r\n' \
                          f'Bag valid:  {bag_directory}\\aip_2_bag\r\n'
        self.assertEqual(script_output.stdout.decode('utf-8'), expected_output, "Problem with test for all valid")

    def test_mix(self):
        """Test for when there are multiple things in the directory: valid bag, invalid bag, and not a bag."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_directory = os.path.join('test_validate_bags', 'mix')
        script_output = subprocess.run(f'python {script_path} {bag_directory}', stdout=subprocess.PIPE, shell=True)

        # Tests that the script output is correct.
        # Tests if key information is in the string rather than the entire string
        # because bagit.py output includes the exact time of the error, so it is different every time the test is run.
        output = script_output.stdout.decode('utf-8')
        result = [f'Bag valid:  {os.path.join(bag_directory, "aip_1_bag")}' in output,
                  f'Bag invalid:  {os.path.join(bag_directory, "aip_2_bag")}' in output,
                  'Payload-Oxum validation failed. Expected 2 files and 51 bytes but found 1 files and 25 bytes' in output]
        expected = [True, True, True]
        self.assertEqual(result, expected, "Problem with test for mix")

    def test_one(self):
        """Test for when there is only one bag in the directory, which is valid."""
        # Runs the script.
        script_path = os.path.join('..', 'validate_bags.py')
        bag_directory = os.path.join('test_validate_bags', 'one')
        script_output = subprocess.run(f'python {script_path} {bag_directory}', stdout=subprocess.PIPE, shell=True)

        # Tests that the script output is correct.
        expected_output = f'\r\nBag valid:  {os.path.join(bag_directory, "aip_1_bag")}\r\n'
        self.assertEqual(script_output.stdout.decode('utf-8'), expected_output, "Problem with test for all valid")


if __name__ == '__main__':
    unittest.main()
