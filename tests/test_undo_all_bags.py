"""Test for the script undo_all_bags.py"""
import os
import shutil
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete test files."""
        shutil.rmtree('test_undo_copy')

    def test_script(self):
        """Test for correct operation of the undo_all_bags.py script."""

        # Makes a copy of the test files in the repo, since the test alters the files.
        shutil.copytree('test_undo_bags', 'test_undo_copy')

        # Runs the script.
        script_path = os.path.join('..', 'undo_all_bags.py')
        subprocess.run(f'python {script_path} test_undo_copy', shell=True)

        # Tests that the names of the folders are correct.
        folder_names = []
        for name in os.listdir('test_undo_copy'):
            folder_names.append(name)
        folder_names_expected = ['aip_1', 'aip_2']
        self.assertEqual(folder_names, folder_names_expected, "Problem with test for folder names")

        # Tests that the contents of the folders are correct.
        folder_contents = []
        for root, dirs, files in os.walk('test_undo_copy'):
            for file in files:
                folder_contents.append(os.path.join(root, file))
        folder_contents_expected = [os.path.join('test_undo_copy', 'aip_1', 'Test File.txt'),
                                    os.path.join('test_undo_copy', 'aip_2', 'File_One.txt'),
                                    os.path.join('test_undo_copy', 'aip_2', 'File_Two.txt')]
        self.assertEqual(folder_contents, folder_contents_expected, "Problem with test for folder contents")


if __name__ == '__main__':
    unittest.main()
