# Quick scripts to work with Library of Congress bags

## Overview

Scripts to perform simple actions on Library of Congress bags.

Related script: [Unpack AIPs](https://github.com/uga-libraries/unpack-aips),
used to get AIPs from the preservation system ready to share with users.

## Getting Started

### Dependencies

- bagit python library
- pandas python library

### Script Arguments

bag_manifest_compare_files.py
* bag_path (required): path to the bag (folder that ends in "_bag")

delete_new_temp.py
* bag_path (required): path to the bag (folder that ends in "_bag")
* script_mode (required): preview (print what will delete) or delete (actually delete)

undo_all_bags.py
* bag_directory (required): path to directory that contains the bags. Bag folder names should end with "_bag".

undo_one_bag.py
* bag (required): path to the bag (folder that ends in "_bag")

update_bag.py
* bag_path (required): path to the bag.

validate_bags.py
* bag_directory (required): path to the directory that contains the bag. Bag folder names should end with "_bag". 

### Testing

There are unit tests for each script in the tests folder.
The scripts do not have functions, or just simple functions, so the only tests are for each entire script.
The tests for undo_one_bag.py are incomplete: see [Issue 1](https://github.com/uga-libraries/bags/issues/1)

## Workflow

### bag_manifest_compare_files.py

This script compares the file paths in the bag manifest to the files in the bag data folder
and makes a report of any path only in one location.

It was developed for investigating further when a bag validation error message is that the number of files changed
but does not indicate which files were added or deleted since the bag was made.

It is faster than bag_manifest_compare_fixity.py, which is used when the file count is the same and size is different.

### delete_new_temp.py

This script finds temporary files that are not in the manifest, deletes them, and validates the bag.
It does not delete temporary files that are in the manifest or non-temporary file that are not in the manifest.
It does not try to validate if some files are missing from the manifest and not deleted, 
but instead prints those files to review if they should be considered temporary or if the bag needs to be updated.

The script can also be run in preview mode, in which case it prints files to be deleted but deletes nothing.
This allows the archivist to check the script is deleting the correct files before doing the deletion.

It was developed for fixing errors when checking bags that have been in storage for some time.
We've found that some temporary files, especially .DS_Store and Thumbs.db, are generated on the Digital Production Hub
even if the folder hasn't been opened recently.

The temp files are removed, so we can check if the rest of the files are valid.
Otherwise, bag validation stops when the file count doesn't match and does not check the MD5.

### undo_all_bags.py and undo_one_bag.py

These scripts are used to removed files from all bags in a specified directory or a specified bag.
They are most commonly used when files are bagged for storage and later need to be worked on.
After validating the bag(s), the content is removed from the bags for further processing.

For each bag:
1. Deletes the bag manifests.
2. Moves the content from the data folder into the parent directory.
3. Deletes the data folder.
4. Renames the parent directory to remove "_bag".

### update_bags.py

This script updates the manifest in a bag to match what is currently in the data folder
and validates the bag, printing the result.

It was developed for use in born-digital accessioning and processing,
for when additional appraisal is done after the content is bagged and before it can be made into AIPs.

### validate_bags.py

This script validates all bags in a specified directory and prints the results to the terminal.
Use this instead of bagit.py's validation because bagit.py prints a lot of extra text during validation.

For each file in the directory:
1. Confirms it is a bag, based on naming convention of ending with "_bag".
2. Validates the bag using bagit.py.
3. Prints to the terminal the bag name, if it is valid or invalid, an any error message.

## Author

Adriane Hanson, Head of Digital Stewardship, University of Georgia