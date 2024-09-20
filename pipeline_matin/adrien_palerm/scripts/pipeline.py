import os

def get_pipeline_root():
    """
    Returns the root directory of the pipeline as a string
    """
    current_file = __file__
    parent_folder = os.path.split(current_file)[0]
    root_folder = os.path.split(parent_folder)[0]
    return root_folder

if __name__ == "__main__":
    print(get_pipeline_root())