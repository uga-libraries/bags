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
import pathlib
import re
import sys


def compare_df(df_data, df_manifest):
    """Make a df with all files that do not match between the data folder and manifest
    Parameters: Dataframes with file paths start with data
    Returns: df_compare (DataFrame) - columns Path, Source
    """
    # Compares the manifest to the files in the data folder, removing any rows that match.
    # The comparison column Path is named the same in both dataframes.
    df_compare = df_data.merge(df_manifest, how='outer', indicator='Source')
    df_compare = df_compare[df_compare['Source'] != 'both']

    # Updates the source names to be more human-readable.
    df_compare['Source'] = df_compare['Source'].str.replace('left_only', 'Data Folder', regex=False)
    df_compare['Source'] = df_compare['Source'].str.replace('right_only', 'Manifest', regex=False)

    return df_compare


def make_data_df(bag):
    """Get the path for every file in the bag's data folder and save to a dataframe
    Parameter: bag (string) - path to bag
    Returns: df_data (DataFrame) - column Path
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


def make_manifest_df(bag):
    """Get the path from the bag md5 manifest and save to a dataframe
    Parameter: bag (string) - path to bag
    Returns: df_manifest (DataFrame) - column Path
    """
    # In the manifest, each row is "MD5  data/path" and there is no header row.
    # The separator includes data because paths may also include a double space,
    # and data needs to be added back for easier comparison with data_df.
    manifest_path = os.path.join(bag, 'manifest-md5.txt')
    df_manifest = pd.read_csv(manifest_path, sep='  data', engine='python', names=['MD5', 'Path'])
    df_manifest['Path'] = 'data' + df_manifest['Path']
    df_manifest.drop(columns=['MD5'], inplace=True)
    return df_manifest


def save_report(df_diff, bag):
    """Save the rows for each file that didn't match between the data folder and manifest to a csv
    Parameters:
        df_diff (DataFrame) - Columns Path, Source
        bag (string) - path to bag, to get location for saving the report
    Returns: None (saves a CSV in the parent folder of the bag)
    """
    bag_dir = pathlib.Path(bag)
    report_path = os.path.join(bag_dir.parent, 'bag_manifest_compare_files_report.csv')
    df_diff.to_csv(report_path, index=False)


if __name__ == '__main__':

    bag_path = sys.argv[1]
    data_df = make_data_df(bag_path)
    manifest_df = make_manifest_df(bag_path)
    differences_df = compare_df(data_df, manifest_df)
    save_report(differences_df, bag_path)
