"""
Tests for the script bag_manifest_compare_files.py, which makes a report of files only in the manifest or data folder.
"""
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one line per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the manifest compare report, if it was made"""
        bags = ['add_bag', 'both_bag', 'delete_bag']
        for bag in bags:
            report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', f'{bag}_manifest_compare_report.csv')
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_add(self):
        """Test for when files were added since the bag was made"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'bag_manifest_compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', 'add_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', 'add_bag_manifest_compare_report.csv')
        result = csv_to_list(report_path)
        expected = [['paths', 'path_location'],
                    ['data/0.txt', 'data'],
                    ['data/6.txt', 'data'],
                    ['data/7.txt', 'data']]
        self.assertEqual(result, expected, "Problem with test for add")

    def test_both(self):
        """Test for when files were added and other files deleted since the bag was made"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'bag_manifest_compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', 'both_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', 'both_bag_manifest_compare_report.csv')
        result = csv_to_list(report_path)
        expected = [['paths', 'path_location'],
                    ['data/0.txt', 'data'],
                    ['data/1.txt', 'manifest'],
                    ['data/2.txt', 'manifest'],
                    ['data/5.txt', 'manifest'],
                    ['data/6.txt', 'data']]
        self.assertEqual(result, expected, "Problem with test for both")

    def test_delete(self):
        """Test for when files were deleted since the bag was made"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'bag_manifest_compare_files.py')
        bag_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', 'delete_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_files', 'delete_bag_manifest_compare_report.csv')
        result = csv_to_list(report_path)
        expected = [['paths', 'path_location'],
                    ['data/1.txt', 'manifest'],
                    ['data/3.txt', 'manifest'],
                    ['data/4.txt', 'manifest'],
                    ['data/5.txt', 'manifest']]
        self.assertEqual(result, expected, "Problem with test for delete")


if __name__ == '__main__':
    unittest.main()
