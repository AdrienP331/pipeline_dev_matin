import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from json_files import file_to_dict
from pattern_resolver import resolve_pattern

def create_asset_folders(asset_document):
    """
    Creates all folders related to the asset provided as a dictionary
    """
    folders_to_create = [
        "<project_root>/assets/<type>/<group>/<asset>/modeling/work",
        "<project_root>/assets/<type>/<group>/<asset>/modeling/publish",
        "<project_root>/assets/<type>/<group>/<asset>/shading/work",
        "<project_root>/assets/<type>/<group>/<asset>/shading/publish",
    ]
    for folder_pattern in folders_to_create:
        create_folder(folder_pattern, asset_document)


def create_folder(folder_pattern, asset_document):
    """
    Resolves the pattern with the values provided through the asset document
    """
    # Resolve pattern
    folder = resolve_pattern(folder_pattern, asset_document)

    # Create folder
    if not os.path.exists(folder):
        print("Creating folder : " + folder)
        os.makedirs(folder)


if __name__ == "__main__":
    paths = sys.argv[1:]
    for path in paths:
        asset_document = file_to_dict(path)
        print("Creating folders for asset : " + asset_document["asset"])
        create_asset_folders(asset_document)