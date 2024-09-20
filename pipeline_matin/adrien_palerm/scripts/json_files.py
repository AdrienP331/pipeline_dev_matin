import json

def file_to_dict(path):
    """
    Reads the provided file and return it as a dictionary
    """
    with open(path, 'r') as file:
        content = file.read()
    dictionary = json.loads(content)
    return dictionary