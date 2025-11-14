import bagit
import csv


def log(log_path, row):
    """Add a row to the specified log
    Parameters:
        log_path (string) - path to the log file
        row (list) - data to save as a single row in the log
    Returns: None
    """
    with open(log_path, 'a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(row)


def make_bag_list(bag_list_path):
    """Get a list of bag paths from a text file
    Parameter: path (string) - path to the text file with the bag paths
    Returns: bag_path_list (list) - list of paths from the text file"""
    with open(bag_list_path) as doc:
        bag_path_list = doc.readlines()
    bag_path_list = [item.rstrip('\n') for item in bag_path_list]
    return bag_path_list


def validate_bag(bag):
    """Validate the bag and return the result for the log
    Parameter: bag (string) - path to bag
    Returns: is_valid (Boolean) and  error_msg (String or None)"""
    bag_instance = bagit.Bag(bag)
    try:
        bag_instance.validate()
        return True, None
    except (bagit.BagValidationError, bagit.BagError) as error_msg:
        return False, error_msg
