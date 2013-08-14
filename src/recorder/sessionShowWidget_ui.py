# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sessionShowWidget.ui'
#
# Created: Tue Aug 13 11:04:43 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(285, 254)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.showName = QtGui.QTextBrowser(Form)
        self.showName.setMaximumSize(QtCore.QSize(16777215, 20))
        self.showName.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.showName.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.showName.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.showName.setOpenLinks(False)
        self.showName.setObjectName("showName")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.showName)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.showBemerkung = QtGui.QTextBrowser(Form)
        self.showBemerkung.setObjectName("showBemerkung")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.showBemerkung)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.showDir = QtGui.QTextBrowser(Form)
        self.showDir.setMaximumSize(QtCore.QSize(16777215, 20))
        self.showDir.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.showDir.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.showDir.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.showDir.setOpenLinks(False)
        self.showDir.setObjectName("showDir")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.showDir)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.showName.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Bemerkung: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Speicherort: ", None, QtGui.QApplication.UnicodeUTF8))

