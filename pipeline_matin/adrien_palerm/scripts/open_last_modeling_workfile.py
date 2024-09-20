
# import python built-in modules
import sys
import os
import subprocess
from glob import glob

# Add the "script" directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from json_files import file_to_dict
from pattern_resolver import resolve_pattern
from settings import get_settings


def open_last_modeling_workfile(asset_document):
    """
    This function opens the latest modeling workfile.
    Please note that "latest" means "latest in alphabetical order", not "latest in date"
    """
    # Get search pattern
    pattern = "<project_root>/assets/<type>/<group>/<asset>/modeling/work/<asset>_v*_*.ma"
    search = resolve_pattern(pattern, asset_document)
    
    # Look for paths that match the search pattern
    paths = glob(search)
    if paths:
        # Get last version
        last_path = sorted(paths)[-1]

        # Open it in maya
        maya_path = get_settings()["maya_path"]
        subprocess.Popen([maya_path, last_path])
    else:
        # Display warning in the console
        input(f"{asset_document['asset']} : No modeling workfile matching the pattern {search} was found. Press any key to continue")


# This part is a way of telling python what to do when this file is run
if __name__ == "__main__":
    # Get files passed as arguments
    paths = sys.argv[1:]

    # Read each file and run the main function
    for path in paths:
        asset_document = file_to_dict(path)
        open_last_modeling_workfile(asset_document)