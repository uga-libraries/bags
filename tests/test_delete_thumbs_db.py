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

    def test_one(self):
        """Test for removing Thumbs.db from one bag"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'one'),
                        os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'one_list.txt')
        subprocess.run(f'python {script_path} {bag_list}', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'ER001_bag'),
                    os.path.join(test_dir, 'ER001_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'ER001_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'ER001_bag', 'data'),
                    os.path.join(test_dir, 'ER001_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'ER001_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'ER001_bag', 'data', 'Folder2'),
                    os.path.join(test_dir, 'ER001_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'ER001_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'ER001_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for one, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Valid?', 'Notes'],
                    [os.path.join(test_dir, 'ER001_bag'), 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for one, log")


if __name__ == '__main__':
    unittest.main()
