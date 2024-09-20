
import os
from maya import cmds
from pattern_resolver import resolve_pattern
from documents import get_asset_document

def export_modeling():
    """
    Exports the selection to the proper directory
    """
    # Get current math
    current_path = cmds.file(q=True, sceneName=True)
    maya_file_name = os.path.split(current_path)[1]

    # Get asset document
    asset_name = maya_file_name.split("_")[0]
    asset_document = get_asset_document(asset_name)

    # Get version
    version = maya_file_name.split("_v", 1)[1] # should get something like "001_description.ma"
    version = version.split("_")[0].split(".")[0] # get rid of everything after the version

    # Add version to the document to resolve the path later on
    asset_document["version"] = version

    # Get export path
    pattern = "<project_root>/assets/<type>/<group>/<asset>/modeling/publish/v<version>/<asset>_v<version>.ma"
    export_path = resolve_pattern(pattern, asset_document)
    
    # Create export folder
    export_folder = os.path.split(export_path)[0]
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    
    # Export
    print(f"Exporting selection to {export_path}")
    cmds.file(
        export_path,
        force=True,
        type="mayaAscii",
        exportSelected=True
    )
