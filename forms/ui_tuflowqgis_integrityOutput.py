# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tuflowqgis_integrityOutput.ui'
#
# Created: Thu Apr 26 14:36:52 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_integrityOutput(object):
    def setupUi(self, integrityOutput):
        integrityOutput.setObjectName(_fromUtf8("integrityOutput"))
        integrityOutput.resize(542, 678)
        self.buttonBox = QtGui.QDialogButtonBox(integrityOutput)
        self.buttonBox.setGeometry(QtCore.QRect(190, 640, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textBrowser = QtGui.QTextBrowser(integrityOutput)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 521, 621))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(integrityOutput)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), integrityOutput.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), integrityOutput.reject)
        QtCore.QMetaObject.connectSlotsByName(integrityOutput)

    def retranslateUi(self, integrityOutput):
        integrityOutput.setWindowTitle(_translate("integrityOutput", "1D Integrity Output", None))

