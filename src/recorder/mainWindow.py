# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Wed Aug 14 13:05:37 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tbStart = QtGui.QToolButton(self.frame_2)
        self.tbStart.setEnabled(False)
        self.tbStart.setMaximumSize(QtCore.QSize(16777215, 19))
        self.tbStart.setObjectName("tbStart")
        self.horizontalLayout.addWidget(self.tbStart)
        self.tbTrigger = QtGui.QToolButton(self.frame_2)
        self.tbTrigger.setEnabled(False)
        self.tbTrigger.setMaximumSize(QtCore.QSize(16777215, 19))
        self.tbTrigger.setObjectName("tbTrigger")
        self.horizontalLayout.addWidget(self.tbTrigger)
        self.tbStop = QtGui.QToolButton(self.frame_2)
        self.tbStop.setEnabled(False)
        self.tbStop.setMaximumSize(QtCore.QSize(16777215, 19))
        self.tbStop.setObjectName("tbStop")
        self.horizontalLayout.addWidget(self.tbStop)
        self.elapsedTime = QtGui.QProgressBar(self.frame_2)
        self.elapsedTime.setMaximumSize(QtCore.QSize(16777215, 19))
        self.elapsedTime.setProperty("value", 0)
        self.elapsedTime.setTextVisible(True)
        self.elapsedTime.setInvertedAppearance(False)
        self.elapsedTime.setObjectName("elapsedTime")
        self.horizontalLayout.addWidget(self.elapsedTime)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuNew = QtGui.QMenu(self.menuBar)
        self.menuNew.setObjectName("menuNew")
        MainWindow.setMenuBar(self.menuBar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionServer = QtGui.QAction(MainWindow)
        self.actionServer.setObjectName("actionServer")
        self.menuNew.addAction(self.actionNew)
        self.menuNew.addAction(self.actionSave)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionServer)
        self.menuBar.addAction(self.menuNew.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL("activated()"), MainWindow.newSession)
        QtCore.QObject.connect(self.tbStart, QtCore.SIGNAL("clicked()"), MainWindow.startRun)
        QtCore.QObject.connect(self.tbStop, QtCore.SIGNAL("clicked()"), MainWindow.stop)
        QtCore.QObject.connect(self.tbTrigger, QtCore.SIGNAL("clicked()"), MainWindow.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tbStart.setText(QtGui.QApplication.translate("MainWindow", "start", None, QtGui.QApplication.UnicodeUTF8))
        self.tbStart.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.tbTrigger.setText(QtGui.QApplication.translate("MainWindow", "trigger", None, QtGui.QApplication.UnicodeUTF8))
        self.tbTrigger.setShortcut(QtGui.QApplication.translate("MainWindow", "T", None, QtGui.QApplication.UnicodeUTF8))
        self.tbStop.setText(QtGui.QApplication.translate("MainWindow", "stop", None, QtGui.QApplication.UnicodeUTF8))
        self.tbStop.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.elapsedTime.setFormat(QtGui.QApplication.translate("MainWindow", "%v", None, QtGui.QApplication.UnicodeUTF8))
        self.menuNew.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionServer.setText(QtGui.QApplication.translate("MainWindow", "Server", None, QtGui.QApplication.UnicodeUTF8))
