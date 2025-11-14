"""Remove any temporary files in the bag that are not in the bag manifest and validate the bag

Parameter:
    bag_path (required): path to the bag (folder that ends in "_bag")
    script_mode (required): preview (print what will delete) or delete (actually delete)

Returns:
    Prints any files that are not in the manifest but did not quality as temporary files
    Prints the validation result
"""
import os
import pandas as pd
import re
import sys
from delete_thumbs_db import log, make_bag_list, validate_bag


def delete_temp(bag, extra_list, mode):
    """Delete any temp files from the bag and return a list of the ones that were not deleted,
    using the same criteria as the general aip script
    Parameters:
        bag (string) - path to bag, needed to make full path for file
        extra_list (list) - list of paths for files that are not in the bag manifest
        mode (string) - preview or delete, determines if the files should just be printed or actually deleted
    Returns:
        temp_count (integer) - number of temp files that will be/were deleted for the log
        not_temp (list) - list of paths for files that were not temp and therefore not deleted
    """
    count = 0
    not_temp = []
    delete_list = [".DS_Store", "._.DS_Store", "Thumbs.db"]
    for file_path in extra_list:
        file_name = file_path.split('/')[-1]
        if file_name in delete_list or file_name.endswith('.tmp') or file_name.startswith('.'):
            print(f'Delete {bag}/{file_path}')
            count += 1
            if mode == 'delete':
                os.remove(f'{bag}/{file_path}')
        else:
            not_temp.append(file_path)
    return count, not_temp


def find_extra_files(bag):
    """Find files (based on full file path) that are in the bag data folder and not the manifest
    Parameter: bag (string) - path to bag
    Returns: extras (list) - list of the paths for every file in data but not the manifest
    """
    # List of file paths in the data folder, saved as a dataframe to compare to manifest.
    # To match the manifest, the path needs to start at data and use forward slashes.
    data_paths = []
    for root, dirs, files in os.walk(os.path.join(bag, 'data')):
        for file in files:
            root_from_data = re.search(rf"{'data'}.*", root).group()
            root_from_data = root_from_data.replace('\\', '/')
            data_paths.append(f'{root_from_data}/{file}')
    data_df = pd.DataFrame(data_paths, columns=['Data_Paths'])

    # Read the bag manifest into a dataframe.
    # data (start of the path) has to be used as part of the separator because paths may also include a double space,
    # and needs to be added back so future paths are correct.
    manifest_df = pd.read_csv(os.path.join(bag, 'manifest-md5.txt'), sep='  data', engine='python',
                              names=['MD5', 'Manifest_Paths'])
    manifest_df['Manifest_Paths'] = 'data' + manifest_df['Manifest_Paths']

    # Compare the data path list and the bag manifest, and return those only in the data path list.
    compare_df = data_df.merge(manifest_df, left_on='Data_Paths', right_on='Manifest_Paths', how='left')
    data_only = compare_df[compare_df['Manifest_Paths'].isnull()]
    extras = data_only['Data_Paths'].tolist()
    return extras


def reminder(mode):
    """Prints a reminder of what the selected script mode does
    Parameter: mode (string) - preview or delete, determines if the files should just be printed or actually deleted
    Returns: None"""
    if mode == 'delete':
        print('\nRunning in script_mode "delete", which will delete extra temp files and validate the bag.')
    elif mode == 'preview':
        print('\nRunning in script_mode "preview", which will print files that would be deleted but changes nothing.')
    else:
        print(f'\nscript_mode {mode} is not "delete" or "preview".')
        sys.exit()


if __name__ == '__main__':

    # Get a list of bags to update from a text file (path is a script argument).
    bag_list = make_bag_list(sys.argv[1])

    # Print reminder of script mode functionality.
    script_mode = sys.argv[2]
    reminder(script_mode)

    # Start the log in the same folder as the bag list file.
    log_file_path = os.path.join(os.path.dirname(sys.argv[1]), f'{script_mode}_temp_log.csv')
    log(log_file_path, ['Bag', 'Temp_Count', 'Temp_Deleted', 'Files_Not_Deleted', 'Bag_Valid', 'Errors'])

    # For each bag, find temp files not in the bag manifest and act on them in accordance with the script mode.
    for bag_path in bag_list:
        if not os.path.exists(bag_path):
            log(log_file_path, [bag_path, 'TBD', 'TBD', 'TBD', 'Bag path error'])
            continue
        extra_files = find_extra_files(bag_path)
        delete_count, not_deleted = delete_temp(bag_path, extra_files, script_mode)
        if script_mode == 'delete':
            if len(not_deleted) == 0:
                is_valid, errors = validate_bag(bag_path)
                log(log_file_path, [bag_path, delete_count, 'TBD', not_deleted, is_valid, errors])
            else:
                log(log_file_path, [bag_path, delete_count, 'TBD', not_deleted, 'False', 'Files not in manifest'])
        elif script_mode == 'preview':
            log(log_file_path, [bag_path, delete_count, 'TBD', not_deleted, 'TBD', 'TBD'])
