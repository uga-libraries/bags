"""
Tests for the script compare_files.py, which makes a report of files only in the manifest or data folder.
"""
import os
import subprocess
import unittest
from test_functions import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the manifest compare report, if it was made"""
        report_path = os.path.join(os.getcwd(), 'test_compare_files', 'compare_files_report.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_add(self):
        """Test for when files were added since the bag was made"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_files', 'add_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_compare_files', 'compare_files_report.csv')
        result = csv_to_list(report_path)
        expected = [['Path', 'Source'],
                    ['data/0.txt', 'Data Folder'],
                    ['data/6.txt', 'Data Folder'],
                    ['data/7.txt', 'Data Folder']]
        self.assertEqual(expected, result, "Problem with test for add")

    def test_both(self):
        """Test for when files were added and other files deleted since the bag was made"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_files', 'both_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_compare_files', 'compare_files_report.csv')
        result = csv_to_list(report_path)
        expected = [['Path', 'Source'],
                    ['data/0.txt', 'Data Folder'],
                    ['data/1.txt', 'Manifest'],
                    ['data/2.txt', 'Manifest'],
                    ['data/5.txt', 'Manifest'],
                    ['data/6.txt', 'Data Folder']]
        self.assertEqual(expected, result, "Problem with test for both")

    def test_delete(self):
        """Test for when files were deleted since the bag was made"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_files', 'delete_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_compare_files', 'compare_files_report.csv')
        result = csv_to_list(report_path)
        expected = [['Path', 'Source'],
                    ['data/1.txt', 'Manifest'],
                    ['data/3.txt', 'Manifest'],
                    ['data/4.txt', 'Manifest'],
                    ['data/5.txt', 'Manifest']]
        self.assertEqual(expected, result, "Problem with test for delete")

    def test_match(self):
        """Test for when the files in the bag manifest and data folder match"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_files', 'match_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_compare_files', 'compare_files_report.csv')
        result = csv_to_list(report_path)
        expected = [['No differences between the files in the manifest and the data folder. '
                     'Check fixity to see if the bag is valid.']]
        self.assertEqual(expected, result, "Problem with test for match")


if __name__ == '__main__':
    unittest.main()
