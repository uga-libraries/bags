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


if __name__ == '__main__':

    # Get bag_path from script argument.
    bag_path = sys.argv[1]

    # Delete any Thumbs.db in the bag's data folder.

    # Update the bag.

    # Validate the bag.
    validate_bag(bag_path)