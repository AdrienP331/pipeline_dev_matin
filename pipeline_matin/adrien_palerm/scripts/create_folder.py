import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

# Import pipeline modules
from json_files import file_to_dict
from pattern_resolver import resolve_pattern

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
    paths = sys.argv[1:] #On recupere a partir de l'argument 1 entre dans la fonction, jusqu'a la fin
    for path in paths:
        document = file_to_dict(path)
        print("Creating folders for asset : " + document["asset"])
        create_folder(document)
