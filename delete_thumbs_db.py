"""Remove any Thumbs.db in the bag, update the bag, and validate the bag

Thumbs.db can auto-generate after the bag is made or change after the bag is made,
causing bag validation errors in bags that are part of the backlog for a while.
This script corrects it so the bag can be validated and any non-Thumbs.db errors identified.

Parameter:
    bag_path (required): path to the bag (folder that ends in "_bag")

Returns:
    Prints the validation result
"""
import bagit
import csv
import os
import sys


def log(log_path, row):
    """Make or add to a log with validation results for each bag, saved to the same folder as the bag list
    Parameters:
        log_path (string) - path to the log file
        row (list) - data to save as a single row in the log
    Returns: None
    """
    with open(log_path, 'a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(row)


def make_bag_list(path):
    """Get a list of bag paths from a text file"""
    with open(path) as doc:
        bag_path_list = doc.readlines()
    bag_path_list = [item.rstrip('\n') for item in bag_path_list]
    return bag_path_list


def delete_thumbs(bag):
    """Delete any Thumbs.db files in the bag
    Parameter: bag (string) - path to bag
    Returns: None"""
    for root, dirs, files in os.walk(bag):
        for file in files:
            if file == 'Thumbs.db':
                os.remove(os.path.join(root, file))


def update_bag(bag):
    """Update the bag so any Thumbs.db that were part of the manifest are removed
    Parameter: bag (string) - path to bag
    Returns: None"""
    bag_inst = bagit.Bag(bag)
    bag_inst.save(manifests=True)


def validate_bag(bag):
    """Validate the bag and return the result for the log
    Parameter: bag (string) - path to bag
    Returns: is_valid (Boolean) and  error_msg (String or None)"""
    bagit_bag = bagit.Bag(bag)
    try:
        bagit_bag.validate()
        return True, None
    except bagit.BagValidationError as error_msg:
        return False, error_msg


if __name__ == '__main__':

    # Get a list of bags to update from a text file (path is the script argument).
    bag_list = make_bag_list(sys.argv[1])

    # Start bag validation log in the same folder as the bag list file.
    log_file_path = os.path.join(os.path.dirname(sys.argv[1]), 'bag_validation_log.csv')
    log(log_file_path, ['Bag_Path', 'Valid?', 'Notes'])

    # For each bag, delete all Thumbs.db from the bag's data folder, update and validate the bag, and log the result.
    for bag_path in bag_list:
        delete_thumbs(bag_path)
        update_bag(bag_path)
        is_valid, errors = validate_bag(bag_path)
        log(log_file_path, [bag_path, is_valid, errors])
