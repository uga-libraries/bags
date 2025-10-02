import os
import shutil
import subprocess
import unittest
from test_delete_new_temp import make_directory_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copies of test data, if made"""
        bags = ['test_manifest_bag', 'test_not_manifest_bag']
        for bag in bags:
            bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', bag)
            if os.path.exists(bag_path):
                shutil.rmtree(bag_path)

    def test_manifest(self):
        """Test for when 1 Thumbs.db file is in the bag manifest"""
        # Make variables and copy of the test data (script deletes files) and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'manifest_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_manifest_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for manifest, directory")

        # Test for the printed information.
        expected = '\nBag is valid\n'
        self.assertEqual(expected, printed.stdout, "Problem with test for manifest, printed text")

    def test_not_manifest(self):
        """Test for when 2 Thumbs.db files are in the bag but not the manifest"""
        # Make variables and copy of the test data (script deletes files) and run the script.
        script_path = os.path.join('..', 'delete_thumbs_db.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'not_manifest_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_thumbs_db', 'test_not_manifest_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for not_manifest, directory")

        # Test for the printed information.
        expected = '\nBag is valid\n'
        self.assertEqual(expected, printed.stdout, "Problem with test for not_manifest, printed text")


if __name__ == '__main__':
    unittest.main()
