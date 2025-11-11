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
import os
import sys
from delete_new_temp import validate_bag


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


if __name__ == '__main__':

    # Get a list of bags to update from a text file (path is the script argument).
    bag_list = make_bag_list(sys.argv[1])
    print("Bag List", bag_list)

    # For each bag, delete all Thumbs.db from the bag's data folder, update the bag, and validate the bag.
    for bag_path in bag_list:
        delete_thumbs(bag_path)
        update_bag(bag_path)
        validate_bag(bag_path)
