"""Compares the fixity of files in a bag manifest to the data folder and creates a report of differences,
which includes files that are only in the bag manifest, only in the data folder, or in both places with different fixity.

Because it can run for a long time to calculate the MD5 of larger accessions, the script can be restarted.
Run the script again with the same parameter, and it will continue creating data_md5.csv where it left off.

Use this script after a bag validation error that indicates the size has changed.
Use compare_files.py instead when the error is a different number of files, which is faster.

This script is modeled after the function validate_bag_manifest() in validate_fixity.py in the hub-monitoring repo.

Parameters:
    bag_path (required): path to the bag folder

Returns:
    compare_fixity_report.csv (saved to the parent folder of the bag_path)
    data_md5.csv (saved to the parent folder of the bag_path)
"""
import csv
import hashlib
import os
import pandas as pd
import pathlib
import re
import sys


def compare_df(df_manifest, output):
    """Make a df with all files that do not match fixity between the data folder and bag manifest
    Parameters:
         df_manifest (Pandas dataframe) - dataframe with MD5 and file paths from bag manifest
         output (string) - path to the folder with the data_md5.csv (the parent folder of the bag)
    Returns: df_diff (DataFrame) - columns MD5, Path, Source
    """
    # Reads the CSV with MD5s for files in the data folder into a dataframe.
    data_csv = os.path.join(output, 'data_md5.csv')
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


def make_data_md5_csv(bag, output):
    """Get the MD5 and path for every file in the bag's data folder and save to a CSV in the parent folder of the bag
    To allow restarting, if the CSV exists, it only calculates the MD5 for files not in the CSV yet.
    Parameter:
        bag (string) - path to bag
        output (string) - path for where to save data_md5.csv (the parent folder of the bag)
    Returns: None
    """
    # Determine if this is a restart based on if data_md5.csv is already present,
    # and if so, make a list of file paths already in the CSV.
    data_csv = os.path.join(output, 'data_md5.csv')
    restart = os.path.exists(data_csv)
    path_list = []
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
            # Only get the MD5 if it is not a restart OR if it is a restart and the file isn't in the CSV yet.
            if restart is False or filepath_from_data not in path_list:
                try:
                    with open(filepath, 'rb') as open_file:
                        data = open_file.read()
                        md5_generated = hashlib.md5(data).hexdigest()
                    save_md5(data_csv, [md5_generated, filepath_from_data])
                # If the file path is too long, fixity cannot be calculated (FileNotFoundError).
                except FileNotFoundError:
                    save_md5(data_csv, ['FileNotFoundError-cannot-calculate-md5', filepath_from_data])


def make_manifest_df(bag):
    """Get the MD5 and path from the bag manifest-md5.txt and save to a dataframe
    Parameter: bag (string) - path to bag
    Returns: df_manifest (DataFrame) - columns Manifest_MD5, Manifest_Path
    """
    # In the bag manifest, each row is "MD5  data/path" and there is no header row.
    # The separator includes data because paths may also include a double space,
    # and so data needs to be added back to the paths for easier comparison with data_df.
    manifest_path = os.path.join(bag, 'manifest-md5.txt')
    df_manifest = pd.read_csv(manifest_path, sep='  data', engine='python', names=['Manifest_MD5', 'Manifest_Path'])
    df_manifest['Manifest_Path'] = 'data' + df_manifest['Manifest_Path']
    return df_manifest


def save_md5(csv_path, row):
    """Save a row to a CSV with the MD5 and path of a file in the data folder to allow the script to restart,
    since calculating the MD5s is the most time-consuming part of the script.
    Parameters:
        csv_path (string) - path to CSV, in the parent folder of the bag
        row (list) - MD5 and path for a single file
    Returns: None
    """
    with open(csv_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def save_report(df_diff, output):
    """Save the rows for each file that didn't match between the data folder and bag manifest to a CSV
    Parameters:
        df_diff (DataFrame) - Columns MD5, Path, Source
        output (string) - path for where to save the report (the parent folder of the bag)
    Returns: None
    """
    report_path = os.path.join(output, 'compare_fixity_report.csv')

    # Dataframe is sorted by path to group files with changed fixity.
    # If the dataframe is empty, a general message is saved to the report instead.
    if len(df_diff.index) > 0:
        df_diff.sort_values(by='Path', inplace=True)
        df_diff.to_csv(report_path, index=False)
    else:
        with open(report_path, 'w') as report:
            report.write('The bag is valid. No differences between the manifest and the data folder contents.')


if __name__ == '__main__':

    bag_path = sys.argv[1]
    output_path = os.path.dirname(bag_path)

    make_data_md5_csv(bag_path, output_path)
    manifest_df = make_manifest_df(bag_path)
    differences_df = compare_df(manifest_df, output_path)
    save_report(differences_df, output_path)
