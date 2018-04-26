# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tuflowqgis_tuplotAxisLabels.ui'
#
# Created: Tue Apr 24 17:53:12 2018
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

class Ui_tuplotAxisLabel(object):
    def setupUi(self, tuplotAxisLabel):
        tuplotAxisLabel.setObjectName(_fromUtf8("tuplotAxisLabel"))
        tuplotAxisLabel.resize(292, 225)
        self.buttonBox = QtGui.QDialogButtonBox(tuplotAxisLabel)
        self.buttonBox.setGeometry(QtCore.QRect(60, 190, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.xAxisLabel = QtGui.QLineEdit(tuplotAxisLabel)
        self.xAxisLabel.setGeometry(QtCore.QRect(10, 30, 271, 20))
        self.xAxisLabel.setObjectName(_fromUtf8("xAxisLabel"))
        self.label = QtGui.QLabel(tuplotAxisLabel)
        self.label.setGeometry(QtCore.QRect(20, 12, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(tuplotAxisLabel)
        self.label_2.setGeometry(QtCore.QRect(20, 52, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.yAxisLabel = QtGui.QLineEdit(tuplotAxisLabel)
        self.yAxisLabel.setGeometry(QtCore.QRect(10, 70, 271, 20))
        self.yAxisLabel.setObjectName(_fromUtf8("yAxisLabel"))
        self.label_3 = QtGui.QLabel(tuplotAxisLabel)
        self.label_3.setGeometry(QtCore.QRect(20, 106, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(tuplotAxisLabel)
        self.label_4.setGeometry(QtCore.QRect(20, 146, 121, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.x2AxisLabel = QtGui.QLineEdit(tuplotAxisLabel)
        self.x2AxisLabel.setGeometry(QtCore.QRect(10, 124, 271, 20))
        self.x2AxisLabel.setObjectName(_fromUtf8("x2AxisLabel"))
        self.y2AxisLabel = QtGui.QLineEdit(tuplotAxisLabel)
        self.y2AxisLabel.setGeometry(QtCore.QRect(10, 164, 271, 20))
        self.y2AxisLabel.setObjectName(_fromUtf8("y2AxisLabel"))

        self.retranslateUi(tuplotAxisLabel)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), tuplotAxisLabel.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), tuplotAxisLabel.reject)
        QtCore.QMetaObject.connectSlotsByName(tuplotAxisLabel)

    def retranslateUi(self, tuplotAxisLabel):
        tuplotAxisLabel.setWindowTitle(_translate("tuplotAxisLabel", "Tuplot - Axis Labels", None))
        self.label.setText(_translate("tuplotAxisLabel", "X Axis Label", None))
        self.label_2.setText(_translate("tuplotAxisLabel", "Y Axis Label", None))
        self.label_3.setText(_translate("tuplotAxisLabel", "Secondary X Axis Label", None))
        self.label_4.setText(_translate("tuplotAxisLabel", "Secondary Y Axis Label", None))

