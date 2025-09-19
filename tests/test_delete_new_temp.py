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
        bags = ['test_extra_not_temp_bag', 'test_extra_temp_bag', 'test_no_extra_bag']
        for bag in bags:
            if os.path.exists(os.path.join(os.getcwd(), bag)):
                shutil.rmtree(os.path.join(os.getcwd(), bag))

    def test_extra_not_temp(self):
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'extra_not_temp_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_extra_not_temp_bag')
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
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'extra_temp_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_extra_temp_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for extra_temp, directory")

        # Test for the printed information.
        expected = "\nBag is valid\n"
        self.assertEqual(expected, printed.stdout, "Problem with test for extra_temp, printed")

    def test_no_extra(self):
        # Make a copy of the test data, since the script deletes files.
        script_path = os.path.join('', '..', 'delete_new_temp.py')
        bag_path = os.path.join(os.getcwd(), 'no_extra_bag')
        new_bag_path = os.path.join(os.getcwd(), 'test_no_extra_bag')
        shutil.copytree(bag_path, new_bag_path)
        printed = subprocess.run(f'python {script_path} {new_bag_path}', capture_output=True, text=True, shell=True)

        # Test for the directory contents.
        result = make_directory_list(new_bag_path)
        expected = ['data\\Document.txt', 'data\\Folder\\Document.txt']
        self.assertEqual(expected, result, "Problem with test for no_extra, directory")

        # Test for the printed information.
        expected = "\nBag is valid\n"
        self.assertEqual(expected, printed.stdout, "Problem with test for no_extra, printed")


if __name__ == '__main__':
    unittest.main()
