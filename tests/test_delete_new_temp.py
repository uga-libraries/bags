import os
import re
import shutil
import subprocess
import unittest


def make_directory_list(path):
    """Makes a list of the full paths of all files remaining in the bag data folder after deletion"""
    dir_list = []
    for root, dirs, files in os.walk(os.path.join(path, 'data')):
        for file in files:
            root_from_data = re.search(rf"{'data'}.*", root).group()
            dir_list.append(os.path.join(root_from_data, file))
    return dir_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copies of test data, if made"""
        bags = ['test_extra_not_temp_bag', 'test_extra_temp_bag', 'test_extra_temp_with_spaces_bag',
                'test_not_valid_bag', 'test_temp_not_all_extra_bag']
        for bag in bags:
            bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', bag)
            if os.path.exists(bag_path):
                shutil.rmtree(bag_path)

    def test_extra_not_temp(self):
        """Test for when files were added after bagging, but they are not temp files and are not deleted"""
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_not_temp_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_extra_not_temp_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Extra.txt', 'data\\Folder\\Document.txt', 'data\\Folder\\Extra2.txt']
        self.assertEqual(expected, result, "Problem with test for extra_not_temp, directory")

        # Test for the printed information.
        expected = ("\nAfter deleting temp files, there are still files in the data folder that are not in the manifest:\n"
                    "\t* data/Extra.txt\n\t* data/Folder/Extra2.txt\n")
        self.assertEqual(expected, printed.stdout, "Problem with test for extra_not_temp, printed")

    def test_extra_temp(self):
        """Test for when files were added after bagging, all are temp files that will be deleted,
        and the bag will be valid after the deletion"""
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_extra_temp_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for extra_temp, directory")

        # Test for the printed information.
        expected = (f"Deleting {new_bag_path}/data/.Document.txt\n"
                    f"Deleting {new_bag_path}/data/Document.tmp\n"
                    f"Deleting {new_bag_path}/data/Folder/Thumbs.db\n"
                    f"\nBag is valid\n")
        self.assertEqual(expected, printed.stdout, "Problem with test for extra_temp, printed")

    def test_extra_temp_with_spaces(self):
        """Test for when files were added after bagging, all are temp files that will be deleted,
        there are folders and files with double spaces (impacts manifest parsing),
        and the bag will be valid after the deletion"""
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'extra_temp_with_spaces_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_extra_temp_with_spaces_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder  Title\\New  Document.txt']
        self.assertEqual(expected, result, "Problem with test for extra_temp_with_spaces, directory")

        # Test for the printed information.
        expected = (f"Deleting {new_bag_path}/data/Document  Temp.tmp\n"
                    f"Deleting {new_bag_path}/data/Folder  Title/Document.tmp\n"
                    f"\nBag is valid\n")
        self.assertEqual(expected, printed.stdout, "Problem with test for extra_temp_with_spaces, printed")

    def test_not_valid(self):
        """Test for a bag with no extra files but that is not valid from the start"""
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'not_valid_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_not_valid_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for not_valid, directory")

        # Test for the printed information.
        expected = ('\nBag is not valid\nBag validation failed: data\Document.txt md5 validation failed: '
                    'expected="4xx51d0000698119300eb0c54dbaxx89" found="4bb51d0461698119344eb0c54dbabb89"; '
                    'data\Folder\Document.txt md5 validation failed: expected="4xx51d0000698119300eb0c54dbaxx89" '
                    'found="4bb51d0461698119344eb0c54dbabb89"\n')
        self.assertEqual(expected, printed.stdout, "Problem with test for not_valid, printed")

    def test_temp_not_all_extra(self):
        """Test for a bag with some temp files that are in the manifest and should not be deleted
        and a temp file added after bagging that should be deleted, after which the bag will validate"""
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'temp_not_all_extra_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_delete_new_temp', 'test_temp_not_all_extra_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\.Document.txt', 'data\\Document.tmp', 'data\\Document.txt',
                    'data\\Folder\\Document.txt', 'data\\Folder\Thumbs.db']
        self.assertEqual(expected, result, "Problem with test for temp_not_all_extra, directory")

        # Test for the printed information.
        expected = (f"Deleting {new_bag_path}/data/Folder/.Document.txt\n"
                    f"\nBag is valid\n")
        self.assertEqual(expected, printed.stdout, "Problem with test for temp_not_all_extra, printed")


if __name__ == '__main__':
    unittest.main()
