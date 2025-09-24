"""Compares the fixity of files in a bag manifest to the data folder and creates a report of file differences,
which includes files that are only in the manifest, only in the data folder, or in both places with different fixity.

Use this script after a bag validation error that indicates the size has changed.
Use bag_manifest_compare_files.py instead when the error is a different number of files, which is faster.

This script is modeled after the function validate_bag_manifest() in validate_fixity.py in the hub-monitoring repo.

Parameters:
    bag_path (required): path to the bag folder

Returns:
    BAGNAME_manifest_compare_report.csv (saved to the parent folder of the bag
"""
import hashlib
import os
import pandas as pd
import sys


if __name__ == '__main__':

    # Get bag_path from script argument.
    bag_path = sys.argv[1]

    # Create a dataframe with the file path and md5 for every file in the data folder.

    # Read the bag md5 manifest to a dataframe.

    # Compare the bag and manifest dataframes.

    # Make a log of the differences.

    # Print a summary of the result.