# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tuflowqgis_check1dIntegrity.ui'
#
# Created: Mon May 28 17:12:29 2018
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
        self.check1dIntegrity = check1dIntegrity
        check1dIntegrity.setObjectName(_fromUtf8("check1dIntegrity"))
        check1dIntegrity.resize(701, 819)
        check1dIntegrity.setFocusPolicy(QtCore.Qt.NoFocus)
        check1dIntegrity.setModal(False)
        self.buttonBox = QtGui.QDialogButtonBox(check1dIntegrity)
        self.buttonBox.setGeometry(QtCore.QRect(530, 783, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(check1dIntegrity)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(check1dIntegrity)
        self.label_2.setGeometry(QtCore.QRect(10, 135, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox_2 = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 700, 391, 101))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.outSel_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outSel_cb.setGeometry(QtCore.QRect(169, 17, 151, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.outSel_cb.setFont(font)
        self.outSel_cb.setObjectName(_fromUtf8("outSel_cb"))
        self.outMessBox_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outMessBox_cb.setGeometry(QtCore.QRect(7, 17, 161, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.outMessBox_cb.setFont(font)
        self.outMessBox_cb.setObjectName(_fromUtf8("outMessBox_cb"))
        self.outPLayer_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outPLayer_cb.setGeometry(QtCore.QRect(169, 36, 231, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.outPLayer_cb.setFont(font)
        self.outPLayer_cb.setObjectName(_fromUtf8("outPLayer_cb"))
        self.outFile = QtGui.QLineEdit(self.groupBox_2)
        self.outFile.setEnabled(False)
        self.outFile.setGeometry(QtCore.QRect(10, 59, 291, 22))
        self.outFile.setObjectName(_fromUtf8("outFile"))
        self.outTxtFile_cb = QtGui.QCheckBox(self.groupBox_2)
        self.outTxtFile_cb.setGeometry(QtCore.QRect(7, 38, 151, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.outTxtFile_cb.setFont(font)
        self.outTxtFile_cb.setObjectName(_fromUtf8("outTxtFile_cb"))
        self.browse_button = QtGui.QPushButton(self.groupBox_2)
        self.browse_button.setEnabled(False)
        self.browse_button.setGeometry(QtCore.QRect(310, 60, 71, 21))
        self.browse_button.setObjectName(_fromUtf8("browse_button"))
        self.addLine_combo = QtGui.QComboBox(check1dIntegrity)
        self.addLine_combo.setGeometry(QtCore.QRect(10, 30, 541, 22))
        self.addLine_combo.setObjectName(_fromUtf8("addLine_combo"))
        self.addLine_button = QtGui.QPushButton(check1dIntegrity)
        self.addLine_button.setGeometry(QtCore.QRect(564, 31, 61, 21))
        self.addLine_button.setObjectName(_fromUtf8("addLine_button"))
        self.addPoint_combo = QtGui.QComboBox(check1dIntegrity)
        self.addPoint_combo.setGeometry(QtCore.QRect(10, 153, 541, 22))
        self.addPoint_combo.setObjectName(_fromUtf8("addPoint_combo"))
        self.lineLyrs_lw = QtGui.QListWidget(check1dIntegrity)
        self.lineLyrs_lw.setGeometry(QtCore.QRect(10, 60, 681, 71))
        self.lineLyrs_lw.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.lineLyrs_lw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.lineLyrs_lw.setObjectName(_fromUtf8("lineLyrs_lw"))
        self.pointLyrs_lw = QtGui.QListWidget(check1dIntegrity)
        self.pointLyrs_lw.setGeometry(QtCore.QRect(10, 183, 681, 71))
        self.pointLyrs_lw.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.pointLyrs_lw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.pointLyrs_lw.setObjectName(_fromUtf8("pointLyrs_lw"))
        self.removeLine_button = QtGui.QPushButton(check1dIntegrity)
        self.removeLine_button.setGeometry(QtCore.QRect(630, 31, 61, 21))
        self.removeLine_button.setObjectName(_fromUtf8("removeLine_button"))
        self.removePoint_button = QtGui.QPushButton(check1dIntegrity)
        self.removePoint_button.setGeometry(QtCore.QRect(628, 153, 61, 21))
        self.removePoint_button.setObjectName(_fromUtf8("removePoint_button"))
        self.addPoint_button = QtGui.QPushButton(check1dIntegrity)
        self.addPoint_button.setGeometry(QtCore.QRect(562, 153, 61, 21))
        self.addPoint_button.setObjectName(_fromUtf8("addPoint_button"))
        self.taLyrs_lw = QtGui.QListWidget(check1dIntegrity)
        self.taLyrs_lw.setEnabled(True)
        self.taLyrs_lw.setGeometry(QtCore.QRect(10, 308, 681, 71))
        self.taLyrs_lw.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.taLyrs_lw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.taLyrs_lw.setObjectName(_fromUtf8("taLyrs_lw"))
        self.addTa_combo = QtGui.QComboBox(check1dIntegrity)
        self.addTa_combo.setEnabled(True)
        self.addTa_combo.setGeometry(QtCore.QRect(10, 278, 541, 22))
        self.addTa_combo.setObjectName(_fromUtf8("addTa_combo"))
        self.removeTa_button = QtGui.QPushButton(check1dIntegrity)
        self.removeTa_button.setEnabled(True)
        self.removeTa_button.setGeometry(QtCore.QRect(628, 278, 61, 21))
        self.removeTa_button.setObjectName(_fromUtf8("removeTa_button"))
        self.addTa_button = QtGui.QPushButton(check1dIntegrity)
        self.addTa_button.setEnabled(True)
        self.addTa_button.setGeometry(QtCore.QRect(562, 278, 61, 21))
        self.addTa_button.setObjectName(_fromUtf8("addTa_button"))
        self.label_8 = QtGui.QLabel(check1dIntegrity)
        self.label_8.setEnabled(True)
        self.label_8.setGeometry(QtCore.QRect(10, 260, 141, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.groupBox_4 = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox_4.setEnabled(True)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 389, 391, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setCheckable(True)
        self.groupBox_4.setChecked(False)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setEnabled(False)
        self.label_4.setGeometry(QtCore.QRect(180, 43, 161, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.snapSearchDis_sb = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.snapSearchDis_sb.setEnabled(False)
        self.snapSearchDis_sb.setGeometry(QtCore.QRect(100, 40, 71, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.snapSearchDis_sb.setFont(font)
        self.snapSearchDis_sb.setDecimals(4)
        self.snapSearchDis_sb.setMinimum(0.0001)
        self.snapSearchDis_sb.setObjectName(_fromUtf8("snapSearchDis_sb"))
        self.check1dPoint_cb = QtGui.QCheckBox(self.groupBox_4)
        self.check1dPoint_cb.setGeometry(QtCore.QRect(210, 20, 181, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.check1dPoint_cb.setFont(font)
        self.check1dPoint_cb.setObjectName(_fromUtf8("check1dPoint_cb"))
        self.check1dLine_cb = QtGui.QCheckBox(self.groupBox_4)
        self.check1dLine_cb.setGeometry(QtCore.QRect(10, 20, 191, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.check1dLine_cb.setFont(font)
        self.check1dLine_cb.setObjectName(_fromUtf8("check1dLine_cb"))
        self.autoSnap_cb = QtGui.QCheckBox(self.groupBox_4)
        self.autoSnap_cb.setGeometry(QtCore.QRect(10, 40, 91, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.autoSnap_cb.setFont(font)
        self.autoSnap_cb.setObjectName(_fromUtf8("autoSnap_cb"))
        self.groupBox_3 = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 470, 391, 221))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setCheckable(True)
        self.groupBox_3.setChecked(False)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.dem_combo = QtGui.QComboBox(self.groupBox_3)
        self.dem_combo.setEnabled(False)
        self.dem_combo.setGeometry(QtCore.QRect(45, 192, 331, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dem_combo.setFont(font)
        self.dem_combo.setObjectName(_fromUtf8("dem_combo"))
        self.getGroundElev_cb = QtGui.QCheckBox(self.groupBox_3)
        self.getGroundElev_cb.setEnabled(False)
        self.getGroundElev_cb.setGeometry(QtCore.QRect(10, 154, 191, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.getGroundElev_cb.setFont(font)
        self.getGroundElev_cb.setObjectName(_fromUtf8("getGroundElev_cb"))
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setEnabled(False)
        self.label_3.setGeometry(QtCore.QRect(12, 37, 111, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.name1d_combo = QtGui.QComboBox(self.groupBox_3)
        self.name1d_combo.setEnabled(False)
        self.name1d_combo.setGeometry(QtCore.QRect(10, 55, 261, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.name1d_combo.setFont(font)
        self.name1d_combo.setObjectName(_fromUtf8("name1d_combo"))
        self.plotDsConn_cb = QtGui.QCheckBox(self.groupBox_3)
        self.plotDsConn_cb.setEnabled(False)
        self.plotDsConn_cb.setGeometry(QtCore.QRect(10, 135, 181, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.plotDsConn_cb.setFont(font)
        self.plotDsConn_cb.setObjectName(_fromUtf8("plotDsConn_cb"))
        self.startNwk_lw = QtGui.QListWidget(self.groupBox_3)
        self.startNwk_lw.setEnabled(False)
        self.startNwk_lw.setGeometry(QtCore.QRect(10, 80, 371, 51))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.startNwk_lw.setFont(font)
        self.startNwk_lw.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.startNwk_lw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.startNwk_lw.setObjectName(_fromUtf8("startNwk_lw"))
        self.addStartNwk_button = QtGui.QPushButton(self.groupBox_3)
        self.addStartNwk_button.setEnabled(False)
        self.addStartNwk_button.setGeometry(QtCore.QRect(279, 54, 51, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.addStartNwk_button.setFont(font)
        self.addStartNwk_button.setObjectName(_fromUtf8("addStartNwk_button"))
        self.removeStartNwk_button = QtGui.QPushButton(self.groupBox_3)
        self.removeStartNwk_button.setEnabled(False)
        self.removeStartNwk_button.setGeometry(QtCore.QRect(333, 54, 51, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.removeStartNwk_button.setFont(font)
        self.removeStartNwk_button.setObjectName(_fromUtf8("removeStartNwk_button"))
        self.angle_sb = QtGui.QSpinBox(self.groupBox_3)
        self.angle_sb.setEnabled(False)
        self.angle_sb.setGeometry(QtCore.QRect(228, 17, 41, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.angle_sb.setFont(font)
        self.angle_sb.setMinimum(1)
        self.angle_sb.setMaximum(360)
        self.angle_sb.setProperty("value", 90)
        self.angle_sb.setObjectName(_fromUtf8("angle_sb"))
        self.label_9 = QtGui.QLabel(self.groupBox_3)
        self.label_9.setEnabled(False)
        self.label_9.setGeometry(QtCore.QRect(12, 20, 211, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_15 = QtGui.QLabel(self.groupBox_3)
        self.label_15.setEnabled(False)
        self.label_15.setGeometry(QtCore.QRect(10, 195, 31, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.coverDepth_sb = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.coverDepth_sb.setEnabled(False)
        self.coverDepth_sb.setGeometry(QtCore.QRect(176, 170, 51, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.coverDepth_sb.setFont(font)
        self.coverDepth_sb.setDecimals(2)
        self.coverDepth_sb.setMinimum(0.01)
        self.coverDepth_sb.setMaximum(9999.0)
        self.coverDepth_sb.setProperty("value", 0.5)
        self.coverDepth_sb.setObjectName(_fromUtf8("coverDepth_sb"))
        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setEnabled(False)
        self.label_16.setGeometry(QtCore.QRect(20, 172, 131, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(self.groupBox_3)
        self.label_17.setEnabled(False)
        self.label_17.setGeometry(QtCore.QRect(230, 170, 51, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(self.groupBox_3)
        self.label_18.setEnabled(False)
        self.label_18.setGeometry(QtCore.QRect(272, 18, 51, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.groupBox_6 = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox_6.setGeometry(QtCore.QRect(415, 389, 261, 121))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setCheckable(True)
        self.groupBox_6.setChecked(False)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.correctPipeDir_inverts_cb = QtGui.QCheckBox(self.groupBox_6)
        self.correctPipeDir_inverts_cb.setGeometry(QtCore.QRect(10, 30, 16, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.correctPipeDir_inverts_cb.setFont(font)
        self.correctPipeDir_inverts_cb.setText(_fromUtf8(""))
        self.correctPipeDir_inverts_cb.setObjectName(_fromUtf8("correctPipeDir_inverts_cb"))
        self.label_5 = QtGui.QLabel(self.groupBox_6)
        self.label_5.setGeometry(QtCore.QRect(30, 24, 211, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_6)
        self.label_6.setGeometry(QtCore.QRect(30, 70, 221, 41))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.correctPipeDir_continuity_cb = QtGui.QCheckBox(self.groupBox_6)
        self.correctPipeDir_continuity_cb.setGeometry(QtCore.QRect(10, 80, 16, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.correctPipeDir_continuity_cb.setFont(font)
        self.correctPipeDir_continuity_cb.setText(_fromUtf8(""))
        self.correctPipeDir_continuity_cb.setObjectName(_fromUtf8("correctPipeDir_continuity_cb"))
        self.groupBox_7 = QtGui.QGroupBox(check1dIntegrity)
        self.groupBox_7.setGeometry(QtCore.QRect(415, 520, 261, 251))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setCheckable(True)
        self.groupBox_7.setChecked(False)
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.angle2_sb = QtGui.QSpinBox(self.groupBox_7)
        self.angle2_sb.setEnabled(False)
        self.angle2_sb.setGeometry(QtCore.QRect(45, 106, 41, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.angle2_sb.setFont(font)
        self.angle2_sb.setMinimum(1)
        self.angle2_sb.setMaximum(360)
        self.angle2_sb.setProperty("value", 90)
        self.angle2_sb.setObjectName(_fromUtf8("angle2_sb"))
        self.label_10 = QtGui.QLabel(self.groupBox_7)
        self.label_10.setEnabled(False)
        self.label_10.setGeometry(QtCore.QRect(38, 90, 141, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.groupBox_7)
        self.label_11.setEnabled(False)
        self.label_11.setGeometry(QtCore.QRect(39, 157, 131, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.dem_combo_2 = QtGui.QComboBox(self.groupBox_7)
        self.dem_combo_2.setEnabled(False)
        self.dem_combo_2.setGeometry(QtCore.QRect(70, 203, 181, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dem_combo_2.setFont(font)
        self.dem_combo_2.setObjectName(_fromUtf8("dem_combo_2"))
        self.label_12 = QtGui.QLabel(self.groupBox_7)
        self.label_12.setEnabled(False)
        self.label_12.setGeometry(QtCore.QRect(40, 207, 31, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.coverDepth2_sb = QtGui.QDoubleSpinBox(self.groupBox_7)
        self.coverDepth2_sb.setEnabled(False)
        self.coverDepth2_sb.setGeometry(QtCore.QRect(44, 175, 51, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.coverDepth2_sb.setFont(font)
        self.coverDepth2_sb.setDecimals(2)
        self.coverDepth2_sb.setMinimum(0.01)
        self.coverDepth2_sb.setMaximum(9999.0)
        self.coverDepth2_sb.setProperty("value", 0.5)
        self.coverDepth2_sb.setObjectName(_fromUtf8("coverDepth2_sb"))
        self.label_13 = QtGui.QLabel(self.groupBox_7)
        self.label_13.setEnabled(False)
        self.label_13.setGeometry(QtCore.QRect(98, 175, 51, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(self.groupBox_7)
        self.label_14.setEnabled(False)
        self.label_14.setGeometry(QtCore.QRect(90, 105, 51, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.checkArea_cb = QtGui.QCheckBox(self.groupBox_7)
        self.checkArea_cb.setGeometry(QtCore.QRect(15, 20, 221, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkArea_cb.setFont(font)
        self.checkArea_cb.setObjectName(_fromUtf8("checkArea_cb"))
        self.checkGradient_cb = QtGui.QCheckBox(self.groupBox_7)
        self.checkGradient_cb.setGeometry(QtCore.QRect(15, 46, 221, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkGradient_cb.setFont(font)
        self.checkGradient_cb.setObjectName(_fromUtf8("checkGradient_cb"))
        self.checkAngle_cb = QtGui.QCheckBox(self.groupBox_7)
        self.checkAngle_cb.setGeometry(QtCore.QRect(15, 71, 221, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkAngle_cb.setFont(font)
        self.checkAngle_cb.setObjectName(_fromUtf8("checkAngle_cb"))
        self.checkCover_cb = QtGui.QCheckBox(self.groupBox_7)
        self.checkCover_cb.setGeometry(QtCore.QRect(16, 137, 221, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.checkCover_cb.setFont(font)
        self.checkCover_cb.setObjectName(_fromUtf8("checkCover_cb"))

        self.retranslateUi(check1dIntegrity)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), check1dIntegrity.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), check1dIntegrity.reject)
        QtCore.QMetaObject.connectSlotsByName(check1dIntegrity)

    def retranslateUi(self, check1dIntegrity):
        check1dIntegrity.setWindowTitle(_translate("check1dIntegrity", "Check 1D Network Integrity", None))
        self.label.setText(_translate("check1dIntegrity", "1D network Line Layer", None))
        self.label_2.setText(_translate("check1dIntegrity", "1D network Point Layer", None))
        self.groupBox_2.setTitle(_translate("check1dIntegrity", "Output Options", None))
        self.outSel_cb.setText(_translate("check1dIntegrity", "Output as selection", None))
        self.outMessBox_cb.setText(_translate("check1dIntegrity", "Output to message box", None))
        self.outPLayer_cb.setText(_translate("check1dIntegrity", "Output to 1D_integrity_check.shp", None))
        self.outTxtFile_cb.setText(_translate("check1dIntegrity", "Output to txt file", None))
        self.browse_button.setText(_translate("check1dIntegrity", "Browse", None))
        self.addLine_button.setText(_translate("check1dIntegrity", "Add", None))
        self.removeLine_button.setText(_translate("check1dIntegrity", "Remove", None))
        self.removePoint_button.setText(_translate("check1dIntegrity", "Remove", None))
        self.addPoint_button.setText(_translate("check1dIntegrity", "Add", None))
        self.removeTa_button.setText(_translate("check1dIntegrity", "Remove", None))
        self.addTa_button.setText(_translate("check1dIntegrity", "Add", None))
        self.label_8.setText(_translate("check1dIntegrity", "1D Table Layer", None))
        self.groupBox_4.setTitle(_translate("check1dIntegrity", "Snapping", None))
        self.label_4.setText(_translate("check1dIntegrity", "Search radius (map units)", None))
        self.check1dPoint_cb.setText(_translate("check1dIntegrity", "Check 1D Point-Line snapping", None))
        self.check1dLine_cb.setText(_translate("check1dIntegrity", "Check 1D Line-Line snapping", None))
        self.autoSnap_cb.setText(_translate("check1dIntegrity", "Auto Snap", None))
        self.groupBox_3.setTitle(_translate("check1dIntegrity", "Flow Trace (Upstream to Downstream)", None))
        self.getGroundElev_cb.setText(_translate("check1dIntegrity", "Get ground elevations", None))
        self.label_3.setText(_translate("check1dIntegrity", "Starting at elements:", None))
        self.plotDsConn_cb.setText(_translate("check1dIntegrity", "Plot output in TUPLOT", None))
        self.addStartNwk_button.setText(_translate("check1dIntegrity", "Add", None))
        self.removeStartNwk_button.setText(_translate("check1dIntegrity", "Remove", None))
        self.label_9.setText(_translate("check1dIntegrity", "Flag Network Connection Angles less than:", None))
        self.label_15.setText(_translate("check1dIntegrity", "DEM", None))
        self.label_16.setText(_translate("check1dIntegrity", "Flag depths less than:", None))
        self.label_17.setText(_translate("check1dIntegrity", "map units", None))
        self.label_18.setText(_translate("check1dIntegrity", "degrees", None))
        self.groupBox_6.setTitle(_translate("check1dIntegrity", "Correct Pipe Direction", None))
        self.label_5.setText(_translate("check1dIntegrity", "Based on inverts - will correct if pipe gradient is adverse", None))
        self.label_6.setText(_translate("check1dIntegrity", "Based on pipe direction continuity - will check upstream and downstream pipe directions for continuity", None))
        self.groupBox_7.setTitle(_translate("check1dIntegrity", "Continuity Check", None))
        self.label_10.setText(_translate("check1dIntegrity", "Flag angles less than:", None))
        self.label_11.setText(_translate("check1dIntegrity", "Flag depths less than:", None))
        self.label_12.setText(_translate("check1dIntegrity", "DEM", None))
        self.label_13.setText(_translate("check1dIntegrity", "map units", None))
        self.label_14.setText(_translate("check1dIntegrity", "degrees", None))
        self.checkArea_cb.setText(_translate("check1dIntegrity", "Check downstream area", None))
        self.checkGradient_cb.setText(_translate("check1dIntegrity", "Check inverts", None))
        self.checkAngle_cb.setText(_translate("check1dIntegrity", "Check outlet angle", None))
        self.checkCover_cb.setText(_translate("check1dIntegrity", "Check cover", None))

