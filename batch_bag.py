"""Make each folder in the provided directory into a bag with MD5 fixity and validate it, with logging.

This script is primarily used in the accessioning workflow when an accession is too big for a single bag.
It will skip any folder that ends with "_bags", which is used if a folder needs to be further split into bags,
and any files that are not in folders, which should be foldered by the archivist prior to running the script.

If the script breaks or needs to be interrupted, run it again with the same parameter to restart,
after resetting the folder the script ends on if it was partially bagged.
It will skip any folders already made into a bag and add to the existing log.

Parameter:
    bag_directory (required): path to the directory that contains the folders to be bagged

Returns:
    bag_validation_log.csv in the bag_directory
"""
import bagit
import os
import sys
from shared_functions import log, validate_bag


def make_bag(bag):
    """Make bag and rename it to add "_bag" according to standard naming conventions
    Since these are for the backlog and not for preservation, we only use the MD5 checksum.
    PermissionError can happen due to path length or spaces at the end of folders or files,
    but can also happen with no clear cause.
    Parameter: bag (string) - path to bag, needed to make full path for file
    Returns: is_bagged (Boolean) - if there was an error, so the validation step can be skipped if needed
    """
    try:
        bagit.make_bag(bag, checksums=['md5'])
        os.replace(bag, f'{bag}_bag')
        return True
    except PermissionError as error:
        log(log_file, [f'{folder}_bag', 'TBD', error])
        return False


if __name__ == '__main__':

    # Parent folder of the folders to be bagged.
    bag_dir = sys.argv[1]

    # A log will already exist, and will be added to, if the script is being restarted.
    log_file = os.path.join(bag_dir, 'bag_validation_log.csv')
    if not os.path.exists(log_file):
        log(log_file, ['Bag', 'Bag_Valid', 'Errors'])

    for folder in os.listdir(bag_dir):
        bag_path = os.path.join(bag_dir, folder)

        # Skip all files and any folders that are big enough that the subfolders will be bags instead.
        # They are still added to the log for checking that they should be been skipped.
        # They will be added again if the script is restarted.
        if os.path.isfile(bag_path) or bag_path.endswith('_bags'):
            log(log_file, [folder, 'Skipped', None])
            continue

        # Skip any folders already in a bag, for if the script is being restarted.
        # Does not add them to the log as skipped, since they should already be in the log from when they were bagged.
        if bag_path.endswith('_bag'):
            continue

        print("Starting on", bag_path)

        # Make into bag. It will not try the last step of validating if there is an error.
        bagged = make_bag(bag_path)
        if not bagged:
            continue

        # Validate the bag and log the result.
        is_valid, errors = validate_bag(f'{bag_path}_bag')
        log(log_file, [f'{folder}_bag', is_valid, errors])
