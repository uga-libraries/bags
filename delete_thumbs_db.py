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

    # Get bag_path from script argument.
    bag_path = sys.argv[1]

    # Delete any Thumbs.db in the bag's data folder.
    delete_thumbs(bag_path)

    # Update the bag.
    update_bag(bag_path)

    # Validate the bag and print the result.
    validate_bag(bag_path)
