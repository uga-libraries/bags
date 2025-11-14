import os
import shutil
import subprocess
import unittest
from test_functions import csv_to_list, make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copy of test data and log, if made"""
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

        log_names = ['delete_new_temp_log.csv', 'preview_new_temp_log.csv']
        for log_name in log_names:
            log_path = os.path.join(os.getcwd(), 'test_delete_new_temp', log_name)
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_batch_delete(self):
        """Test for delete mode with multiple bags"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'batch'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'batch_list.txt')
        subprocess.run(f'python {script_path} {bag_list} delete', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'b01_bag'),
                    os.path.join(test_dir, 'b01_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b01_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b01_bag', 'data'),
                    os.path.join(test_dir, 'b01_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b01_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b01_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'b02_bag'),
                    os.path.join(test_dir, 'b02_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b02_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b02_bag', 'data'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Folder  Title'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Folder  Title', 'New  Document.txt'),
                    os.path.join(test_dir, 'b02_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b02_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'b03_bag'),
                    os.path.join(test_dir, 'b03_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b03_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b03_bag', 'data'),
                    os.path.join(test_dir, 'b03_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b03_bag', 'data', 'New Doc.txt'),
                    os.path.join(test_dir, 'b03_bag', 'data', 'New Doc2.txt'),
                    os.path.join(test_dir, 'b03_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b03_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'b04_bag'),
                    os.path.join(test_dir, 'b04_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b04_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b04_bag', 'data'),
                    os.path.join(test_dir, 'b04_bag', 'data', 'Document.tmp'),
                    os.path.join(test_dir, 'b04_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b04_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b04_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for batch_delete, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'delete_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'b01_bag'), '5',
                     'data/.Document.txt, data/.DS_Store, data/._.DS_Store, data/Document.tmp, data/Thumbs.db',
                     'BLANK', 'True', 'BLANK'],
                    [os.path.join(test_dir, 'b02_bag'), '2', 'data/Document  Temp.tmp, data/Folder  Title/Document.tmp',
                     'BLANK', 'True', 'BLANK'],
                    [os.path.join(test_dir, 'b03_bag'), '0', 'BLANK', 'data/New Doc.txt, data/New Doc2.txt',
                     'False', 'Non-temp files not in manifest'],
                    [os.path.join(test_dir, 'b04_bag'), '1', 'data/Thumbs.db', 'BLANK', 'False',
                     'Payload-Oxum validation failed. Expected 2 files and 138 bytes but found 2 files and 209 bytes']]
        self.assertEqual(expected, result, "Problem with test for batch_delete, log")

    def test_batch_preview(self):
        """Test for preview mode with multiple bags"""
        # Make a copy of the test data (in case there is an error with the script).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'batch'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'batch_list.txt')
        subprocess.run(f'python {script_path} {bag_list} preview', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'b01_bag'),
                    os.path.join(test_dir, 'b01_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b01_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b01_bag', 'data'),
                    os.path.join(test_dir, 'b01_bag', 'data', '.DS_Store'),
                    os.path.join(test_dir, 'b01_bag', 'data', '.Document.txt'),
                    os.path.join(test_dir, 'b01_bag', 'data', '._.DS_Store'),
                    os.path.join(test_dir, 'b01_bag', 'data', 'Document.tmp'),
                    os.path.join(test_dir, 'b01_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b01_bag', 'data', 'Thumbs.db'),
                    os.path.join(test_dir, 'b01_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b01_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'b02_bag'),
                    os.path.join(test_dir, 'b02_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b02_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b02_bag', 'data'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Document  Temp.tmp'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Folder  Title'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Folder  Title', 'Document.tmp'),
                    os.path.join(test_dir, 'b02_bag', 'data', 'Folder  Title', 'New  Document.txt'),
                    os.path.join(test_dir, 'b02_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b02_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'b03_bag'),
                    os.path.join(test_dir, 'b03_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b03_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b03_bag', 'data'),
                    os.path.join(test_dir, 'b03_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b03_bag', 'data', 'New Doc.txt'),
                    os.path.join(test_dir, 'b03_bag', 'data', 'New Doc2.txt'),
                    os.path.join(test_dir, 'b03_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b03_bag', 'tagmanifest-md5.txt'),
                    os.path.join(test_dir, 'b04_bag'),
                    os.path.join(test_dir, 'b04_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'b04_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'b04_bag', 'data'),
                    os.path.join(test_dir, 'b04_bag', 'data', 'Document.tmp'),
                    os.path.join(test_dir, 'b04_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'b04_bag', 'data', 'Thumbs.db'),
                    os.path.join(test_dir, 'b04_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'b04_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for batch_preview, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'preview_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'b01_bag'), '5',
                     'data/.Document.txt, data/.DS_Store, data/._.DS_Store, data/Document.tmp, data/Thumbs.db',
                     'BLANK', 'TBD', 'TBD'],
                    [os.path.join(test_dir, 'b02_bag'), '2', 'data/Document  Temp.tmp, data/Folder  Title/Document.tmp',
                     'BLANK', 'TBD', 'TBD'],
                    [os.path.join(test_dir, 'b03_bag'), '0', 'BLANK', 'data/New Doc.txt, data/New Doc2.txt',
                     'TBD', 'TBD'],
                    [os.path.join(test_dir, 'b04_bag'), '1', 'data/Thumbs.db', 'BLANK', 'TBD', 'TBD']]
        self.assertEqual(expected, result, "Problem with test for batch_preview, log")

    def test_extra_not_temp_delete(self):
        """Test for delete mode with non-temp files added after bagging that should not be deleted"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_not_temp'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))
        
        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_not_temp_list.txt')
        subprocess.run(f'python {script_path} {bag_list} delete', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'coll-1-1_bag'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Extra.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Folder', 'Extra2.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for extra_not_temp_delete, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'delete_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-1_bag'), '0', 'BLANK', 'data/Extra.txt, data/Folder/Extra2.txt',
                    'False', 'Non-temp files not in manifest']]
        self.assertEqual(expected, result, "Problem with test for extra_not_temp_delete, log")

    def test_extra_not_temp_preview(self):
        """Test for preview mode with non-temp files added after bagging that should not be deleted"""
        # Make a copy of the test data (in case there is an error with the script).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_not_temp'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_not_temp_list.txt')
        subprocess.run(f'python {script_path} {bag_list} preview', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'coll-1-1_bag'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Extra.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'data', 'Folder', 'Extra2.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'coll-1-1_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for extra_not_temp_preview, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'preview_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-1_bag'), '0', 'BLANK', 'data/Extra.txt, data/Folder/Extra2.txt',
                     'TBD', 'TBD']]
        self.assertEqual(expected, result, "Problem with test for extra_not_temp_preview, log")

    def test_extra_temp_delete(self):
        """Test for delete mode with temp files added after bagging that should be deleted"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp_list.txt')
        subprocess.run(f'python {script_path} {bag_list} delete', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'coll-1-2_bag'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for extra_temp_delete, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'delete_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-2_bag'), '3',
                     'data/.Document.txt, data/Document.tmp, data/Folder/Thumbs.db', 'BLANK', 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for extra_temp_delete, log")

    def test_extra_temp_preview(self):
        """Test for preview mode with temp files added after bagging that should be deleted"""
        # Make a copy of the test data (in case there is an error with the script).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp_list.txt')
        subprocess.run(f'python {script_path} {bag_list} preview', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'coll-1-2_bag'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', '.Document.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Document.tmp'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'data', 'Folder', 'Thumbs.db'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'coll-1-2_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for extra_temp_preview, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'preview_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-2_bag'), '3',
                     'data/.Document.txt, data/Document.tmp, data/Folder/Thumbs.db', 'BLANK', 'TBD', 'TBD']]
        self.assertEqual(expected, result, "Problem with test for extra_temp_preview, log")

    def test_path_error(self):
        """Test for when the path in the bag list is not correct"""
        # Make variables and run the script.
        # This uses the list for a different test.
        # Since the test data isn't first copied to test_dir, the paths are all incorrect.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'batch_list.txt')
        subprocess.run(f'python {script_path} {bag_list} preview', shell=True)

        # Test for the log contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'preview_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'b01_bag'), 'TBD', 'TBD', 'TBD', 'TBD', 'Bag path error'],
                    [os.path.join(test_dir, 'b02_bag'), 'TBD', 'TBD', 'TBD', 'TBD', 'Bag path error'],
                    [os.path.join(test_dir, 'b03_bag'), 'TBD', 'TBD', 'TBD', 'TBD', 'Bag path error'],
                    [os.path.join(test_dir, 'b04_bag'), 'TBD', 'TBD', 'TBD', 'TBD', 'Bag path error']]
        self.assertEqual(expected, result, "Problem with test for path_error, log")

    def test_temp_not_extra_delete(self):
        """Test for delete mode with temp files added before bagging that should not be deleted"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'temp_not_extra'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'temp_not_extra_list.txt')
        subprocess.run(f'python {script_path} {bag_list} delete', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'coll-1-3_bag'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', '.Document.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Document.tmp'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Folder', 'Thumbs.db'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for temp_not_extra_delete, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'delete_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-3_bag'), '0', 'BLANK', 'BLANK', 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for temp_not_extra_delete, log")

    def test_temp_not_extra_preview(self):
        """Test for preview mode with temp files added before bagging that should not be deleted"""
        # Make a copy of the test data (in case there is an error with the script).
        shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'temp_not_extra'),
                        os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'delete_new_temp.py')
        bag_list = os.path.join(os.getcwd(), 'test_delete_new_temp', 'temp_not_extra_list.txt')
        subprocess.run(f'python {script_path} {bag_list} preview', shell=True)

        # Test for the directory contents.
        test_dir = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_dir')
        result = make_directory_list(test_dir)
        expected = [os.path.join(test_dir, 'coll-1-3_bag'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'bag-info.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'bagit.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', '.Document.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Document.tmp'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Folder'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Folder', 'Document.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'data', 'Folder', 'Thumbs.db'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'manifest-md5.txt'),
                    os.path.join(test_dir, 'coll-1-3_bag', 'tagmanifest-md5.txt')]
        self.assertEqual(expected, result, "Problem with test for temp_not_extra_preview, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'preview_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-3_bag'), '0', 'BLANK', 'BLANK', 'TBD', 'TBD']]
        self.assertEqual(expected, result, "Problem with test for temp_not_extra_preview, log")


if __name__ == '__main__':
    unittest.main()
