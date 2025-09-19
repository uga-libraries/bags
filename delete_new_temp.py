"""Remove any temporary files in the bag that are not in the bag manifest and validate the bag

Parameter:
    bag_path (required): path to the bag (folder that ends in "_bag")

Returns:
    Prints any files that are not in the manifest but did not quality as temporary files
    Prints the validation result
"""
import bagit
import os
import pandas
import re
import sys

import pandas as pd


def find_extra_files(bag):
    """Find files (based on full file path) that are in the bag data folder and not the manifest
    Parameter: bag (string) - path to bag
    Returns: extras (list) - list of the paths for every file in data but not the manifest
    """
    # List of file paths in the data folder, saved as a dataframe to compare to manifest.
    # To match the manifest, it needs to start at data.
    data_paths = []
    for root, dirs, files in os.walk(os.path.join(bag, 'data')):
        for file in files:
            root_from_data = re.search(rf"{'data'}.*", root).group()
            data_paths.append(os.path.join(root_from_data, file))
    data_df = pd.DataFrame(data_paths, columns=['Paths'])

    # Read the bag manifest into a dataframe.
    manifest_df = pd.read_csv(os.path.join(bag, 'manifest-md5.txt'), sep='  ', engine='python', names=['MD5', 'Paths'])

    # Compare the data path list and the bag manifest, and return those only in the data path list.
    data_only = data_df.merge(manifest_df, how='left')
    extras = data_only['Paths'].tolist()
    return extras


if __name__ == '__main__':
    # Get bag_path from script argument.
    bag_path = sys.argv[1]

    # Find any files that are in the bag data folder but not in the manifest (extra files).
    extra_files = find_extra_files(bag_path)

    # Delete any extra files that are temp files and print the path for any other files.

    # Validate the bag and print the results.