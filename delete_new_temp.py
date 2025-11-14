"""Identify or delete any temporary files that are not in the bag manifest in all bags in a list and validate the bags

Parameter:
    bag_list (required): path to a text file with the full path to all bags to be updated, one row per path
    script_mode (required): preview (log what would delete) or delete (actually delete)

Returns:
    preview_new_temp_log.py or delete_new_temp_log.py in the same directory as bag_list
"""
import os
import pandas as pd
import re
import sys
from delete_thumbs_db import log, make_bag_list, validate_bag


def delete_temp(bag, temp):
    """Delete any extra temp files from the bag
    Parameters:
        bag (string) - path to bag, needed to make full path for file
        temp (list) - list of paths for temp files that are not in the bag manifest
    Returns: None
    """
    for file_path in temp:
        os.remove(os.path.join(bag, file_path))


def find_extra_files(bag):
    """Find files that are in the bag data folder and not the manifest, classifying them as temporary or not
    Parameter: bag (string) - path to bag
    Returns:
        temp (list) - list of the paths for every temp file in the data folder but not the manifest
        not_temp(list)- list of the paths for every non-temp file in the data folder but not the manifest
    """
    # Make a list of file paths in the data folder, reformatted and saved as a dataframe to compare to the manifest.
    # To match the manifest, the path needs to start at data and use forward slashes.
    data_paths = []
    for root, dirs, files in os.walk(os.path.join(bag, 'data')):
        for file in files:
            root_from_data = re.search(rf"{'data'}.*", root).group()
            root_from_data = root_from_data.replace('\\', '/')
            data_paths.append(f'{root_from_data}/{file}')
    data_df = pd.DataFrame(data_paths, columns=['Data_Paths'])

    # Read the bag manifest into a dataframe.
    # data (start of the path) has to be used as part of the separator because paths include other double spaces,
    # and needs to be added back so the paths to the files are correct if they are being deleted.
    manifest_df = pd.read_csv(os.path.join(bag, 'manifest-md5.txt'), sep='  data', engine='python',
                              names=['MD5', 'Manifest_Paths'])
    manifest_df['Manifest_Paths'] = 'data' + manifest_df['Manifest_Paths']

    # Compare the data folder and the bag manifest, and make a list of those only in the data folder (extras).
    compare_df = data_df.merge(manifest_df, left_on='Data_Paths', right_on='Manifest_Paths', how='left')
    data_only = compare_df[compare_df['Manifest_Paths'].isnull()]
    extras = data_only['Data_Paths'].tolist()

    # Sort the extras by if they are temporary files or not and return those lists.
    temp = []
    not_temp = []
    delete_list = [".DS_Store", "._.DS_Store", "Thumbs.db"]
    for file_path in extras:
        file_name = file_path.split('/')[-1]
        if file_name in delete_list or file_name.endswith('.tmp') or file_name.startswith('.'):
            temp.append(file_path)
        else:
            not_temp.append(file_path)
    return temp, not_temp


def reminder(mode):
    """Print a reminder of what the selected script mode does
    Parameter: mode (string) - preview or delete, determines if the files should just be logged or actually deleted
    Returns: None"""
    if mode == 'delete':
        print('\nRunning in script_mode "delete", which will delete extra temp files and validate the bag.')
    elif mode == 'preview':
        print('\nRunning in script_mode "preview", which will identify files that would be deleted but changes nothing.')
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
    log_file_path = os.path.join(os.path.dirname(sys.argv[1]), f'{script_mode}_new_temp_log.csv')
    log(log_file_path, ['Bag', 'Extra_Temp_Count', 'Extra_Temp', 'Extra_Not_Temp', 'Bag_Valid', 'Errors'])

    # For each bag, find files in the data folder and not in the bag manifest
    # and act on them in accordance with the script mode.
    # Preview logs, delete will delete extra temp files, validate the bag, and log.
    for bag_path in bag_list:
        if not os.path.exists(bag_path):
            log(log_file_path, [bag_path, 'TBD', 'TBD', 'TBD', 'TBD', 'Bag path error'])
            continue
        print("Starting on", bag_path)
        extra_temp, extra_not_temp = find_extra_files(bag_path)
        if script_mode == 'delete':
            delete_temp(bag_path, extra_temp)
            # Only validate if there were no extra files which were not temps, as those were not deleted,
            # which means the bag is still not valid.
            if len(extra_not_temp) == 0:
                is_valid, errors = validate_bag(bag_path)
                log(log_file_path, [bag_path, len(extra_temp), ', '.join(extra_temp), ', '.join(extra_not_temp),
                                    is_valid, errors])
            else:
                log(log_file_path, [bag_path, len(extra_temp), ', '.join(extra_temp), ', '.join(extra_not_temp),
                                    'False', 'Non-temp files not in manifest'])
        elif script_mode == 'preview':
            log(log_file_path, [bag_path, len(extra_temp), ', '.join(extra_temp), ', '.join(extra_not_temp),
                                'TBD', 'TBD'])
