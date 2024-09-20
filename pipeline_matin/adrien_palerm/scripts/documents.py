import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from pipeline import get_pipeline_root
from json_files import file_to_dict

def get_asset_document(asset_name):
    """
    Returns the asset document corresponding to the provided asset name
    """
    pipeline_root = get_pipeline_root()
    asset_file = pipeline_root + "/database/assets/" + asset_name + ".json"
    asset_document = file_to_dict(asset_file)
    return asset_document

def get_shot_document(shot_name):
    """
    Returns the shot document corresponding to the provided shot name
    """
    pipeline_root = get_pipeline_root()
    shot_file = pipeline_root + "/database/shots/" + shot_name + ".json"
    shot_document = file_to_dict(shot_file)
    return shot_document