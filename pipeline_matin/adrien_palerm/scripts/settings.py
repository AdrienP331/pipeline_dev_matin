import os
from pipeline import get_pipeline_root
from json_files import file_to_dict

def get_settings():
    """
    Returns project settings contained in the settings.json file as a dictionary
    """
    # Get file path
    root_dir = get_pipeline_root()
    json_file = os.path.join(root_dir, "settings.json")

    # Convert to dictionary
    settings = file_to_dict(json_file)
    return settings

if __name__ == "__main__":
    print(get_settings())