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

    # def test_extra_not_temp_preview(self):
    #     """Test for when files were added after bagging, but they are not temp files, in preview mode"""
    #     # Make a copy of the test data (script edits files).
    #     shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_not_temp_bag'),
    #                     os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_bag'))
    #
    #     # Make variables and run the script.
    #     script_path = os.path.join('', '..', 'delete_new_temp.py')
    #     bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_bag')
    #     printed = subprocess.run(f'python {script_path} {bag_path} preview', shell=True, capture_output=True, text=True)
    #
    #     # Test for the directory contents.
    #     result = make_directory_list(bag_path)
    #     expected = [os.path.join(bag_path, 'bag-info.txt'),
    #                 os.path.join(bag_path, 'bagit.txt'),
    #                 os.path.join(bag_path, 'data'),
    #                 os.path.join(bag_path, 'data', 'Document.txt'),
    #                 os.path.join(bag_path, 'data', 'Extra.txt'),
    #                 os.path.join(bag_path, 'data', 'Folder'),
    #                 os.path.join(bag_path, 'data', 'Folder', 'Document.txt'),
    #                 os.path.join(bag_path, 'data', 'Folder', 'Extra2.txt'),
    #                 os.path.join(bag_path, 'manifest-md5.txt'),
    #                 os.path.join(bag_path, 'tagmanifest-md5.txt')]
    #     self.assertEqual(expected, result, "Problem with test for extra_not_temp_preview, directory")
    #
    #     # Test for the printed information.
    #     result = printed.stdout
    #     expected = ('\nRunning in script_mode "preview", which will print files that would be deleted but changes nothing.\n'
    #                 '\nPreview of files to delete is complete.\n'
    #                 'Files that would have been deleted are listed above.\n'
    #                 'There are 2 files that are not in the manifest and are not temp.\n'
    #                 '\t* data/Extra.txt\n'
    #                 '\t* data/Folder/Extra2.txt\n')
    #     self.assertEqual(expected, result, "Problem with test for extra_not_temp_preview, printed")

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
        self.assertEqual(expected, result, "Problem with test for extra_temp, log")

    # def test_extra_temp_preview(self):
    #     """Test for when files were added after bagging and the script is in preview mode,
    #     so they'll be printed but not deleted"""
    #     # Make a copy of the test data (script edits files).
    #     shutil.copytree(os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp_bag'),
    #                     os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_bag'))
    #
    #     # Make variables and run the script.
    #     script_path = os.path.join('', '..', 'delete_new_temp.py')
    #     bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_bag')
    #     printed = subprocess.run(f'python {script_path} {bag_path} preview', shell=True, capture_output=True, text=True)
    #
    #     # Test for the directory contents.
    #     result = make_directory_list(bag_path)
    #     expected = [os.path.join(bag_path, 'bag-info.txt'),
    #                 os.path.join(bag_path, 'bagit.txt'),
    #                 os.path.join(bag_path, 'data'),
    #                 os.path.join(bag_path, 'data', '.Document.txt'),
    #                 os.path.join(bag_path, 'data', 'Document.tmp'),
    #                 os.path.join(bag_path, 'data', 'Document.txt'),
    #                 os.path.join(bag_path, 'data', 'Folder'),
    #                 os.path.join(bag_path, 'data', 'Folder', 'Document.txt'),
    #                 os.path.join(bag_path, 'data', 'Folder', 'Thumbs.db'),
    #                 os.path.join(bag_path, 'manifest-md5.txt'),
    #                 os.path.join(bag_path, 'tagmanifest-md5.txt')]
    #     self.assertEqual(expected, result, "Problem with test for extra_temp_preview, directory")
    #
    #     # Test for the printed information.
    #     result = printed.stdout
    #     expected = ('\nRunning in script_mode "preview", which will print files that would be deleted but changes nothing.\n'
    #                 f'Delete {bag_path}/data/.Document.txt\n'
    #                 f'Delete {bag_path}/data/Document.tmp\n'
    #                 f'Delete {bag_path}/data/Folder/Thumbs.db\n'
    #                 '\nPreview of files to delete is complete.\n'
    #                 'Files that would have been deleted are listed above.\n'
    #                 'There are 0 files that are not in the manifest and are not temp.\n')
    #     self.assertEqual(expected, result, "Problem with test for extra_temp_preview, printed")

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
        self.assertEqual(expected, result, "Problem with test for temp_not_extra, directory")

        # Test for the log contents.
        result = csv_to_list(os.path.join(os.getcwd(), 'test_delete_new_temp', 'delete_new_temp_log.csv'))
        expected = [['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'],
                    [os.path.join(test_dir, 'coll-1-3_bag'), '0', 'BLANK', 'BLANK', 'True', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for temp_not_extra, log")


if __name__ == '__main__':
    unittest.main()
