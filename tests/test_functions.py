"""Functions used by more than one test for reading and formatting the test results"""

import pandas as pd


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list with one line per row and blanks filled with a string"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list
