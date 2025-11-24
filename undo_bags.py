"""Remove content from one or more bags at any level in a directory structure, if the bag is valid

Bags should follow the naming convention of ending with "_bag".
If a bag is not valid, it will print the error and not do the rest of the script,
so the error can be investigated before the bag metadata needed for this review is deleted.

Parameter:
    bag_directory (required): path to the directory with the bag or bags

Returns:
    Nothing.
    All content originally in bags will be in folders without the "_bag" ending
    and without the bag manifests or directory structure.
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
    for root, directory, folder in os.walk(bag_dir):
        if root.endswith('_bag'):
            print("Starting on", root)
            is_valid, errors = validate_bag(root)
            if is_valid:
                delete_metadata(root)
                correct_reorg = reorganize(root)
                if correct_reorg:
                    rename(root)
                else:
                    print("Error: data folder not empty after reorganize")
            else:
                print("Bag is not valid. Review before undoing.")
