"""Compares the files in a bag manifest to the files in the data folder and creates a report of files in only one spot.

Use this script after a bag validation error that indicates a different number of expected files.
Use bag_manifest_compare_fixity.py instead when the validation error is the same number of files but a different size.

Parameters:
    bag_path (required): path to the bag folder

Returns:
    bag_manifest_compare_files_report.csv (saved to the parent folder of the bag_path)
"""
import os
import pandas as pd
import re
import sys


def make_data_df(bag):
    """Get the path for every file in the bag's data folder and save to a dataframe
    Parameter: bag (string) - path to bag
    Returns: df_data (DataFrame) - column Data_Path
    """
    # File paths in the dataframe start with data and have forward slashes to match the manifest.
    data_folder_list = []
    for root, dirs, files in os.walk(os.path.join(bag, 'data')):
        for file in files:
            root_from_data = re.search(rf"{'data'}.*", root).group()
            root_from_data = root_from_data.replace('\\', '/')
            data_folder_list.append(f'{root_from_data}/{file}')
    df_data = pd.DataFrame(data_folder_list, columns=['Path'])
    return df_data


if __name__ == '__main__':

    bag_path = sys.argv[1]
    data_df = make_data_df(bag_path)

    # Reads the bag manifest into a dataframe, removing the md5 column which isn't needed for this process.
    manifest_df = pd.read_csv(os.path.join(bag_path, 'manifest-md5.txt'),
                              delimiter='  ', names=['md5', 'paths'], engine='python')
    manifest_df.drop(['md5'], axis=1, inplace=True)

    # Compares the manifest to the files in the data folder, removing any rows that match.
    df_compare = manifest_df.merge(data_df, how='outer', indicator='True')
    df_compare = df_compare[df_compare['True'] != 'both']

    # Updates column and value names to be more human-readable.
    df_compare.rename(columns={'True': 'path_location'}, inplace=True)
    df_compare['path_location'] = df_compare['path_location'].str.replace('left_only', 'manifest', regex=False)
    df_compare['path_location'] = df_compare['path_location'].str.replace('right_only', 'data', regex=False)

    # Saves paths only in the manifest or only in the data folder to a csv in the parent directory of the bag.
    report_path = os.path.join(os.path.dirname(bag_path), 'bag_manifest_compare_files_report.csv')
    df_compare.to_csv(report_path, index=False)
