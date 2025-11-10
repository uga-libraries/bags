"""Validate all bags at any level in a directory structure and print the result

Use this script to skip reading through the extra text printed by bagit.py validation.
Bags must be named with "_bag" on the end to be detected as a bag by the script.

Parameters:
    bag_directory (required): path to the directory with the bags

Returns:
    If the bag is valid, it will print the bag name and that it is valid.
    If the bag is invalid, it will print the bag name, that it is invalid, and the error message
"""
import bagit
import os
import sys

# Indicate the directory that contains bags.
bags = sys.argv[1]

for root, directory, folder in os.walk(bags):

    # A directory is a bag if the name ends with _bag
    # Use root variable to have the full filepath.
    if root.endswith('_bag'):
        bag = bagit.Bag(root)
        try:
            bag.validate()
            print(f"\nBag valid: {root}")
        except bagit.BagValidationError as errors:
            print(f"\nBag invalid: {root} {errors}")
