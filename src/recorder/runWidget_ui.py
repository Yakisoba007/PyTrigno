# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'runWidget.ui'
#
# Created: Mon Aug 19 15:45:04 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 421)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.lwRuns = QtGui.QListWidget(Form)
        self.lwRuns.setObjectName("lwRuns")
        self.gridLayout.addWidget(self.lwRuns, 0, 0, 1, 3)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.leCurrentRun = QtGui.QLineEdit(Form)
        self.leCurrentRun.setObjectName("leCurrentRun")
        self.gridLayout.addWidget(self.leCurrentRun, 1, 1, 1, 2)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.timeEdit = QtGui.QTimeEdit(Form)
        self.timeEdit.setMaximumTime(QtCore.QTime(0, 2, 59))
        self.timeEdit.setMinimumTime(QtCore.QTime(0, 0, 10))
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout.addWidget(self.timeEdit, 2, 1, 1, 1)
        self.cbEternity = QtGui.QCheckBox(Form)
        self.cbEternity.setObjectName("cbEternity")
        self.gridLayout.addWidget(self.cbEternity, 2, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.cbEternity, QtCore.SIGNAL("stateChanged(int)"), Form.toggleEternity)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Run Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Run Time [m:ss]", None, QtGui.QApplication.UnicodeUTF8))
        self.timeEdit.setDisplayFormat(QtGui.QApplication.translate("Form", "m:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEternity.setText(QtGui.QApplication.translate("Form", "eternity", None, QtGui.QApplication.UnicodeUTF8))

