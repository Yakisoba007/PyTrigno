from PySide.QtGui import QDialog, QFileDialog
from sessionDialog_ui import Ui_Dialog
import os

class SessionDialog(QDialog):
    '''
    dialog box for creating a new session
    '''
    
    
    def __init__(self, parent=None):
        super(SessionDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def check(self):
        if len(self.ui.leName.text().strip()) < 1:
            print("Name must be filled")
        elif not os.path.isdir(self.ui.leDir.text()):
            print("need an existing dir")
        else:
            self.accept()
    
    def changeDir(self):
        d = QFileDialog.getExistingDirectory(self, "Open Directory",
                                             'C:\\PatientData', QFileDialog.ShowDirsOnly)
        self.ui.leDir.setText(d)