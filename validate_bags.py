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


if __name__ == '__main__':

    # Parent folder of the bags to be validated.
    bag_dir = sys.argv[1]

    # Starts the bag validation log in the same folder as the bags.
    log_file = log_path = os.path.join(bag_dir, 'bag_validation_log.csv')
    log(log_file, ['Bag_Path', 'Bag_Valid', 'Errors'])

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
