"""Compares the fixity of files in a bag manifest to the data folder and creates a report of differences,
which includes files that are only in the manifest, only in the data folder, or in both places with different fixity.

Use this script after a bag validation error that indicates the size has changed.
Use bag_manifest_compare_files.py instead when the error is a different number of files, which is faster.

This script is modeled after the function validate_bag_manifest() in validate_fixity.py in the hub-monitoring repo.

Parameters:
    bag_path (required): path to the bag folder

Returns:
    bag_manifest_compare_fixity_report.csv (saved to the parent folder of the bag_path)
"""
import csv
import hashlib
import os
import pandas as pd
import pathlib
import re
import sys


def compare_df(bag, df_manifest):
    """Make a df with all files that do not match fixity between the data folder and manifest
    Parameters:
         bag (string) - path to bag, where data_md5.csv is
         df_manifest (Pandas dataframe) - dataframe with MD5 and file paths starting with data
    Returns: df_diff (DataFrame) - columns MD5, Path, Source
    """
    # Reads the CSV with MD5s for files in the data folder into a dataframe.
    data_csv = os.path.join(os.path.dirname(bag), 'data_md5.csv')
    df_data = pd.read_csv(data_csv, names=['Data_MD5', 'Data_Path'])

    # Just merging on fixity, so the paths may not be exactly aligned in the case of duplicates.
    # After merging, column Source has left_only if it is only in df_data and right_only if it is only in df_manifest.
    # If it has both, that means the MD5 matched, and it will not be included in the log.
    df_compare = df_data.merge(df_manifest, how='outer', left_on='Data_MD5', right_on='Manifest_MD5', indicator='Source')

    # Makes and reformats separate dataframes for fixity only in one of each of the dataframes,
    # so they can be merged into a dataframe with three columns, not separate fixity and path columns for each source.
    df_data_only = df_compare[df_compare['Source'] == 'left_only'].copy()
    df_data_only.drop(columns=['Manifest_MD5', 'Manifest_Path'], inplace=True)
    df_data_only.rename(columns={'Data_MD5': 'MD5', 'Data_Path': 'Path'}, inplace=True)
    df_data_only['Source'] = 'Data Folder'

    df_manifest_only = df_compare[df_compare['Source'] == 'right_only'].copy()
    df_manifest_only.drop(columns=['Data_MD5', 'Data_Path'], inplace=True)
    df_manifest_only.rename(columns={'Manifest_MD5': 'MD5', 'Manifest_Path': 'Path'}, inplace=True)
    df_manifest_only['Source'] = 'Manifest'

    # Combines the two dataframes. It now has three columns: MD5, Path, and Source.
    df_diff = pd.concat([df_data_only, df_manifest_only], ignore_index=True)
    return df_diff


def make_data_md5_csv(bag):
    """Get the md5 and path for every file in the bag's data folder and save to a CSV
    To allow restarting, if the CSV exists, it only calculates the MD5 for files not in the CSV yet
    Parameter: bag (string) - path to bag
    Returns: None
    """
    # Determine if this is a restart based on if data_md5.csv is already present,
    # and if so, make a list of file paths already in the CSV.
    data_csv = os.path.join(os.path.dirname(bag), 'data_md5.csv')
    restart = os.path.exists(data_csv)
    path_list=[]
    if restart:
        df_data = pd.read_csv(data_csv, names=['Data_MD5', 'Data_Path'])
        path_list = df_data['Data_Path'].tolist()

    # Get the MD5 and path for every file in the data folder, updating the path to match the bag manifest formatting.
    # During a restart, this is only done for files that are not already in data_md5.csv.
    for root, dirs, files in os.walk(os.path.join(bag, 'data')):
        for file in files:
            # Make file paths start with data and have forward slashes to match the bag manifest.
            filepath = os.path.join(root, file)
            root_from_data = re.search(rf"{'data'}.*", root).group()
            root_from_data = root_from_data.replace('\\', '/')
            filepath_from_data = f'{root_from_data}/{file}'
            # Only get the MD5 if it is not a restart OR if it is a restart and the file isn't in the csv yet.
            if restart == False or filepath_from_data not in path_list:
                try:
                    with open(filepath, 'rb') as open_file:
                        data = open_file.read()
                        md5_generated = hashlib.md5(data).hexdigest()
                    save_md5(data_csv, [md5_generated, filepath_from_data])
                # If the file path is too long, fixity cannot be calculated (FileNotFoundError).
                except FileNotFoundError:
                    save_md5(data_csv, ['FileNotFoundError-cannot-calculate-md5', filepath_from_data])


def make_manifest_df(bag):
    """Get the md5 and path from the bag md5 manifest and save to a dataframe
    Parameter: bag (string) - path to bag
    Returns: df_manifest (DataFrame) - columns Manifest_MD5, Manifest_Path
    """
    # In the manifest, each row is "MD5  data/path" and there is no header row.
    # The separator includes data because paths may also include a double space,
    # and data needs to be added back for easier comparison with data_df.
    manifest_path = os.path.join(bag, 'manifest-md5.txt')
    df_manifest = pd.read_csv(manifest_path, sep='  data', engine='python', names=['Manifest_MD5', 'Manifest_Path'])
    df_manifest['Manifest_Path'] = 'data' + df_manifest['Manifest_Path']
    return df_manifest


def save_md5(csv_path, row):
    """Save a row to a csv with the md5 of a file in the data folder to allow the script to restart
    Parameters:
        csv_path (string) - path to csv, in parent folder of the bag
        row (list) - md5 and filepath for a single file
    """
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def save_report(df_diff, bag):
    """Save the rows for each file that didn't match between the data folder and manifest to a csv
    Parameters:
        df_diff (DataFrame) - Columns MD5, Path, Source
        bag (string) - path to bag, to get location for saving the report
    Returns: None (saves a CSV in the parent folder of the bag)
    """
    bag_dir = pathlib.Path(bag)
    report_path = os.path.join(bag_dir.parent, 'bag_manifest_compare_fixity_report.csv')

    # Dataframe is sorted by path to group files with changed fixity,
    # as opposed to files that are only in one of the two sources.
    df_diff.sort_values(by='Path', inplace=True)
    df_diff.to_csv(report_path, index=False)


if __name__ == '__main__':

    bag_path = sys.argv[1]
    make_data_md5_csv(bag_path)
    manifest_df = make_manifest_df(bag_path)
    differences_df = compare_df(bag_path, manifest_df)
    save_report(differences_df, bag_path)
