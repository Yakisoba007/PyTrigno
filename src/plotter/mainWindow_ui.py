# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Mon Aug 12 15:24:37 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1049, 828)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainFrame = QtGui.QFrame(self.tab)
        self.mainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.horizontalLayout.addWidget(self.mainFrame)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1049, 21))
        self.menubar.setObjectName("menubar")
        self.menuDatei = QtGui.QMenu(self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dataView = QtGui.QTreeWidget(self.dockWidgetContents)
        self.dataView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.dataView.setObjectName("dataView")
        self.dataView.header().setVisible(False)
        self.verticalLayout.addWidget(self.dataView)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.menuDatei.addAction(self.actionLoad)
        self.menubar.addAction(self.menuDatei.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.actionLoad, QtCore.SIGNAL("activated()"), MainWindow.loadData)
        QtCore.QObject.connect(self.dataView, QtCore.SIGNAL("itemSelectionChanged()"), MainWindow.plotData)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Show Stored Data", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Stream Data", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDatei.setTitle(QtGui.QApplication.translate("MainWindow", "Datei", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Stored Data", None, QtGui.QApplication.UnicodeUTF8))
        self.dataView.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))

