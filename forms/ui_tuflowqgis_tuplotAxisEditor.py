# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tuflowqgis_tuplotAxisEditor.ui'
#
# Created: Mon Apr 23 17:58:39 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_tuplotAxisEditor(object):
    def setupUi(self, tuplotAxisEditor):
        tuplotAxisEditor.setObjectName(_fromUtf8("tuplotAxisEditor"))
        tuplotAxisEditor.resize(291, 196)
        self.buttonBox = QDialogButtonBox(tuplotAxisEditor)
        self.buttonBox.setGeometry(QtCore.QRect(50, 160, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QTabWidget(tuplotAxisEditor)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 291, 161))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.line = QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(140, 3, 20, 121))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.xAxisCustom_rb = QRadioButton(self.tab)
        self.xAxisCustom_rb.setGeometry(QtCore.QRect(20, 23, 121, 17))
        self.xAxisCustom_rb.setObjectName(_fromUtf8("xAxisCustom_rb"))
        self.buttonGroup = QButtonGroup(tuplotAxisEditor)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.xAxisCustom_rb)
        self.label_2 = QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(86, 78, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.xMin_sb = QDoubleSpinBox(self.tab)
        self.xMin_sb.setGeometry(QtCore.QRect(20, 46, 61, 22))
        self.xMin_sb.setMinimum(-99999.0)
        self.xMin_sb.setMaximum(99999.0)
        self.xMin_sb.setObjectName(_fromUtf8("xMin_sb"))
        self.yAxisAuto_rb = QRadioButton(self.tab)
        self.yAxisAuto_rb.setGeometry(QtCore.QRect(160, 3, 82, 17))
        self.yAxisAuto_rb.setChecked(True)
        self.yAxisAuto_rb.setObjectName(_fromUtf8("yAxisAuto_rb"))
        self.buttonGroup_2 = QButtonGroup(tuplotAxisEditor)
        self.buttonGroup_2.setObjectName(_fromUtf8("buttonGroup_2"))
        self.buttonGroup_2.addButton(self.yAxisAuto_rb)
        self.label_3 = QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(225, 79, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.xInc_sb = QDoubleSpinBox(self.tab)
        self.xInc_sb.setGeometry(QtCore.QRect(20, 106, 61, 22))
        self.xInc_sb.setMinimum(0.01)
        self.xInc_sb.setMaximum(99999.0)
        self.xInc_sb.setObjectName(_fromUtf8("xInc_sb"))
        self.xMax_sb = QDoubleSpinBox(self.tab)
        self.xMax_sb.setGeometry(QtCore.QRect(20, 76, 61, 22))
        self.xMax_sb.setMinimum(-99999.0)
        self.xMax_sb.setMaximum(99999.0)
        self.xMax_sb.setObjectName(_fromUtf8("xMax_sb"))
        self.label_5 = QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(86, 109, 61, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.yInc_sb = QDoubleSpinBox(self.tab)
        self.yInc_sb.setGeometry(QtCore.QRect(160, 106, 61, 22))
        self.yInc_sb.setMinimum(0.01)
        self.yInc_sb.setMaximum(99999.0)
        self.yInc_sb.setObjectName(_fromUtf8("yInc_sb"))
        self.label_4 = QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(225, 48, 61, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.xAxisAuto_rb = QRadioButton(self.tab)
        self.xAxisAuto_rb.setGeometry(QtCore.QRect(20, 3, 82, 17))
        self.xAxisAuto_rb.setChecked(True)
        self.xAxisAuto_rb.setObjectName(_fromUtf8("xAxisAuto_rb"))
        self.buttonGroup.addButton(self.xAxisAuto_rb)
        self.yMin_sb = QDoubleSpinBox(self.tab)
        self.yMin_sb.setGeometry(QtCore.QRect(160, 46, 61, 22))
        self.yMin_sb.setMinimum(-99999.0)
        self.yMin_sb.setMaximum(99999.0)
        self.yMin_sb.setObjectName(_fromUtf8("yMin_sb"))
        self.yMax_sb = QDoubleSpinBox(self.tab)
        self.yMax_sb.setGeometry(QtCore.QRect(160, 76, 61, 22))
        self.yMax_sb.setMinimum(-99999.0)
        self.yMax_sb.setMaximum(99999.0)
        self.yMax_sb.setObjectName(_fromUtf8("yMax_sb"))
        self.label = QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(86, 49, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_6 = QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(225, 110, 61, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.yAxisCustom_rb = QRadioButton(self.tab)
        self.yAxisCustom_rb.setGeometry(QtCore.QRect(160, 23, 121, 17))
        self.yAxisCustom_rb.setObjectName(_fromUtf8("yAxisCustom_rb"))
        self.buttonGroup_2.addButton(self.yAxisCustom_rb)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.line_2 = QFrame(self.tab_2)
        self.line_2.setGeometry(QtCore.QRect(140, 3, 20, 121))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(150, 0, 141, 141))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_12 = QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(75, 110, 61, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.yInc_sb_2 = QDoubleSpinBox(self.groupBox)
        self.yInc_sb_2.setGeometry(QtCore.QRect(10, 106, 61, 22))
        self.yInc_sb_2.setMinimum(0.01)
        self.yInc_sb_2.setMaximum(99999.0)
        self.yInc_sb_2.setObjectName(_fromUtf8("yInc_sb_2"))
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(75, 48, 61, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.yMin_sb_2 = QDoubleSpinBox(self.groupBox)
        self.yMin_sb_2.setGeometry(QtCore.QRect(10, 46, 61, 22))
        self.yMin_sb_2.setMinimum(-99999.0)
        self.yMin_sb_2.setMaximum(99999.0)
        self.yMin_sb_2.setObjectName(_fromUtf8("yMin_sb_2"))
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(75, 79, 61, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.yAxisAuto_rb_2 = QRadioButton(self.groupBox)
        self.yAxisAuto_rb_2.setGeometry(QtCore.QRect(10, 3, 82, 17))
        self.yAxisAuto_rb_2.setChecked(True)
        self.yAxisAuto_rb_2.setObjectName(_fromUtf8("yAxisAuto_rb_2"))
        self.buttonGroup_4 = QButtonGroup(tuplotAxisEditor)
        self.buttonGroup_4.setObjectName(_fromUtf8("buttonGroup_4"))
        self.buttonGroup_4.addButton(self.yAxisAuto_rb_2)
        self.yMax_sb_2 = QDoubleSpinBox(self.groupBox)
        self.yMax_sb_2.setGeometry(QtCore.QRect(10, 76, 61, 22))
        self.yMax_sb_2.setMinimum(-99999.0)
        self.yMax_sb_2.setMaximum(99999.0)
        self.yMax_sb_2.setObjectName(_fromUtf8("yMax_sb_2"))
        self.yAxisCustom_rb_2 = QRadioButton(self.groupBox)
        self.yAxisCustom_rb_2.setGeometry(QtCore.QRect(10, 23, 121, 17))
        self.yAxisCustom_rb_2.setObjectName(_fromUtf8("yAxisCustom_rb_2"))
        self.buttonGroup_4.addButton(self.yAxisCustom_rb_2)
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 151, 131))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.xMin_sb_2 = QDoubleSpinBox(self.groupBox_2)
        self.xMin_sb_2.setGeometry(QtCore.QRect(20, 46, 61, 22))
        self.xMin_sb_2.setMinimum(-99999.0)
        self.xMin_sb_2.setMaximum(99999.0)
        self.xMin_sb_2.setObjectName(_fromUtf8("xMin_sb_2"))
        self.xMax_sb_2 = QDoubleSpinBox(self.groupBox_2)
        self.xMax_sb_2.setGeometry(QtCore.QRect(20, 76, 61, 22))
        self.xMax_sb_2.setMinimum(-99999.0)
        self.xMax_sb_2.setMaximum(99999.0)
        self.xMax_sb_2.setObjectName(_fromUtf8("xMax_sb_2"))
        self.xAxisAuto_rb_2 = QRadioButton(self.groupBox_2)
        self.xAxisAuto_rb_2.setGeometry(QtCore.QRect(20, 3, 82, 17))
        self.xAxisAuto_rb_2.setChecked(True)
        self.xAxisAuto_rb_2.setObjectName(_fromUtf8("xAxisAuto_rb_2"))
        self.buttonGroup_3 = QButtonGroup(tuplotAxisEditor)
        self.buttonGroup_3.setObjectName(_fromUtf8("buttonGroup_3"))
        self.buttonGroup_3.addButton(self.xAxisAuto_rb_2)
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(86, 49, 61, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(86, 78, 61, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.xInc_sb_2 = QDoubleSpinBox(self.groupBox_2)
        self.xInc_sb_2.setGeometry(QtCore.QRect(20, 106, 61, 22))
        self.xInc_sb_2.setMinimum(0.01)
        self.xInc_sb_2.setMaximum(99999.0)
        self.xInc_sb_2.setObjectName(_fromUtf8("xInc_sb_2"))
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(86, 109, 61, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.xAxisCustom_rb_2 = QRadioButton(self.groupBox_2)
        self.xAxisCustom_rb_2.setGeometry(QtCore.QRect(20, 23, 121, 17))
        self.xAxisCustom_rb_2.setObjectName(_fromUtf8("xAxisCustom_rb_2"))
        self.buttonGroup_3.addButton(self.xAxisCustom_rb_2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(tuplotAxisEditor)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(tuplotAxisEditor.accept)
        self.buttonBox.rejected.connect(tuplotAxisEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(tuplotAxisEditor)

    def retranslateUi(self, tuplotAxisEditor):
        tuplotAxisEditor.setWindowTitle(_translate("tuplotAxisEditor", "Tuplot", None))
        self.xAxisCustom_rb.setText(_translate("tuplotAxisEditor", "Custom X Axis Limits", None))
        self.label_2.setText(_translate("tuplotAxisEditor", "X Maximum", None))
        self.yAxisAuto_rb.setText(_translate("tuplotAxisEditor", "Auto Y Axis", None))
        self.label_3.setText(_translate("tuplotAxisEditor", "Y Maximum", None))
        self.label_5.setText(_translate("tuplotAxisEditor", "X Increment", None))
        self.label_4.setText(_translate("tuplotAxisEditor", "Y Minimum", None))
        self.xAxisAuto_rb.setText(_translate("tuplotAxisEditor", "Auto X Axis", None))
        self.label.setText(_translate("tuplotAxisEditor", "X Minimum", None))
        self.label_6.setText(_translate("tuplotAxisEditor", "Y Increment", None))
        self.yAxisCustom_rb.setText(_translate("tuplotAxisEditor", "Custom Y Axis Limits", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("tuplotAxisEditor", "Primary Axis", None))
        self.label_12.setText(_translate("tuplotAxisEditor", "Y Increment", None))
        self.label_10.setText(_translate("tuplotAxisEditor", "Y Minimum", None))
        self.label_8.setText(_translate("tuplotAxisEditor", "Y Maximum", None))
        self.yAxisAuto_rb_2.setText(_translate("tuplotAxisEditor", "Auto Y Axis", None))
        self.yAxisCustom_rb_2.setText(_translate("tuplotAxisEditor", "Custom Y Axis Limits", None))
        self.xAxisAuto_rb_2.setText(_translate("tuplotAxisEditor", "Auto X Axis", None))
        self.label_11.setText(_translate("tuplotAxisEditor", "X Minimum", None))
        self.label_7.setText(_translate("tuplotAxisEditor", "X Maximum", None))
        self.label_9.setText(_translate("tuplotAxisEditor", "X Increment", None))
        self.xAxisCustom_rb_2.setText(_translate("tuplotAxisEditor", "Custom X Axis Limits", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("tuplotAxisEditor", "Secondary Axis", None))

