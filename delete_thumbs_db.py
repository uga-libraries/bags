"""Remove any Thumbs.db in all bags in a list, update the bag, and validate the bag

Thumbs.db can auto-generate after the bag is made or change after the bag is made,
causing bag validation errors in bags that are part of the backlog for a while.
This script should only be run once it is established that Thumbs.db are the only reason the bag isn't valid,
since it updates the bag and therefore makes the current state the valid one.

Parameter:
    bag_list (required): path to a text file with the full path to all bags to be updated, one row per path

Returns:
    bag_validation_log.csv in the same directory as bag_list
"""
import bagit
import csv
import os
import sys
from shared_functions import log, make_bag_list, validate_bag


def delete_thumbs(bag):
    """Delete any Thumbs.db files in the bag
    Parameter: bag (string) - path to bag
    Returns: count (integer) - number of Thumbs.db that were deleted for the log"""
    count = 0
    for root, dirs, files in os.walk(bag):
        for file in files:
            if file == 'Thumbs.db':
                os.remove(os.path.join(root, file))
                count += 1
    return count


def update_bag(bag):
    """Update the bag so any Thumbs.db that were part of the manifest are removed
    Parameter: bag (string) - path to bag
    Returns: None"""
    bag_inst = bagit.Bag(bag)
    bag_inst.save(manifests=True)


if __name__ == '__main__':

    # Get a list of bags to update from a text file (path is the script argument).
    bag_list = make_bag_list(sys.argv[1])

    # Start the bag validation log in the same folder as the bag list file.
    log_file = os.path.join(os.path.dirname(sys.argv[1]), 'bag_validation_log.csv')
    log(log_file, ['Bag_Path', 'Thumbs_Deleted', 'Valid?', 'Notes'])

    # For each bag, delete all Thumbs.db from the bag's data folder, update and validate the bag, and log the result.
    for bag_path in bag_list:
        if not os.path.exists(bag_path):
            log(log_file, [bag_path, 'TBD', 'TBD', 'Bag path error'])
            continue
        print("Starting on", bag_path)
        thumb_count = delete_thumbs(bag_path)
        update_bag(bag_path)
        is_valid, errors = validate_bag(bag_path)
        log(log_file, [bag_path, thumb_count, is_valid, errors])
