"""Remove any temporary files in the bag that are not in the bag manifest and validate the bag

Parameter:
    bag_path (required): path to the bag (folder that ends in "_bag")

Returns:
    Prints any files that are not in the manifest but did not quality as temporary files
    Prints the validation result
"""
import bagit
import os
import pandas
import sys


if __name__ == '__main__':
    # Get bag_path from script argument.

    # Find any files that are in the bag data folder but not in the manifest (extra files).

    # Delete any extra files that are temp files and print the path for any other files.

    # Validate the bag and print the results.