import sys
from PySide.QtCore import QTimer
from PySide.QtGui import (QMainWindow, QWidget, QGridLayout,
                          QMessageBox, QInputDialog, QListWidgetItem,
                          QApplication)
from mainWindow import Ui_MainWindow
from sessionDialog import SessionDialog
from session import Session
from sessionShowWidget import sessionView
from runWidget import RunWidget
from utils.server import DelsysStation

from datetime import datetime
import pyqtgraph as pg

import numpy as np
import socket
import os
from kinectRecorder import KinectRecorder
from plotter.plotter import Plotter

class Recorder(QMainWindow):
    '''Main Window
     - menu toolbar to load and save session, open plotter and set server
     - dock widget holding session and run information
     - grid plot to stream current emg data of 16 channels
     - start, stop, progressbar and trigger for current run
    '''
    
    
    def __init__(self, parent=None):
        super(Recorder, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.plotter = None
        self.session = None
        self.server = DelsysStation(parent=self)
        
        self.ui.dockWidget.setWidget(QWidget())
        
        self.dockLayout = QGridLayout(self.ui.dockWidget.widget())
        self.showSessionMeta = None
        self.showRunMeta = None
        self.plotWidget = None
        self.plots = []
        self.startTime = datetime.now()
        
        self.pinger = QTimer(self) # timer to read data from server whenever available
        self.runPinger = QTimer(self) # timer to call stop when run duration times out
        
        self.runPinger.setSingleShot(True)
        self.runPinger.timeout.connect(self.stop)
        self.pinger.timeout.connect(self.ping)
        self.kinectRecorder=None
        self.newpath=None
        self.notSavedState = False
        
    def clearDock(self):
        ''' clear session (dock widget elements)
        - remove showSessionMeta
        - remove showRunMeta
        - kill kinectRecorder
        - remove session
        
        if changes are not saved, ask
        '''
        if self.showSessionMeta is not None:
            reply = QMessageBox.question(self, 'QMessageBox.question()',
                                         'Do you want to first save the current session?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save()
            elif reply == QMessageBox.Cancel:
                return 
            
            self.session = None
            self.dockLayout.removeWidget(self.showSessionMeta)
            self.dockLayout.removeWidget(self.showRunMeta)
            self.showSessionMeta.deleteLater()
            self.showRunMeta.deleteLater()
            self.showSessionMeta = None
            self.showRunMeta = None
            self.kinectRecorder.killRecorder()
            
    def preparePlots(self):
        '''arange 2x8 plots for each channel and
        set parameters
        '''
        if self.ui.frame.layout() is None:
            layout = QGridLayout()
            self.ui.frame.setLayout(layout)
        else:
            #########
            # reset #
            #########
            layout = self.ui.frame.layout()
            layout.removeWidget(self.plotWidget)
            self.plotWidget = None
            self.plots = []
        self.plotWidget = pg.GraphicsLayoutWidget(border=(100,100,100))
        layout.addWidget(self.plotWidget)
        
        for i in range(8):
            for k in range(2):
                self.plots.append(self.plotWidget.addPlot(title="EMG " + str(k+2*i+1)))
                self.plots[-1].plot(np.linspace(0,2,1000))
                self.plots[-1].setYRange(-0.0002, 0.0002)
            self.plotWidget.nextRow()
        
        self.plotWidget.show()
        
    def setServer(self):
        ''' open dialog to set server address
        e.g. localhost, 192.168.1.5
        '''
        text, ok = QInputDialog.getText(self, "Set server",
                'Enter server adress')
        if ok:
            self.server.host = text
            
    def newSession(self):
        ''' create new session:
        - clear dock
        - open dialog to set session parameters
        - create showSessionMeta, showRunMeta, kinectRecorder
        '''
        self.clearDock()
        
        sessionDialog = SessionDialog(self)
        if sessionDialog.exec_():
            newpath = os.path.join(sessionDialog.ui.leDir.text(), sessionDialog.ui.leName.text()) 
            if not os.path.isdir(newpath):
                os.makedirs(newpath)
            else:
                print('reusing folder')
                QMessageBox.information(self, 'Warning!', '''You\'re reusing the subject folder''',
            QMessageBox.Ok)
                
            self.session = Session(sessionDialog.ui.leName.text(),
                                   sessionDialog.ui.teBemerkung.toPlainText(),
                                   newpath)
            self.showSessionMeta = sessionView(self.session, self)
            self.showRunMeta = RunWidget(self)
            self.showRunMeta.ui.leCurrentRun.setText(str(len(self.session.runs)))
            
            try:
                self.kinectRecorder=KinectRecorder()
            except:
                print "no Kinect recording"
                self.kinectRecorder = None
                                        
            self.showSessionMeta.ui.showBemerkung.textChanged.connect(self.pendingSave)
            self.showRunMeta.ui.lwRuns.itemDoubleClicked.connect(self.openPlotter)
            self.dockLayout.addWidget(self.showSessionMeta)
            self.dockLayout.addWidget(self.showRunMeta)
            
            self.showRunMeta.show()
            self.showSessionMeta.show()
            self.preparePlots()
            self.ui.tbStart.setEnabled(True)
    
    def pendingSave(self):
        self.notSavedState = True
        self.setWindowTitle("PyTrigno(*)")
        
    def save(self):
        self.notSavedState = False
        self.setWindowTitle("PyTrigno")
        self.session.remarks = self.showSessionMeta.ui.showBemerkung.toPlainText()
        self.session.dump("ReadMe.txt")
        
    def startRun(self):
        ''' start a recording:
         - setup server
         - setup timer (if no eternity is toggled)
         - setup progress bar
         - setup buttons
         - setup session
         - start recorder
        '''
        #setup server
        self.server.exitFlag = False
        try:
            self.startTime = datetime.now()
            self.server.start()
        except:
            print("something went wrong")
            self.server.exitFlag = True
            raise socket.timeout("Could not connect to Delsys Station")
        else:
            if self.showRunMeta.ui.cbEternity.checkState() == 0:
                duration = self.showRunMeta.ui.timeEdit.time()
                d = duration.second() + duration.minute()*60
                
                self.runPinger.start(d*1000)
                self.ui.elapsedTime.setRange(0,d)
            elif self.showRunMeta.ui.cbEternity.checkState() == 2:
                self.ui.elapsedTime.setRange(0,0)
            
            self.pinger.start()
            
            self.ui.tbStop.setEnabled(True)
            self.ui.tbTrigger.setEnabled(True)
            self.ui.tbStart.setEnabled(False)
            
            name = self.showRunMeta.ui.leCurrentRun.text()
            self.session.addRun(name)
            if self.kinectRecorder is not None:
                self.kinectRecorder.startRecording(self.newpath+'\\'+name+'.oni')            
            self.ui.elapsedTime.setRange(0,d)
    
    def stop(self):
        ''' stop recording due to button press or timeout
        - setup buttons
        - stop timers
        - stop server
        - kill kinectRecorder
        - add item to list of runs
        '''
        self.ui.tbStop.setEnabled(False)
        self.ui.tbTrigger.setEnabled(False)
        self.ui.tbStart.setEnabled(True)
        self.ui.elapsedTime.reset()
        
        QListWidgetItem(self.showRunMeta.ui.leCurrentRun.text(),
                        self.showRunMeta.ui.lwRuns)
        
        self.showRunMeta.ui.leCurrentRun.setText(str(len(self.session.runs)))
        self.server.exitFlag = True
        self.server.stop()

        self.runPinger.stop()
        self.pinger.stop()
        
        self.session.stopRun(self.server.buffer)
        self.server.buffer = None
        if self.kinectRecorder is not None:
            self.kinectRecorder.stopRecording()
        self.server.flush()
        
    def trigger(self):
        ''' add a trigger '''
        print("trigger")
        trigger = self.server.buffer[0].shape[1]
        self.session.addTrigger(trigger)
        
    def ping(self):
        ''' update progress bar and plots everytime
        new data is available 
        '''
        elapsed = int((datetime.now()-self.startTime).total_seconds())
        self.ui.elapsedTime.setValue(elapsed)
        
        for p in range(len(self.plots)):
            if self.server.buffer[0].shape[1] < 5000:
                self.plots[p].plot(self.server.buffer[0][p], clear=True)
            else:
                self.plots[p].plot(self.server.buffer[0][p,-5000:], clear=True)
    
    def openPlotter(self, item=None):
        if self.plotter is None:
            self.plotter = Plotter()
        if item is not None:
            self.plotter.load([os.path.join(self.session.dir, item.text()) + ".pk"])
        self.plotter.show()
        
    def closeEvent(self, event):
        if self.notSavedState:
            reply = QMessageBox.question(self, 'QMessageBox.question()',
                                            'Do you want to first save the current session?',
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        else:
            reply = QMessageBox.No

        if reply == QMessageBox.Yes:
            self.save()
        elif reply == QMessageBox.Cancel:
            event.ignore()
            return
      
        if not self.server.exitFlag:
            self.stop()
        event.accept()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mySW = Recorder()
    mySW.show()
    sys.exit(app.exec_())
