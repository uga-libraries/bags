"""
Tests for the script bag_manifest_compare_fixity.py, which makes a report of fixity differences.
"""
import os
import subprocess
import unittest
from test_bag_manifest_compare_files import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the manifest compare report, if it was made"""
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'bag_manifest_compare_fixity_report.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_added(self):
        """Test for a bag with 3 files added after bagging"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'bag_manifest_compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'added_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'bag_manifest_compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['89c60670864545fbc6b508503ef67ccb', 'data/File_1a.txt', 'Data Folder'],
                    ['3d6407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt', 'Data Folder'],
                    ['bb93fde70b35637aa1489695d38917ae', 'data/Folder/File_2b.txt', 'Data Folder']]
        self.assertEqual(expected, result, "Problem with test for added")

    def test_deleted(self):
        """Test for a bag with 1 file deleted after bagging"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'bag_manifest_compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'deleted_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'bag_manifest_compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['893c9bca3cf9d6c9af9828f06c3eeb78', 'data/File_1.txt', 'Manifest']]
        self.assertEqual(expected, result, "Problem with test for deleted")

    def test_edited(self):
        """Test for a bag where 2/3 files have been edited, but no files added or deleted"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'bag_manifest_compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'edited_bag')
        subprocess.run(f'python {script_path} {bag_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(os.getcwd(), 'test_bag_manifest_compare_fixity', 'bag_manifest_compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['a31ad967b49226c29700a71e20e91ad6', 'data/File_1.txt', 'Data Folder'],
                    ['47ae221bd3711ce37e4487bfec08a3ee', 'data/File_1.txt', 'Manifest'],
                    ['dbed2c145ec5a3ef5877753abefdabf6', 'data/File_2.txt', 'Data Folder'],
                    ['673711fb4102a49ee1700eaccc4efe10', 'data/File_2.txt', 'Manifest']]
        self.assertEqual(expected, result, "Problem with test for edited")


if __name__ == '__main__':
    unittest.main()
