from project import get_project_root

def resolve_pattern(pattern, document):
    """
    Resolves the provided pattern with the provided document
    For instance, a pattern can look like this :
      "<project_root>/assets/<type>/<group>/<asset>/modeling/work"

    It may also include the "*" character, used to search files with the glob() function
    For instance :
      "<project_root>/assets/<type>/<group>/<asset>/modeling/work/<asset>_v*_*.ma"
    """
    # Replace root project
    project_root = get_project_root()
    pattern = pattern.replace("<project_root>", project_root)

    # Replace fields related to the asset
    for key, value in document.items():
        to_replace = "<" + key + ">"
        pattern = pattern.replace(to_replace, value)
    
    # Raise an error if the path couldn't be fully resolved
    if "<" in pattern:
        raise Exception(f"Failed to fully resolve the pattern : {pattern}")
    
    return pattern