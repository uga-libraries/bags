"""Validate all bags at any level in a directory structure and saves the result to a log

Use this script to skip reading through the extra text printed by bagit.py validation.
Bags must be named with "_bag" on the end to be detected as a bag by the script.

Parameters:
    bag_directory (required): path to the directory with the bags

Returns:
    Makes bag_validation_log.csv in bag_directory
"""
import bagit
import csv
import os
import sys
from shared_functions import log


def make_log(bag_path, is_valid=None, note=None, new_log=False):
    """Make or add to a log with validation results for each bag, saved to the bag_directory
    Parameters:
        bag_path (string) - path to bag_dir (if header) or specific bag
        is_valid (Boolean, optional) - if the bag is valid
        note (string, optional) - error output of bagit
        new_log (Boolean, optional) - True if a new log should be started with a header
    Returns: None
    """
    if new_log:
        log_path = os.path.join(bag_path, 'bag_validation_log.csv')
        with open(log_path, 'w', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(['Bag_Path', 'Valid?', 'Notes'])
    else:
        log_path = os.path.join(os.path.dirname(bag_path), 'bag_validation_log.csv')
        with open(log_path, 'a', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow([bag_path, is_valid, note])


if __name__ == '__main__':

    # Parent folder of the bags to be validated.
    bag_dir = sys.argv[1]

    # Starts the bag validation log in the same folder as the bags.
    log_file = log_path = os.path.join(bag_dir, 'bag_validation_log.csv')
    log(log_file, ['Bag_Path', 'Valid?', 'Notes'])

    for root, directory, folder in os.walk(bag_dir):

        # A directory is a bag if the name ends with _bag
        # Use root variable to have the full filepath.
        if root.endswith('_bag'):
            bag = bagit.Bag(root)
            try:
                bag.validate()
                log(log_file, [root, True, None])
            except bagit.BagValidationError as errors:
                log(log_file, [root, False, errors])
