# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tuflowqgis_check1dIntegrity.ui'
#
# Created: Wed Apr 25 18:35:44 2018
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

class Ui_check1dIntegrity(object):
    def setupUi(self, check1dIntegrity):
        check1dIntegrity.setObjectName(_fromUtf8("check1dIntegrity"))
        check1dIntegrity.resize(428, 495)
        self.buttonBox = QtGui.QDialogButtonBox(check1dIntegrity)
        self.buttonBox.setGeometry(QtCore.QRect(210, 460, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(check1dIntegrity)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(check1dIntegrity)
        self.label_2.setGeometry(QtCore.QRect(10, 135, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox.setGeometry(QtCore.QRect(10, 260, 401, 61))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.check1dPoint_cb = QtGui.QCheckBox(self.groupBox)
        self.check1dPoint_cb.setGeometry(QtCore.QRect(200, 20, 221, 20))
        self.check1dPoint_cb.setObjectName(_fromUtf8("check1dPoint_cb"))
        self.check1dLine_cb = QtGui.QCheckBox(self.groupBox)
        self.check1dLine_cb.setGeometry(QtCore.QRect(10, 20, 181, 20))
        self.check1dLine_cb.setObjectName(_fromUtf8("check1dLine_cb"))
        self.groupBox_2 = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 331, 401, 121))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.outSel_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outSel_cb.setGeometry(QtCore.QRect(200, 20, 151, 20))
        self.outSel_cb.setObjectName(_fromUtf8("outSel_cb"))
        self.outMessBox_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outMessBox_cb.setGeometry(QtCore.QRect(10, 20, 171, 20))
        self.outMessBox_cb.setObjectName(_fromUtf8("outMessBox_cb"))
        self.outTxtFile_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outTxtFile_cb.setGeometry(QtCore.QRect(10, 50, 221, 20))
        self.outTxtFile_cb.setObjectName(_fromUtf8("outTxtFile_cb"))
        self.outFile = QtGui.QLineEdit(self.groupBox_2)
        self.outFile.setEnabled(False)
        self.outFile.setGeometry(QtCore.QRect(10, 80, 311, 22))
        self.outFile.setObjectName(_fromUtf8("outFile"))
        self.browse_button = QtGui.QPushButton(self.groupBox_2)
        self.browse_button.setEnabled(False)
        self.browse_button.setGeometry(QtCore.QRect(326, 76, 71, 28))
        self.browse_button.setObjectName(_fromUtf8("browse_button"))
        self.addLine_combo = QtGui.QComboBox(check1dIntegrity)
        self.addLine_combo.setGeometry(QtCore.QRect(10, 30, 321, 22))
        self.addLine_combo.setObjectName(_fromUtf8("addLine_combo"))
        self.addLine_button = QtGui.QPushButton(check1dIntegrity)
        self.addLine_button.setGeometry(QtCore.QRect(340, 26, 71, 28))
        self.addLine_button.setObjectName(_fromUtf8("addLine_button"))
        self.addPoint_button = QtGui.QPushButton(check1dIntegrity)
        self.addPoint_button.setGeometry(QtCore.QRect(340, 150, 71, 28))
        self.addPoint_button.setObjectName(_fromUtf8("addPoint_button"))
        self.addPoint_combo = QtGui.QComboBox(check1dIntegrity)
        self.addPoint_combo.setGeometry(QtCore.QRect(10, 153, 321, 22))
        self.addPoint_combo.setObjectName(_fromUtf8("addPoint_combo"))
        self.lineLyrs_lw = QtGui.QListWidget(check1dIntegrity)
        self.lineLyrs_lw.setGeometry(QtCore.QRect(10, 60, 401, 71))
        self.lineLyrs_lw.setObjectName(_fromUtf8("lineLyrs_lw"))
        self.pointLyrs_lw = QtGui.QListWidget(check1dIntegrity)
        self.pointLyrs_lw.setGeometry(QtCore.QRect(10, 183, 401, 71))
        self.pointLyrs_lw.setObjectName(_fromUtf8("pointLyrs_lw"))

        self.retranslateUi(check1dIntegrity)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), check1dIntegrity.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), check1dIntegrity.reject)
        QtCore.QMetaObject.connectSlotsByName(check1dIntegrity)

    def retranslateUi(self, check1dIntegrity):
        check1dIntegrity.setWindowTitle(_translate("check1dIntegrity", "Check 1D Network Integrity", None))
        self.label.setText(_translate("check1dIntegrity", "1D network Line Layer", None))
        self.label_2.setText(_translate("check1dIntegrity", "1D network Point Layer", None))
        self.groupBox.setTitle(_translate("check1dIntegrity", "Check Options", None))
        self.check1dPoint_cb.setText(_translate("check1dIntegrity", "Check 1D point-Line snapping", None))
        self.check1dLine_cb.setText(_translate("check1dIntegrity", "Check 1D line-line snapping", None))
        self.groupBox_2.setTitle(_translate("check1dIntegrity", "Output Options", None))
        self.outSel_cb.setText(_translate("check1dIntegrity", "Output as selection", None))
        self.outMessBox_cb.setText(_translate("check1dIntegrity", "Output to message box", None))
        self.outTxtFile_cb.setText(_translate("check1dIntegrity", "Output to txt file", None))
        self.browse_button.setText(_translate("check1dIntegrity", "Browse", None))
        self.addLine_button.setText(_translate("check1dIntegrity", "Add", None))
        self.addPoint_button.setText(_translate("check1dIntegrity", "Add", None))

