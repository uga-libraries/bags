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
import re
import sys


def make_data_df(bag):
    """Get the md5 and path for every file in the bag's data folder and save to a dataframe
    Parameter: bag (string) - path to bag
    Returns: df_data (DataFrame) - columns Data_MD5, Data_Path
    """
    # File paths in the dataframe start with data and have forward slashes to match the manifest.
    # If the file path is too long, fixity cannot be calculated (FileNotFoundError).
    data_folder_list = []
    for root, dirs, files in os.walk(os.path.join(bag, 'data')):
        for file in files:
            filepath = os.path.join(root, file)
            root_from_data = re.search(rf"{'data'}.*", root).group()
            root_from_data = root_from_data.replace('\\', '/')
            filepath_from_data = f'{root_from_data}/{file}'
            try:
                with open(filepath, 'rb') as open_file:
                    data = open_file.read()
                    md5_generated = hashlib.md5(data).hexdigest()
                data_folder_list.append([md5_generated, filepath_from_data])
            except FileNotFoundError:
                data_folder_list.append(['FileNotFoundError-cannot-calculate-md5', filepath_from_data])
    df_data = pd.DataFrame(data_folder_list, columns=['Data_MD5', 'Data_Path'], dtype=str)
    return df_data


if __name__ == '__main__':

    # Get bag_path from script argument.
    bag_path = sys.argv[1]

    # Create a dataframe with the file path and md5 for every file in the data folder.
    data_df = make_data_df(bag_path)

    # Read the bag md5 manifest to a dataframe.

    # Compare the bag and manifest dataframes.

    # Make a log of the differences.

    # Print a summary of the result.