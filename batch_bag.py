"""Make each folder in the provided directory into a bag and validate it, with logging

This script is primarily used in the accessioning workflow when an accession is too big for a single bag.
It will skip any folder that ends with "_bags", which is used if a folder needs to be further split into bags.

Parameter:
    bag_directory (required): path to the directory that contains the folders to be bagged

Returns:
    Log
"""
import bagit
import csv
import os
import sys


def make_log(bag_path, note, header=False):
    """Make or add to a log with validation results for each bag"""
    if header:
        log_path = os.path.join(bag_path, 'bag_validation_log.csv')
        with open(log_path, 'w', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(['Bag', 'Valid?', 'Notes'])
    else:
        log_path = os.path.join(os.path.dirname(bag_path), 'bag_validation_log.csv')
        with open(log_path, 'a', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow([os.path.basename(bag_path), note == 'Valid', note])


def validate_bag(bag_path):
    """Validate a bag and returns the result
    Parameter: bag (string) - path to bag
    Returns: None
    """
    bag_instance = bagit.Bag(bag_path)
    try:
        bag_instance.validate()
        return "Valid"
    except bagit.BagValidationError as errors:
        return errors


if __name__ == '__main__':

    bag_dir = sys.argv[1]
    make_log(bag_dir, None, header=True)
    for folder in os.listdir(bag_dir):
        folder_path = os.path.join(bag_dir, folder)

        # Skip the log file.
        if folder_path.endswith('bag_validation_log.csv'):
            continue

        # Make bag and rename it to add "_bag" according to standard naming conventions.
        bagit.make_bag(folder_path, checksums=['md5'])
        os.replace(folder_path, f'{folder_path}_bag')

        # Validate the bag.
        bagit_output = validate_bag(f'{folder_path}_bag')
        make_log(f'{folder_path}_bag', bagit_output)
