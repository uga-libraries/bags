# Quick scripts to work with Library of Congress bags.


# undo_bags
Remove content from bags. Deletes the manifests, moves content from the data folder into the parent directory, deletes the data folder, and renames the parent directory to remove \'_bag\'. The is a script that will do a single bag and a script to do all bags located within a single folder.

Common usage is if bag files when they are initially donated, and then after time passes we validate the bag to ensure the content is unchanged and then want to delete or otherwise change content before putting it in another bag for permenant preservation.

# validate_batch
Validate all bags within a single folder and dislay a summary of the results in the terminal. The summary includes the bag name, if it is valid or invalid, and for invalid ones the error message.

Common usage is to validate a number of bags at once and not have to scroll through the extra text displayed in the terminal (fixity results of every file in the bag) to figure out if each bag is valid or not.
