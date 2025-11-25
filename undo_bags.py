"""Remove content from one or more bags within a given folder (bag_directory), if the bag is valid

Bags should follow the naming convention of ending with "_bag".
If a bag is not valid, it will print the error and not do the rest of the script,
so the error can be investigated before the bag metadata needed for this review is deleted.

If the bag_directory contains additional folders which themselves contain bags,
those bags will not be impacted by the script.
The script only acts on bags directly within the bag_directory so staff can easily determine all bags should be undone.

Parameter:
    bag_directory (required): path to the directory with the bag or bags

Returns:
    All folders originally within bags directly within the bag_directory will no longer be in bags:
    no bag manifests, no data folder, and "_bag" ending removed from the folder.
"""
import os
import sys
from shared_functions import validate_bag


def delete_metadata(bag):
    """Delete all metadata files from the bag
    Parameter: bag (string) - path to bag
    Returns: None
    """
    # Matches the bag metadata file names as much as possible to avoid accidentally any other files.
    # There should only be bag metadata files in this location, but sometimes other things are saved here in error.
    for doc in os.listdir(bag):
        doc_path = os.path.join(bag, doc)
        # These bag metadata files always have the same name.
        if doc == 'bag-info.txt' or doc == 'bagit.txt':
            os.remove(doc_path)
        # The manifest metadata files include the fixity type in the name.
        elif doc.startswith('manifest-') and doc.endswith('.txt'):
            os.remove(doc_path)
        elif doc.startswith('tagmanifest-') and doc.endswith('.txt'):
            os.remove(doc_path)


def reorganize(bag):
    """Move all files from the data folder of the bag
    Parameter: bag (string) - path to bag
    Returns: correct_reorg (Boolean) - True if no error, False if data didn't empty
    """
    # Moves the contents of the data folder into the parent directory.
    data_path = os.path.join(bag, 'data')
    for item in os.listdir(data_path):
        os.replace(os.path.join(data_path, item), os.path.join(bag, item))

    # Deletes the now-empty data folder, or returns an error if it wasn't empty.
    if not os.listdir(data_path):
        os.rmdir(data_path)
        return True
    else:
        return False


def rename(bag):
    """Delete '_bag' from the end of the directory name
    Parameter: bag (string) - path to bag
    Returns: None
    """
    # Use the position rather than replacing "_bag" in case the string is in other parts of the folder path,
    # where it needs to rename. This happens in the unit test and could happen with the backlog
    # for accessions split in multiple bags.
    new_name = bag[:-4]
    os.replace(bag, new_name)


if __name__ == '__main__':
    bag_dir = sys.argv[1]
    for folder in os.listdir(bag_dir):
        if folder.endswith('_bag'):
            bag_path = os.path.join(bag_dir, folder)
            print("Starting on", bag_path)
            is_valid, errors = validate_bag(bag_path)
            if is_valid:
                delete_metadata(bag_path)
                correct_reorg = reorganize(bag_path)
                if correct_reorg:
                    rename(bag_path)
                else:
                    print("Error: data folder not empty after reorganize")
            else:
                print("Bag is not valid. Review before undoing.")
