# Quick scripts to work with Library of Congress bags

## Overview

Scripts to perform simple actions on Library of Congress bags.

Related script: [Unpack AIPs](https://github.com/uga-libraries/unpack-aips),
used to get AIPs from the preservation system ready to share with users.

## Getting Started

### Dependencies

- bagit python library
- pandas python library

### Testing

There are unit tests for each script in the "tests" folder.
The scripts do not have functions, or just simple functions, so the only tests are for each entire script.
The tests for undo_one_bag.py are incomplete: see [Issue 1](https://github.com/uga-libraries/bags/issues/1)

## Scripts

### bag_manifest_compare_files.py

Purpose: compare the file paths in the bag manifest to the files in the bag data folder and make a report of any path only in one location.

Argument: bag_path (required): path to the bag (folder that ends in "_bag")

This script was developed for investigating a bag validation error from the number of files changing,
since bagit does not indicate which files were added or deleted since the bag was made.

### bag_manifest_compare_fixity.py

Purpose: compare the MD5s in the bag manifest to the MD5s of files in the bag data folder and make a report of the differences, 
either because the fixity changed or the file is only in one location.

Argument: bag_path (required): path to the bag (folder that ends in "_bag")

This script was developed for investigating a bag validation error from the size changing,
since bagit does not indicate which files changed in size since the bag was made.

Because this script can run for a long time to calculate the MD5 of larger accessions, the script can be restarted.
Run the script again with the same parameter, and it will continue creating data_md5.csv where it left off.

### batch_bag.py

Purpose: make a bag with MD5 fixity from each folder in the bag_directory, validate it, and log the results.

Argument: bag_directory (required): path to the directory that contains the folders to bag.

This script is primarily used in the accessioning workflow when an accession is too big for a single bag.
Loose files should be put into folders prior to running the script.
The script will skip any files and any folder that ends with _bags, which indicates the subfolders will be bagged.

### delete_new_temp.py

Purpose: find temporary files that are not in the manifest, delete them (if delete mode), and validate the bag.

Arguments:
* bag_path (required): path to the bag (folder that ends in "_bag")
* script_mode (required): preview (print what will delete) or delete (actually delete)

This script was developed for fixing errors from checking fixity on bags that have been in storage for some time.
Some temporary files, especially .DS_Store and Thumbs.db, are generated even if the folder hasn't been opened recently.

The script does not delete temporary files that are in the manifest or non-temporary file that are not in the manifest.

### delete_thumbs_db.py

Purpose: delete Thumbs.db anywhere in the bag, update the bag, and validate the bag.

Argument: bag_path (required): path to the bag (folder that ends in "_bag")

This script should only be used after delete_new_temp.py or one of the bag manifest compare scripts shows that
Thumbs.db are the only reason the bag is not validating, because it updates the bag.

### undo_all_bags.py

Purpose: remove files from each bag in bag_directory.

Argument: bag_directory (required): path to directory that contains the bags. Bag folder names should end with "_bag".

This script is most commonly used when files are bagged for storage and later need to be worked on.
Bag metadata files are deleted, content is moved out of the data folder, and the folder is renamed to remove "_bag'.
Validate the bags prior to running this script.

### undo_one_bag.py

Purpose: remove files from the bag.

Argument: bag (required): path to the bag (folder that ends in "_bag")

This script is most commonly used when files are bagged for storage and later need to be worked on.
Bag metadata files are deleted, content is moved out of the data folder, and the folder is renamed to remove "_bag'.
Validate the bag prior to running this script.

### update_bag.py

Purpose: Update the manifest in a bag to match what is currently in the data folder and validates the bag.

Argument: bag_path (required): path to the bag.

This script was developed for use in born-digital accessioning and processing,
for when additional appraisal is done after the content is bagged and before it can be made into AIPs.
The validation result is printed to the terminal.

### validate_bags.py

Purpose: validate every bag in bag_directory.

Argument bag_directory (required): path to the directory that contains the bag. Bag folder names should end with "_bag". 

The results are printed to the terminal.
Use this script instead of bagit.py because bagit.py prints a lot of extra text during validation.

## Author

Adriane Hanson, Head of Digital Stewardship, University of Georgia