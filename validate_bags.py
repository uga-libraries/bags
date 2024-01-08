# Find and validate all bags at any level in a directory structure.
# Only print final results and any errors to terminal. Otherwise, there is a lot of information printed to the terminal which makes a lot to scroll through to find the final validation result.

# Bags should be named with the convention 'name_bag'.

# Usage: python3 /path/script /path/bag_directory

import os
import subprocess
import sys

# Indicate the directory that contains bags.
bags = sys.argv[1]

for root, directory, folder in os.walk(bags):

    # A directory is a bag if the name ends with _bag
    # Use root variable to have the full filepath.
    if root.endswith('_bag'):

        # Save the validation results to a variable.
        # Print a summary of the results to the terminal.
        validation = subprocess.run(f'bagit.py --validate "{root}"', stderr=subprocess.PIPE, shell=True)

        if 'is invalid' in str(validation.stderr):
            print("\nBag invalid: ", root)
            print(validation.stderr.decode('utf-8'))

        else:
            print("\nBag valid: ", root)
        
