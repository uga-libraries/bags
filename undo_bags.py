"""Remove content from one or more bags at any level in a directory structure

Bags should follow the naming convention of ending with "_bag".

Parameter:
    bag_directory (required): path to the directory with the bag or bags

Returns:
    Nothing.
    All content originally in bags will be in folders without the "_bag" ending
    and without the bag manifests or directory structure.
"""
import os
import sys


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


if __name__ == '__main__':
    # Indicate the directory that contains the bag or bags.
    bag_dir = sys.argv[1]
    os.chdir(bag_dir)

    for root, directory, folder in os.walk('.'):

        # A directory is a bag if the name ends with _bag
        # Use root variable to have the full filepath.
        if root.endswith('_bag'):
            delete_metadata(root)

            # Move the contents from the data folder into the parent directory.
            for item in os.listdir(f'{root}/data'):
                os.replace(f'{root}/data/{item}', f'{root}/{item}')

            # Delete the now-empty data folder.
            os.rmdir(f'{root}/data')

            # Delete '_bag' from the end of the directory name.
            newname = root.replace('_bag', '')
            os.replace(root, newname)
