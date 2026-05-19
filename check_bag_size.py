"""Check all bags in the provided directory for any that are above 100 GB or 10,000 files

This is used to double-check for bags over the recommended size for efficient validation.
It is a companion to check_file_count.py, which is run prior to making the bags.

Parameter:
    bag_directory (required): path to the directory that contains the bags

Returns:
    bag_size_check.csv in the bag_directory with the bag names, number of GB and files, and if they are over the maximum
"""
import csv
import bagit
import os
import sys


if __name__ == '__main__':

    # Parent folder of the bags.
    bag_dir = sys.argv[1]

    # Starts a log with a header for the results.
    log_path = os.path.join(bag_dir, 'bag_size_check.csv')
    with open(log_path, 'w', newline='') as log:
        log_writer = csv.writer(log)
        log_writer.writerow(['Bag', 'Size_GB', 'Size_OK', 'Files', 'Files_OK'])

    for bag in os.listdir(bag_dir):

        # Skips any metadata files. All folders should be bags.
        if os.path.isfile(os.path.join(bag_dir, bag)):
            continue

        # Gets size information from the bag payload.
        # File count is divided in half to exclude the metadata files (one FITS per file)
        # It is often a decimal because of the preservation.xml and potentially other files made by the script.
        bag_instance = bagit.Bag(os.path.join(bag_dir, bag))
        bag_payload = bag_instance.info['Payload-Oxum']
        size_bytes, file_count = bag_payload.split('.')
        size_bag = int(size_bytes) / 1000000000
        files = int(file_count) / 2

        # Saves size information for the current bag to the log,
        # including comparing it to the desired maximums.
        with open(log_path, 'a', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow([bag, size_bag, size_bag <= 100, files, files < 10000])
