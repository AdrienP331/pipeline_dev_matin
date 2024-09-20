import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from json_files import file_to_dict
from pattern_resolver import resolve_pattern

def create_shot_folders(shot_document):
    """
    Creates all folders related to the shot provided as a dictionary
    """
    folders_to_create = [
        "<project_root>/shots/<sequence>/<shot>/layout/work",
        "<project_root>/shots/<sequence>/<shot>/layout/publish",
        "<project_root>/shots/<sequence>/<shot>/animation/work",
        "<project_root>/shots/<sequence>/<shot>/animation/publish",
        "<project_root>/shots/<sequence>/<shot>/lighting/work",
        "<project_root>/shots/<sequence>/<shot>/lighting/publish",
    ]
    for folder_pattern in folders_to_create:
        create_folder(folder_pattern, shot_document)


def create_folder(folder_pattern, shot_document):
    """
    Resolves the pattern with the values provided through the shot document
    """
    # Resolve pattern
    folder = resolve_pattern(folder_pattern, shot_document)

    # Create folder
    if not os.path.exists(folder):
        print("Creating folder : " + folder)
        os.makedirs(folder)


if __name__ == "__main__":
    paths = sys.argv[1:]
    for path in paths:
        shot_document = file_to_dict(path)
        print("Creating folders for shot : " + shot_document["shot"])
        create_shot_folders(shot_document)