'''
Created on 13.08.2013

@author: Genji
'''
import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *
from sessionShowWidget_ui import Ui_Form

class sessionView(QWidget):
    def __init__(self, session, parent=None):
        super(sessionView, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.showName.setText(session.name)
        self.ui.showBemerkung.setPlainText(session.remarks)
        self.ui.showDir.setText(session.dir)
