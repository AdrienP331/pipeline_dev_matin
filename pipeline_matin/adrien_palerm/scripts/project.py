from settings import get_settings

def get_project_root():
    """Returns the root of the project as a string"""
    settings = get_settings()
    return settings["project_root"]

if __name__ == "__main__":
    print(get_project_root())