"""Remove content from all bags at any level in a directory structure

Bags should follow the naming convention of ending with "_bag".

Parameter:
    bag_directory (required): path to the directory with the bags

Returns:
    Nothing.
    All content originally in bags will be in folders without the "_bag" ending
    and without the bag manifests or directory structure.
"""
import os
import sys

# Indicate the directory that contains bags.
bags = sys.argv[1]
os.chdir(bags)

for root, directory, folder in os.walk('.'):

    # A directory is a bag if the name ends with _bag
    # Use root variable to have the full filepath.
    if root.endswith('_bag'):

        # Delete the bag metadata files.
        for doc in os.listdir(root):
            if doc.endswith('.txt'):
                os.remove(f'{root}/{doc}')

        # Move the contents from the data folder into the parent directory.
        for item in os.listdir(f'{root}/data'):
            os.replace(f'{root}/data/{item}', f'{root}/{item}')

        # Delete the now-empty data folder.
        os.rmdir(f'{root}/data')

        # Delete '_bag' from the end of the directory name.
        newname = root.replace('_bag', '')
        os.replace(root, newname)
