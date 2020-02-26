# Undo a specified bag. Common usage is if bagged files when they were received and later what to do appraisal and delete some.

# Usage: python3 /path/script /path/bag

import os
import sys


# Indicate the directory to be unbagged.
bag = sys.argv[1]
os.chdir(bag)

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
if bag.endswith('_bag'):
    newname = bag.replace('_bag', '')
    os.replace(bag, newname)
