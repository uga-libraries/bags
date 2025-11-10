"""Functions used by more than one test for reading and formatting the test results"""

import os
import pandas as pd


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list with one line per row and blanks filled with a string"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


def make_directory_list(path):
    """Makes a list of the full paths for all the folders and files in the specified directory"""
    dir_list = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_list.append(os.path.join(root, dir_name))
        for file_name in files:
            dir_list.append(os.path.join(root, file_name))
    dir_list.sort()
    return dir_list
