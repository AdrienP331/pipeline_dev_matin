
from PySide2 import QtWidgets, QtCore
from json_files import file_to_dict

class DocumentDropDialog(QtWidgets.QDialog):
    """
    This is the parent class for a maya widget in which the user
    can drag and drop json documents.

    To use it, just create a class than inheritates from DocumentDropDialog,
    set the "close_when_done" and "title" attributes, and define the "process_document"
    function.

    A good example of this can be found in the module maya_import_modeling_publish

    Here is how to open the widget in maya :
    
        import maya_drop_document_dialog
        maya_drop_document_dialog.DocumentDropDialog.show_dialog()
    """
    # Set a few attributes that drive the behavior of the class
    close_when_done = True
    title = "Drop Document Here"

    def __init__(self, parent=None):
        """
        If you are unfamiliar to classes, don't pay too much attention about
        what is going on here.
        Basically, it is the function that is called when creating an instance of our widget.
        """
        # Initialize QDialog
        super(DocumentDropDialog, self).__init__(parent)

        # Set window title
        self.setWindowTitle(self.title)

        # Set window size
        self.setFixedHeight(100)
        self.setFixedWidth(200)

        # Add some text to the widget
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Drag and drop document(s) here", self)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size:14px; font-weight:bold")
        layout.addWidget(self.label)

        # Make it so file can be drag-n-dropped onto the widget
        # It will automatically make use of the methods dragEnterEvent and dropEvent
        self.setAcceptDrops(True)
        

    def dragEnterEvent(self, event):
        """
        This function defines the behavior of the widget when files are passed
        over the widget
        """
        # Check if the dropped data contains files
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Check if all provided files are json files
            if all(url.toLocalFile().endswith('.json') for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event):
        """
        This function defines the behavior of the widget when files are dropped
        on the widget
        """
        # Get paths
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()

            # Check if file is a json file
            if file_path.endswith('.json'):
                # Read document
                document = file_to_dict(file_path)

                # Run the main function
                self.process_document(document)

        # close the dialog, if the close_when_done attribute was set to True
        if self.close_when_done:
            self.deleteLater()

    def process_document(self, document):
        """
        Main method of the class, that processes each document dropped on the dialog.
        It should be replaced in a derived class, so it actually does something
        """
        print(document)

    @classmethod
    def show_dialog(cls):
        dialog = cls()
        dialog.exec_()
