"""Check all folders in the provided directory for any that are above 10,000 files

Run this script prior to converting a batch of folders into bags to check for any that might be too large.
We recommend, but do not require, a maximum of 10,000 files per bag for more time efficient validation.
Total size (recommended under 100 GB) is not checked because that takes longer to calculate.

This is a companion to check_bag_size.py, which checks file count and total size in GB using the bag metadata.

Parameter:
    bag_directory (required): path to the directory that contains the folders to bag

Returns:
    file_count_check.csv in the bag_directory with the folder names, number of files, and if they are over the maximum
"""
import os
import sys
from shared_functions import log


if __name__ == '__main__':

    # Maximum number of files desired. Update this number for other use cases.
    MAX_FILES = 10000

    # Parent folder of the folders to be bagged.
    bag_dir = sys.argv[1]

    # Start a log with a header for the results.
    log_path = os.path.join(bag_dir, 'file_count_check.csv')
    log(log_path, ['Folder', 'Files', 'Files_OK'])

    for folder_name in os.listdir(bag_dir):

        # Skips any metadata files. All folders should be checked.
        if os.path.isfile(os.path.join(bag_dir, folder_name)):
            continue

        # Gets the number of files at all levels within the current folder.
        file_count = 0
        for root, dirs, files in os.walk(os.path.join(bag_dir, folder_name)):
           file_count += len(files)

        # Saves file count information for the current folder to the log,
        # including comparing it to the desired maximum.
        log(log_path, [folder_name, file_count, file_count < MAX_FILES])
