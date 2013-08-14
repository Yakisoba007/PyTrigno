'''
Created on 13.08.2013

@author: Genji
'''
from PySide.QtCore import *
from PySide.QtGui import *
from sessionDialog_ui import Ui_Dialog
import os

class SessionDialog(QDialog):
    def __init__(self, parent=None):
        super(SessionDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def check(self):
        if len(self.ui.leName.text().strip()) < 1:
            print "Name must be filled"
        elif not os.path.isdir(self.ui.leDir.text()):
            print "need an existing dir"
        else:
            self.accept()
    
    def changeDir(self):
        d = QFileDialog.getExistingDirectory(self, "Open Directory",
                                             os.getcwd(), QFileDialog.ShowDirsOnly)
        self.ui.leDir.setText(d)