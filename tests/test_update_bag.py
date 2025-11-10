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
        shutil.rmtree(os.path.join('test_update_bag', 'aip_bag'))

    def test_addition(self):
        """Test for when a file has been added since a bag was made"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join('test_update_bag', 'aip_addition_bag'), os.path.join('test_update_bag', 'aip_bag'))

        # Runs the script.
        script_path = os.path.join('..', 'update_bag.py')
        printed = subprocess.run(f"python {script_path} {os.path.join('test_update_bag', 'aip_bag')}",
                                 shell=True, capture_output=True, text=True)

        # Tests the bag was valid.
        result = printed.stdout
        expected = 'Bag is valid\n'
        self.assertEqual(result, expected, "Problem with test for addition")

    def test_deletion(self):
        """Test for when a file has been deleted since a bag was made"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join('test_update_bag', 'aip_deletion_bag'), os.path.join('test_update_bag', 'aip_bag'))

        # Runs the script.
        script_path = os.path.join('..', 'update_bag.py')
        printed = subprocess.run(f"python {script_path} {os.path.join('test_update_bag', 'aip_bag')}",
                                 shell=True, capture_output=True, text=True)

        # Tests the bag was valid.
        result = printed.stdout
        expected = 'Bag is valid\n'
        self.assertEqual(result, expected, "Problem with test for deletion")

    def test_edit(self):
        """Test for when a file has been edited since a bag was made"""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree(os.path.join('test_update_bag', 'aip_edit_bag'), os.path.join('test_update_bag', 'aip_bag'))

        # Runs the script.
        script_path = os.path.join('..', 'update_bag.py')
        printed = subprocess.run(f"python {script_path} {os.path.join('test_update_bag', 'aip_bag')}",
                                 shell=True, capture_output=True, text=True)

        # Tests the bag was valid.
        result = printed.stdout
        expected = 'Bag is valid\n'
        self.assertEqual(result, expected, "Problem with test for edit")


if __name__ == '__main__':
    unittest.main()
