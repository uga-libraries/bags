# Quick scripts to work with Library of Congress bags.


# undo_bags
Remove content from bags. Deletes the manifests, moves content from the data folder into the parent directory, deletes the data folder, and renames the parent directory to remove \'_bag\'. There is a script that will do a single bag and a script to do all bags located within a single folder.

A common usage is if files are bagged to be stored for some time before additional steps are taken, e.g. bagging a new donation to be processed at a later date. When the files are to be worked on again, the bag is validated to ensure the files are unchanged from their time in storage and then the files are unbagged to be worked on. Once that work is complete, they will be bagged again.

# validate_batch
Validate all bags within a single folder and display a summary of the results in the terminal. The summary includes the bag name, if it is valid or invalid, and for invalid ones the error message.

Use this instead of bagit.py's validation to get a summary of if all the bags are valid without having to scroll through all the additional text displayed in the terminal by bagit.py.
