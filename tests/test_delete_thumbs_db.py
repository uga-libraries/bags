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
        expected = [['Bag_Path', 'Thumbs_Deleted', 'Valid?', 'Notes'],
                    [os.path.join(test_dir, 'aip1_bag'), '1', 'True', 'BLANK'],
                    [os.path.join(test_dir, 'aip2_bag'), '2', 'True', 'BLANK'],
                    [os.path.join(test_dir, 'aip3_bag'), '1', 'True', 'BLANK']]
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
        expected = [['Bag_Path', 'Thumbs_Deleted', 'Valid?', 'Notes'],
                    [os.path.join(test_dir, 'ER001_bag'), '3', 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for one, log")

    def test_unusual(self):
        """Test for unusual things: bag_path doesn't exist, no Thumbs.db, and a blank row in the list"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'unusual'),
                        os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'unusual_list.txt')
        subprocess.run(f'python {script_path} {bag_list}', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'a1_bag'),
                    os.path.join(test_dir, 'a1_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'a1_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'a1_bag', 'data'),
                    os.path.join(test_dir, 'a1_bag', 'data', 'Text Document.txt'),
                    os.path.join(test_dir, 'a1_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'a1_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for unusual, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'bag_validation_log.csv'))
        expected = [['Bag_Path', 'Thumbs_Deleted', 'Valid?', 'Notes'],
                    [os.path.join(test_dir, 'a0_bag'), 'TBD', 'TBD', 'Bag path error'],
                    [os.path.join(test_dir, 'a1_bag'), '0', 'True', 'BLANK'],
                    ['BLANK', 'TBD', 'TBD', 'Bag path error']]
        self.assertEqual(expected, result, "Problem with test for unusual, log")


if __name__ == '__main__':
    unittest.main()
