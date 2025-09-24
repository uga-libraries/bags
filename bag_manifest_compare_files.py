"""Compares the files in a bag manifest to the files in the data folder and creates a report of files in only one spot

Use this script after a bag validation error that indicates a different number of expected files
Use bag_manifest_compare_fixity.py instead when the validation error is the same number of files but a different size

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

    # Reads the bag manifest into a dataframe, removing the md5 column which isn't needed for this process.
    manifest_df = pd.read_csv(os.path.join(bag_path, 'manifest-md5.txt'),
                              delimiter='  ', names=['md5', 'paths'], engine='python')
    manifest_df.drop(['md5'], axis=1, inplace=True)

    # Makes a dataframe with the relative paths of files in the data folder, starting with data.
    # Direction of slash is changed to match the bagit manifest.
    data_paths = []
    data_path = os.path.join(bag_path, 'data')
    for root, dirs, files in os.walk(os.path.join(bag_path, 'data')):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), bag_path)
            relative_path = relative_path.replace('\\', '/')
            data_paths.append(relative_path)
    data_df = pd.DataFrame(data_paths, columns=['paths'])

    # Compares the manifest to the files in the data folder, removing any rows that match.
    df_compare = manifest_df.merge(data_df, how='outer', indicator='True')
    df_compare = df_compare[df_compare['True'] != 'both']

    # Updates column and value names to be more human-readable.
    df_compare.rename(columns={'True': 'path_location'}, inplace=True)
    df_compare['path_location'] = df_compare['path_location'].str.replace('left_only', 'manifest', regex=False)
    df_compare['path_location'] = df_compare['path_location'].str.replace('right_only', 'data', regex=False)

    # Saves paths only in the manifest or only in the data folder to a csv in the parent directory of the bag.
    report_path = os.path.join(os.path.dirname(bag_path), f'{os.path.basename(bag_path)}_manifest_compare_report.csv')
    df_compare.to_csv(report_path, index=False)
