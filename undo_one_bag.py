"""Remove content from a specified bag

The bag may or may not follow the naming convention of ending with "_bag".

Parameter:
    bag (required): path to the bag

Returns:
    Nothing.
    All content originally in the bag will be in the folder, without the bag manifests or directory structure.
    If the bag was originally named ending in "_bag", that ending will be removed.
"""
import os
import sys


# Indicate the directory to be unbagged.
bag_path = sys.argv[1]
os.chdir(bag_path)

# Delete the bag metadata files, which are all text files.
for doc in os.listdir('.'):
    if doc.endswith('.txt'):
        os.remove(doc)

# Move the contents from the data folder into the parent directory.
for item in os.listdir('data'):
    os.replace(f'data/{item}', item)

# Delete the now-empty data folder.
os.rmdir('data')

# Delete '_bag' from the end of the directory name if the standard bag naming convention was used.
if bag_path.endswith('_bag'):
    newname = bag_path.replace('_bag', '')
    os.replace(bag_path, newname)
