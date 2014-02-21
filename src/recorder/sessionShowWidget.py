from PySide.QtGui import QWidget
from sessionShowWidget_ui import Ui_Form

class sessionView(QWidget):
    '''
    widget to show session information
    '''
    
    
    def __init__(self, session, parent=None):
        super(sessionView, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.showName.setText(session.name)
        self.ui.showBemerkung.setPlainText(session.remarks)
        self.ui.showDir.setText(session.dir)
