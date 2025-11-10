"""
Tests for the script update_bag.py, which updates the manifest of a bag and validates the new bag.
"""
import os
import shutil
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the copies made for testing"""
        shutil.rmtree(os.path.join(os.getcwd(), 'test_update_bag', 'test_bag'))

    def test_addition(self):
        """Test for when a file has been added since a bag was made"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_update_bag', 'aip_addition_bag'),
                        os.path.join(os.getcwd(), 'test_update_bag', 'test_bag'))

        # Runs the script.
        script_path = os.path.join('..', 'update_bag.py')
        bag_path = os.path.join('test_update_bag', 'test_bag')
        printed = subprocess.run(f"python {script_path} {bag_path}", shell=True, capture_output=True, text=True)

        # Tests the bag was valid.
        result = printed.stdout
        expected = 'Bag is valid\n'
        self.assertEqual(expected, result, "Problem with test for addition")

    def test_deletion(self):
        """Test for when a file has been deleted since a bag was made"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_update_bag', 'aip_deletion_bag'),
                        os.path.join(os.getcwd(), 'test_update_bag', 'test_bag'))

        # Runs the script.
        script_path = os.path.join('..', 'update_bag.py')
        bag_path = os.path.join('test_update_bag', 'test_bag')
        printed = subprocess.run(f"python {script_path} {bag_path}", shell=True, capture_output=True, text=True)

        # Tests the bag was valid.
        result = printed.stdout
        expected = 'Bag is valid\n'
        self.assertEqual(expected, result, "Problem with test for deletion")

    def test_edit(self):
        """Test for when a file has been edited since a bag was made"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join(os.getcwd(), 'test_update_bag', 'aip_edit_bag'),
                        os.path.join(os.getcwd(), 'test_update_bag', 'test_bag'))

        # Runs the script.
        script_path = os.path.join('..', 'update_bag.py')
        bag_path = os.path.join('test_update_bag', 'test_bag')
        printed = subprocess.run(f"python {script_path} {bag_path}", shell=True, capture_output=True, text=True)

        # Tests the bag was valid.
        result = printed.stdout
        expected = 'Bag is valid\n'
        self.assertEqual(expected, result, "Problem with test for edit")


if __name__ == '__main__':
    unittest.main()
