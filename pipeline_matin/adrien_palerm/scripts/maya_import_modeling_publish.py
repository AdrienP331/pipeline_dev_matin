
from glob import glob
from maya import cmds
from maya_drop_document_dialog import DocumentDropDialog
from pattern_resolver import resolve_pattern

class ImportModelingPublishDialog(DocumentDropDialog):
    """
    This class is a child class of DocumentDropDialog, with a different
    window title and a different "process_document" method
    """
    # Set a few attributes that drive the behavior of the class
    close_when_done = False
    title = "Import Modeling Publish"

    def process_document(self, document):
        """
        Main method of the class, that processes each document dropped on the dialog
        Looks for the latest published file, and imports it as a reference
        """
        # Get search pattern
        pattern = "<project_root>/assets/<type>/<group>/<asset>/modeling/publish/v*/<asset>_v*.ma"
        search = resolve_pattern(pattern, document)

        # Look for paths that match the search pattern
        print(f"Looking for files matching the pattern : {search}")
        paths = glob(search)
        if paths:
            # Get last version
            last_path = sorted(paths)[-1]

            # Import it
            cmds.file(
                last_path,
                reference=True,
                namespace=document["asset"] + "_ref"
            )
        
        # Display an error popup if no file was found
        else:
            title = "Warning"
            message = f"No publish found for asset : {document['asset']}"
            buttons = ["OK"]
            cmds.confirmDialog(t=title, m=message, b=buttons)