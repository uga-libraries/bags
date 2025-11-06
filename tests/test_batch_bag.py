import os
import shutil
import subprocess
import unittest


def make_directory_list(path):
    """Makes a list of all the folders in the bag_dir"""
    dir_list = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_list.append(dir_name)
    return dir_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete copy of test data (bagged or not), if made"""
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        if os.path.exists(bag_dir):
            shutil.rmtree(bag_dir)

    def test_bag_all(self):
        """Test for when all folders should be bagged"""
        # Make a copy of the test data (script edits files).
        shutil.copytree(os.path.join(os.getcwd(), 'test_batch_bag', 'bag_all'),
                        os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir'))

        # Make variables and run the script.
        script_path = os.path.join('..', 'batch_bag.py')
        bag_dir = os.path.join(os.getcwd(), 'test_batch_bag', 'bag_dir')
        subprocess.run(f'python {script_path} {bag_dir}', shell=True)

        # Test for the directory contents.
        result = make_directory_list(bag_dir)
        expected = ['aip1_bag', 'aip2_bag', 'data', 'data', 'aip2_subfolder']
        self.assertEqual(expected, result, "Problem with test for bag_all, directory")


if __name__ == '__main__':
    unittest.main()
