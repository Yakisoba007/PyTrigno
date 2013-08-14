'''
Created on 13.08.2013

@author: Genji
'''
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from runWidget_ui import Ui_Form

class RunWidget(QWidget):
    def __init__(self, parent=None):
        super(RunWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.session = None