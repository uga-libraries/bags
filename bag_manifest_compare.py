"""Compares the files in a bag manifest to the files in the data folder
and creates a report of files in only one location

Use this script after a bag validation error that indicates a different number of expected files

Parameters:
    bag_path (required): path to the bag folder

Returns:
    BAGNAME_manifest_compare_report.csv
"""
import os
import pandas as pd
import sys


if __name__ == '__main__':

    bag_path = sys.argv[1]

    # Reads the bag manifest into a dataframe.
    manifest_df = pd.read_csv(os.path.join(bag_path, 'manifest-md5.txt'),
                              delimiter='  ', names=['md5', 'paths'], engine='python')

    # Makes a dataframe with the relative paths of files in the data folder, starting with data.

    # Compares the manifest to the files in the data folder.

    # Saves paths only in the manifest or only in the data folder to a csv in the parent directory of the bag.