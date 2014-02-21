from PySide.QtGui import QWidget
from runWidget_ui import Ui_Form

class RunWidget(QWidget):
    ''' widget containing information about current run
     - list of all previous runs
     - list item can be double clicked to open it in plotter
     - edit time interval to set recording length
     - manual stop checkbox 
    '''
    
    
    def __init__(self, parent=None):
        super(RunWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.session = None
        
    def toggleEternity(self, i):
        ''' if eternity, choosig time interval is not available '''
        if i == 0:
            self.ui.timeEdit.setEnabled(True)
        elif i== 2:
            self.ui.timeEdit.setDisabled(True)
