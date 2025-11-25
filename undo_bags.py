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
    bag_undo_log.csv (in bag_directory)
    All folders originally within bags directly within the bag_directory will no longer be in bags:
    no bag manifests, no data folder, and "_bag" ending removed from the folder.
"""
import os
import sys
from shared_functions import log, validate_bag


def delete_metadata(bag):
    """Delete all metadata files from the bag if only the expected metadata files are present
    Parameter: bag (string) - path to bag
    Returns: unexpected (string, None) - paths for all unexpected files in one string or None if no unexpected
    """
    # Variable for tracking unexpected files mixed with bag metadata.
    unexpected_list = []

    # Matches the bag metadata file names as much as possible to avoid accidentally any other files.
    # There should only be bag metadata files in this location, but sometimes other things are saved here in error.
    for doc in os.listdir(bag):
        if doc == 'data':
            continue
        doc_path = os.path.join(bag, doc)
        # These bag metadata files always have the same name.
        if doc == 'bag-info.txt' or doc == 'bagit.txt':
            os.remove(doc_path)
        # The manifest metadata files include the fixity type in the name.
        elif doc.startswith('manifest-') and doc.endswith('.txt'):
            os.remove(doc_path)
        elif doc.startswith('tagmanifest-') and doc.endswith('.txt'):
            os.remove(doc_path)
        else:
            unexpected_list.append(doc_path)

    # Return a string with the unexpected files or None.
    if len(unexpected_list) == 0:
        return None
    else:
        return f"Unexpected content mixed with bag metadata: {', '.join(unexpected_list)}"


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

    # Parent folder of the bag(s) to be undone.
    bag_dir = sys.argv[1]

    # Starts the bag validation log in the same folder as the bags.
    log_file = log_path = os.path.join(bag_dir, 'bag_undo_log.csv')
    log(log_file, ['Bag_Path', 'Bag_Valid', 'Errors'])

    # Finds all bags directly within the bag directory, based on the folder naming convention,
    # undoes the bag (stopping if there is an error) and logs the result.
    for folder in os.listdir(bag_dir):
        if folder.endswith('_bag'):
            bag_path = os.path.join(bag_dir, folder)
            print("Starting on", bag_path)
            is_valid, errors = validate_bag(bag_path)
            # Only continue with undoing the bag if the bag is valid.
            if is_valid:
                # Only continue with reorganizing the bag if there are no unexpected files mixed with bag metadata.
                unexpected = delete_metadata(bag_path)
                if unexpected:
                    log(log_path, [bag_path, True, unexpected])
                else:
                    # Only continue with renaming the bag if the data folder was empty and could be deleted.
                    correct_reorg = reorganize(bag_path)
                    if correct_reorg:
                        rename(bag_path)
                        log(log_path, [bag_path, True, None])
                    else:
                        log(log_path, [bag_path, True, 'data folder not empty after reorganize'])
            else:
                log(log_path, [bag_path, False, errors])
