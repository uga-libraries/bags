import os
import shutil
import subprocess
import unittest
from test_functions import make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copy of test data, if made"""
        bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_bag')
        if os.path.exists(bag_path):
            shutil.rmtree(bag_path)

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
