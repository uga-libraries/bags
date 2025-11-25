"""
Tests for the script compare_fixity.py, which makes a report of fixity differences.
"""
import os
import shutil
import subprocess
import unittest
from test_functions import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the manifest compare report and data_md5.csv, if it was made"""
        filenames = ['compare_fixity_report.csv', 'data_md5.csv']
        for filename in filenames:
            file_path = os.path.join(os.getcwd(), 'test_compare_fixity', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_added(self):
        """Test for a bag with 3 files added after bagging"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_fixity', 'added_bag')
        output_path = os.path.join(os.getcwd(), 'test_compare_fixity')
        subprocess.run(f'python {script_path} {bag_path} {output_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(output_path, 'compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['89c60670864545fbc6b508503ef67ccb', 'data/File_1a.txt', 'Data Folder'],
                    ['3d6407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt', 'Data Folder'],
                    ['bb93fde70b35637aa1489695d38917ae', 'data/Folder/File_2b.txt', 'Data Folder']]
        self.assertEqual(expected, result, "Problem with test for added, compare report")

        # Tests the data_md5.csv has the correction information.
        report_path = os.path.join(output_path, 'data_md5.csv')
        result = csv_to_list(report_path)
        expected = [['a31ad967b49226c29700a71e20e91ad6', 'data/File_1.txt'],
                    ['89c60670864545fbc6b508503ef67ccb', 'data/File_1a.txt'],
                    ['1864a668ff2218ba2b23c576347b9386', 'data/Folder/File_2.txt'],
                    ['3d6407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt'],
                    ['bb93fde70b35637aa1489695d38917ae', 'data/Folder/File_2b.txt']]
        self.assertEqual(expected, result, "Problem with test for added, data md5")

    def test_deleted(self):
        """Test for a bag with 1 file deleted after bagging"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_fixity', 'deleted_bag')
        output_path = os.path.join(os.getcwd(), 'test_compare_fixity')
        subprocess.run(f'python {script_path} {bag_path} {output_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(output_path, 'compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['893c9bca3cf9d6c9af9828f06c3eeb78', 'data/File_1.txt', 'Manifest']]
        self.assertEqual(expected, result, "Problem with test for deleted, compare report")

        # Tests the data_md5.csv has the correction information.
        report_path = os.path.join(output_path, 'data_md5.csv')
        result = csv_to_list(report_path)
        expected = [['2486ea837419dc36af7f6dd9e2e0f96c', 'data/File_2.txt']]
        self.assertEqual(expected, result, "Problem with test for deleted, data md5")

    def test_edited(self):
        """Test for a bag where 2/3 files have been edited, but no files added or deleted"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_fixity', 'edited_bag')
        output_path = os.path.join(os.getcwd(), 'test_compare_fixity')
        subprocess.run(f'python {script_path} {bag_path} {output_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(output_path, 'compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['a31ad967b49226c29700a71e20e91ad6', 'data/File_1.txt', 'Data Folder'],
                    ['47ae221bd3711ce37e4487bfec08a3ee', 'data/File_1.txt', 'Manifest'],
                    ['dbed2c145ec5a3ef5877753abefdabf6', 'data/File_2.txt', 'Data Folder'],
                    ['673711fb4102a49ee1700eaccc4efe10', 'data/File_2.txt', 'Manifest']]
        self.assertEqual(expected, result, "Problem with test for edited, compare report")

        # Tests the data_md5.csv has the correction information.
        report_path = os.path.join(output_path, 'data_md5.csv')
        result = csv_to_list(report_path)
        expected = [['a31ad967b49226c29700a71e20e91ad6', 'data/File_1.txt'],
                    ['dbed2c145ec5a3ef5877753abefdabf6', 'data/File_2.txt'],
                    ['7f52bb6641d0d471856d704f670356e9', 'data/File_3.txt']]
        self.assertEqual(expected, result, "Problem with test for edited, data md5")

    def test_restart(self):
        """Test for a bag that already has data_md5.csv started"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_fixity', 'restart_dir', 'restart_bag')
        output_path = os.path.join(os.getcwd(), 'test_compare_fixity')
        shutil.copy(os.path.join(os.getcwd(), 'test_compare_fixity', 'restart_dir', 'data_md5_copy.csv'),
                    os.path.join(output_path, 'data_md5.csv'))
        subprocess.run(f'python {script_path} {bag_path} {output_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(output_path, 'compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['MD5', 'Path', 'Source'],
                    ['0000x668xx2218xx2b23x576347x9386', 'data/Folder/File_2.txt', 'Data Folder'],
                    ['1864a668ff2218ba2b23c576347b9386', 'data/Folder/File_2.txt', 'Manifest'],
                    ['3d6407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt', 'Data Folder'],
                    ['0x0407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt', 'Manifest']]
        self.assertEqual(expected, result, "Problem with test for restart, compare report")

        # Tests the data_md5.csv has the correction information.
        report_path = os.path.join(output_path, 'data_md5.csv')
        result = csv_to_list(report_path)
        expected = [['a31ad967b49226c29700a71e20e91ad6', 'data/File_1.txt'],
                    ['0000x668xx2218xx2b23x576347x9386', 'data/Folder/File_2.txt'],
                    ['89c60670864545fbc6b508503ef67ccb', 'data/File_1a.txt'],
                    ['3d6407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt'],
                    ['bb93fde70b35637aa1489695d38917ae', 'data/Folder/File_2b.txt']]
        self.assertEqual(expected, result, "Problem with test for restart, data md5")

    def test_valid(self):
        """Test for a bag that is valid (no fixity differences)"""

        # Makes variables needed and runs the script.
        script_path = os.path.join('..', 'compare_fixity.py')
        bag_path = os.path.join(os.getcwd(), 'test_compare_fixity', 'valid_bag')
        output_path = os.path.join(os.getcwd(), 'test_compare_fixity')
        subprocess.run(f'python {script_path} {bag_path} {output_path}')

        # Tests the manifest compare report has the correct information.
        report_path = os.path.join(output_path, 'compare_fixity_report.csv')
        result = csv_to_list(report_path)
        expected = [['The bag is valid. No differences between the manifest and the data folder contents.']]
        self.assertEqual(expected, result, "Problem with test for valid, compare report")

        # Tests the data_md5.csv has the correction information.
        report_path = os.path.join(output_path, 'data_md5.csv')
        result = csv_to_list(report_path)
        expected = [['a31ad967b49226c29700a71e20e91ad6', 'data/File_1.txt'],
                    ['89c60670864545fbc6b508503ef67ccb', 'data/File_1a.txt'],
                    ['1864a668ff2218ba2b23c576347b9386', 'data/Folder/File_2.txt'],
                    ['3d6407ca6b6c62b25f5e090918d8549e', 'data/Folder/File_2a.txt'],
                    ['bb93fde70b35637aa1489695d38917ae', 'data/Folder/File_2b.txt']]
        self.assertEqual(expected, result, "Problem with test for valid, data md5")


if __name__ == '__main__':
    unittest.main()
