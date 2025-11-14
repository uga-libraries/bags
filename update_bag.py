"""Updates a bag manifest when the contents have gotten out of sync and validates the new bag

Use this script after appraisal or adding new content to an existing bag

Parameters:
    bag_path (required): path to the bag folder

Returns:
    If the bag is valid, it will print the bag name and that it is valid.
    If the bag is invalid, it will print the bag name, that it is invalid, and the error message
"""
import bagit
import sys
from shared_functions import validate_bag


if __name__ == '__main__':

    # Updates the bag.
    bag = bagit.Bag(sys.argv[1])
    bag.save(manifests=True)

    # Validates the bag and print the errors, if any.
    is_valid, errors = validate_bag(sys.argv[1])
    if is_valid:
        print("Bag is valid")
    else:
        print(errors)
