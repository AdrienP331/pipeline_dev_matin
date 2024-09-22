
# import python built-in modules
import sys
import os
import subprocess

# Add the "script" directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from settings import get_settings

def launch_max():
    """
    This function opens 3dsmax, with custom shelves and python paths
    blender's configuration is done by using environment variables, which
    can be accessed in python with os.environ, then passed to a Popen object
    """

    # Get blender path
    settings = get_settings()
    max_path = settings["max_path"]
    
    # Open blender
    subprocess.Popen(
        [max_path]
    )

# This part is a way of telling python what to do when this file is run
if __name__ == "__main__":
    launch_max()