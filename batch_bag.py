"""Make each folder in the provided directory into a bag and validate it, with logging

This script is primarily used in the accessioning workflow when an accession is too big for a single bag.
It will skip any folder that ends with "_bags", which is used if a folder needs to be further split into bags.

Parameter:
    bag_directory (required): path to the directory that contains the folders to be bagged

Returns:
    Log
"""
import bagit
import os
import sys


def validate_bag(bag_path):
    """Validates a bag and returns the result
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
    for folder in os.listdir(bag_dir):
        folder_path = os.path.join(bag_dir, folder)

        # Make bag and rename it to add "_bag" according to standard naming conventions.
        bagit.make_bag(folder_path, checksums=['md5'])
        os.replace(folder_path, f'{folder_path}_bag')

        # Validate the bag.
        error = validate_bag(f'{folder_path}_bag')
