# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sessionDialog.ui'
#
# Created: Mon Aug 19 14:10:52 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(351, 227)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.leName = QtGui.QLineEdit(Dialog)
        self.leName.setObjectName("leName")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.leName)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.teBemerkung = QtGui.QTextEdit(Dialog)
        self.teBemerkung.setObjectName("teBemerkung")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.teBemerkung)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leDir = QtGui.QLineEdit(Dialog)
        self.leDir.setObjectName("leDir")
        self.horizontalLayout.addWidget(self.leDir)
        self.pbChooseDir = QtGui.QPushButton(Dialog)
        self.pbChooseDir.setMaximumSize(QtCore.QSize(20, 20))
        self.pbChooseDir.setObjectName("pbChooseDir")
        self.horizontalLayout.addWidget(self.pbChooseDir)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.check)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QObject.connect(self.pbChooseDir, QtCore.SIGNAL("clicked()"), Dialog.changeDir)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Bemerkung:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Speicherort:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbChooseDir.setText(QtGui.QApplication.translate("Dialog", "..", None, QtGui.QApplication.UnicodeUTF8))

