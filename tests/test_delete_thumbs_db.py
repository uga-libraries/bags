import os
import shutil
import subprocess
import unittest
from test_functions import csv_to_list, make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copy of test data and log, if made"""
        test_dir = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir')
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

        log_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'bag_validation_log.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_batch(self):
        """Test for removing Thumbs.db from multiple bags at the same time"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'batch'),
                        os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'batch_list.txt')
        subprocess.run(f'python {script_path} {bag_list}', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'aip1_bag'),
                    os.path.join(test_dir, 'aip1_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'aip1_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'aip1_bag', 'data'),
                    os.path.join(test_dir, 'aip1_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'aip1_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'aip1_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'aip2_bag'),
                    os.path.join(test_dir, 'aip2_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'aip2_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'aip2_bag', 'data'),
                    os.path.join(test_dir, 'aip2_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'aip2_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'aip2_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'aip2_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'aip2_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'aip3_bag'),
                    os.path.join(test_dir, 'aip3_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'aip3_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'aip3_bag', 'data'),
                    os.path.join(test_dir, 'aip3_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'aip3_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'aip3_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for batch, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Valid?', 'Notes'],
                    [os.path.join(test_dir, 'aip1_bag'), 'True', 'BLANK'],
                    [os.path.join(test_dir, 'aip2_bag'), 'True', 'BLANK'],
                    [os.path.join(test_dir, 'aip3_bag'), 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for batch, log")

    def test_manifest(self):
        """Test for when 1 Thumbs.db file is in the bag manifest"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'manifest_bag'), 
                        os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_bag'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_bag')
        printed = subprocess.run(f'python {script_path} {bag_path}', shell=True, capture_output=True, text=True)

        # Test for the directory contents.
        result = make_directory_list(bag_path)
        expected = [os.path.join(bag_path, 'bag-info.txt'),
                    os.path.join(bag_path, 'bagit.txt'),
                    os.path.join(bag_path, 'data'),
                    os.path.join(bag_path, 'data', 'Document.txt'),
                    os.path.join(bag_path, 'manifest-md5.txt'),
                    os.path.join(bag_path, 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for manifest, directory")

        # Test for the printed information.
        result = printed.stdout
        expected = '\nBag is valid\n'
        self.assertEqual(expected, result, "Problem with test for manifest, printed text")

    def test_not_manifest(self):
        """Test for when 2 Thumbs.db files are in the bag but not the manifest"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'not_manifest_bag'),
                        os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_bag'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_bag')
        printed = subprocess.run(f'python {script_path} {bag_path}', shell=True, capture_output=True, text=True)

        # Test for the directory contents.
        result = make_directory_list(bag_path)
        expected = [os.path.join(bag_path, 'bag-info.txt'),
                    os.path.join(bag_path, 'bagit.txt'),
                    os.path.join(bag_path, 'data'),
                    os.path.join(bag_path, 'data', 'Document.txt'),
                    os.path.join(bag_path, 'data', 'Folder'),
                    os.path.join(bag_path, 'data', 'Folder', 'Document.txt'),
                    os.path.join(bag_path, 'manifest-md5.txt'),
                    os.path.join(bag_path, 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for not_manifest, directory")

        # Test for the printed information.
        result = printed.stdout
        expected = '\nBag is valid\n'
        self.assertEqual(expected, result, "Problem with test for not_manifest, printed text")


if __name__ == '__main__':
    unittest.main()
