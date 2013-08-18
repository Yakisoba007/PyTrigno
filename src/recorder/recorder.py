'''
Created on 13.08.2013

@author: Genji
'''
import sys
from PySide.QtCore import *
from PySide.QtGui import *
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

class Recorder(QMainWindow):
    def __init__(self, parent=None):
        super(Recorder, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.session = None
        self.server = DelsysStation(parent=self)
        
        self.ui.dockWidget.setWidget(QWidget())
        
        self.dockLayout = QGridLayout(self.ui.dockWidget.widget())
        self.showSessionMeta = None
        self.showRunMeta = None
        self.plotWidget = None
        self.plots = []
        self.startTime = datetime.now()
        
        self.pinger = QTimer(self)
        self.runPinger = QTimer(self)
        
        self.runPinger.setSingleShot(True)
        self.runPinger.timeout.connect(self.stop)
        self.pinger.timeout.connect(self.ping)
        self.kinectRecorder=None
        self.newpath=None
        
    def clearDock(self):
        if self.showSessionMeta is not None:
            reply = QMessageBox.question(self, 'QMessageBox.question()',
                                         'Do you want to first save the current session?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                print("save")
            elif reply == QMessageBox.Cancel:
                return 
            
            self.session = None
            self.dockLayout.removeWidget(self.showSessionMeta)
            self.dockLayout.removeWidget(self.showRunMeta)
            self.showSessionMeta = None
            self.showRunMeta = None
            self.kinectRecorder.killRecorder()
            
    def preparePlots(self):
        if self.ui.frame.layout() is None:
            layout = QGridLayout()
            self.ui.frame.setLayout(layout)
        else:
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
        
    def newSession(self):
        self.clearDock()
        sessionDialog = SessionDialog(self)
        if sessionDialog.exec_():
            self.newpath = sessionDialog.ui.leDir.text()+'\\'+sessionDialog.ui.leName.text()
            if not os.path.isdir(self.newpath):
                os.makedirs(self.newpath)
            else:
                print('reusing folder')
                QMessageBox.information(self, 'Warning!', '''You\'re reusing the subject folder''',
            QMessageBox.Ok)
            self.session = Session(sessionDialog.ui.leName.text(),
                                   sessionDialog.ui.teBemerkung.toHtml(),
                                   sessionDialog.ui.leDir.text()+'\\'+sessionDialog.ui.leName.text())
            self.showSessionMeta = sessionView(self.session, self)
            self.showRunMeta = RunWidget()
            self.showRunMeta.ui.leCurrentRun.setText(str(len(self.session.runs)))
            self.kinectRecorder=KinectRecorder()
            self.dockLayout.addWidget(self.showSessionMeta)
            self.dockLayout.addWidget(self.showRunMeta)
            self.showRunMeta.show()
            self.showSessionMeta.show()
            self.preparePlots()
            self.ui.tbStart.setEnabled(True)
    
    def startRun(self):
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
            duration = self.showRunMeta.ui.timeEdit.time()
            d = duration.second() + duration.minute()*60
            
            self.runPinger.start(d*1000)
            self.pinger.start()
            
            self.ui.tbStop.setEnabled(True)
            self.ui.tbTrigger.setEnabled(True)
            self.ui.tbStart.setEnabled(False)
            
            name = self.showRunMeta.ui.leCurrentRun.text()
            self.session.addRun(name)
            self.kinectRecorder.startRecording(self.newpath+'\\'+name+'.oni')            
            self.ui.elapsedTime.setRange(0,d)


    
    def stop(self):
        self.ui.tbStop.setEnabled(False)
        self.ui.tbTrigger.setEnabled(False)
        self.ui.tbStart.setEnabled(True)
        self.ui.elapsedTime.setValue(0)
        
        self.showRunMeta.ui.leCurrentRun.setText(str(len(self.session.runs)))
        self.server.exitFlag = True
        self.server.stop()

        self.runPinger.stop()
        self.pinger.stop()
        
        self.session.stopRun(self.server.buffer)
        self.server.buffer = None
        self.kinectRecorder.stopRecording()
        
    def trigger(self):
        print("trigger")
        trigger = self.server.buffer.shape[1]
        self.session.addTrigger(trigger)
        
    def ping(self):
        elapsed = int((datetime.now()-self.startTime).total_seconds())
        self.ui.elapsedTime.setValue(elapsed)
        
        for p in range(len(self.plots)):
            if self.server.buffer is None:
                return
            if self.server.buffer.shape[1] < 5000:
                self.plots[p].plot(self.server.buffer[p], clear=True)
            else:
                self.plots[p].plot(self.server.buffer[p,-5000:], clear=True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mySW = Recorder()
    mySW.show()
    sys.exit(app.exec_())