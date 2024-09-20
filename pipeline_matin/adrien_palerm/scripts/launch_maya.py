
# import python built-in modules
import sys
import os
import subprocess

# Add the "script" directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from settings import get_settings
from pipeline import get_pipeline_root

def launch_maya():
    """
    This function opens maya, with custom shelves and python paths
    Maya's configuration is done by using environment variables, which
    can be accessed in python with os.environ, then passed to a Popen object
    """
    # Get pipeline's root path
    pipeline_root = get_pipeline_root()

    # Get maya path
    settings = get_settings()
    maya_path = settings["maya_path"]

    # Set maya preferences
    environment_variables = os.environ.copy()
    # Set maya's preferences main folder
    environment_variables["MAYA_APP_DIR"] = settings["maya_preferences_folder"]
    # Set additional python paths, this is needed so we can easily import python scripts
    environment_variables["PYTHONPATH"] = pipeline_root + "/scripts"
    # Set additional shelf directory
    environment_variables["MAYA_SHELF_PATH"] = pipeline_root + "/maya_shelves"
    
    # Open maya
    subprocess.Popen(
        [maya_path],
        env=environment_variables
    )

# This part is a way of telling python what to do when this file is run
if __name__ == "__main__":
    launch_maya()