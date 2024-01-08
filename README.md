# Quick scripts to work with Library of Congress bags

## Overview

Scripts to perform simple actions on Library of Congress bags.
Includes removing content from a bag or batch of bags and validating a batch of bags.

Related script: [Unpack AIPs](https://github.com/uga-libraries/unpack-aips),
used to get AIPs from the preservation system ready to share with users.

## Getting Started

### Dependencies

These scripts only use standard Python libraries and have no special dependencies.

### Script Arguments

undo_all_bags.py
* bag_directory (required): path to directory that contains the bags. Bag folder names should end with "_bag".

undo_one_bag.py
* bag (required): path to the bag.

validate_bags.py
* bag_directory (required): path to the directory that contains the bag. Bag folder names should end with "_bag". 

### Testing

There are unit tests for each script in the tests folder.
The scripts do not have functions, so the only tests are for each entire script.
The tests for undo_one_bag.py are incomplete: see [Issue 1](https://github.com/uga-libraries/bags/issues/1)

## Workflow

undo_all_bags.py and undo_one_bag.py

These scripts are used to removed files from all bags in a specified directory or a specified bag.
They are most commonly used when files are bagged for storage and later need to be worked on.
After validating the bag(s), the content is removed from the bags for further processing.

For each bag:
1. Deletes the bag manifests.
2. Moves the content from the data folder into the parent directory.
3. Deletes the data folder.
4. Renames the parent directory to remove "_bag".

validate_bags.py

This script validates all bags in a specified directory and prints the results to the terminal.
Use this instead of bagit.py's validation because bagit.py prints a lot of extra text during validation.

For each file in the directory:
1. Confirms it is a bag, based on naming convention of ending with "_bag".
2. Validates the bag using bagit.py.
3. Prints to the terminal the bag name, if it is valid or invalid, an any error message.

## Author

Adriane Hanson, Head of Digital Stewardship, University of Georgia