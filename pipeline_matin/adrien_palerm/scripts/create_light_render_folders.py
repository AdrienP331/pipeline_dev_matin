import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from json_files import file_to_dict
from pattern_resolver import resolve_pattern
from create_folder import create_folder

def create_shot_folders(shot_document):

    # Creates all folders provided as a dictionary
    # Here we list and automatize the folders to create 
    folders_to_create = [
        "<project_root>/light_render/shots/<sequence>/<shot>/scenes",
        "<project_root>/light_render/shots/<sequence>/<shot>/render",
    ]
    # Then we loop a folder creating funtion til every folder is created
    for folder_pattern in folders_to_create:
        create_folder(folder_pattern, shot_document)

if __name__ == "__main__":
    paths = sys.argv[1:]    #On recupere a partir de l'argument 1 entre dans la fonction, jusqu'a la fin
    for path in paths:
        shot_document = file_to_dict(path)
        print("Creating folders for shot : " + shot_document["shot"])
        create_shot_folders(shot_document)