# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tuflowqgis_TuPlot.ui'
#
# Created: Wed May 09 12:25:59 2018
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

class Ui_tuflowqgis_TuPlot(object):
    def setupUi(self, tuflowqgis_TuPlot):
        tuflowqgis_TuPlot.setObjectName(_fromUtf8("tuflowqgis_TuPlot"))
        tuflowqgis_TuPlot.resize(952, 596)
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_1.sizePolicy().hasHeightForWidth())
        self.tab_1.setSizePolicy(sizePolicy)
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.gridlayout = QtGui.QGridLayout(self.tab_1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self._2 = QtGui.QHBoxLayout()
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label1 = QtGui.QLabel(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.gridLayout_3.addWidget(self.label1, 0, 0, 1, 1)
        self.ResList = QtGui.QListWidget(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResList.sizePolicy().hasHeightForWidth())
        self.ResList.setSizePolicy(sizePolicy)
        self.ResList.setMinimumSize(QtCore.QSize(200, 0))
        self.ResList.setMaximumSize(QtCore.QSize(200, 200))
        self.ResList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ResList.setObjectName(_fromUtf8("ResList"))
        self.gridLayout_3.addWidget(self.ResList, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab_1)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.HydPropList = QtGui.QListWidget(self.tab_1)
        self.HydPropList.setMinimumSize(QtCore.QSize(200, 50))
        self.HydPropList.setMaximumSize(QtCore.QSize(200, 75))
        self.HydPropList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.HydPropList.setObjectName(_fromUtf8("HydPropList"))
        self.gridLayout_3.addWidget(self.HydPropList, 3, 0, 1, 1)
        self.Control = QtGui.QGroupBox(self.tab_1)
        self.Control.setMinimumSize(QtCore.QSize(20, 85))
        self.Control.setMaximumSize(QtCore.QSize(250, 16777215))
        self.Control.setObjectName(_fromUtf8("Control"))
        self.CloseRes = QtGui.QPushButton(self.Control)
        self.CloseRes.setGeometry(QtCore.QRect(105, 13, 80, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseRes.sizePolicy().hasHeightForWidth())
        self.CloseRes.setSizePolicy(sizePolicy)
        self.CloseRes.setMinimumSize(QtCore.QSize(50, 20))
        self.CloseRes.setMaximumSize(QtCore.QSize(80, 40))
        self.CloseRes.setAutoRepeat(False)
        self.CloseRes.setAutoDefault(False)
        self.CloseRes.setDefault(False)
        self.CloseRes.setFlat(False)
        self.CloseRes.setObjectName(_fromUtf8("CloseRes"))
        self.AddRes = QtGui.QPushButton(self.Control)
        self.AddRes.setGeometry(QtCore.QRect(10, 13, 80, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddRes.sizePolicy().hasHeightForWidth())
        self.AddRes.setSizePolicy(sizePolicy)
        self.AddRes.setMinimumSize(QtCore.QSize(50, 20))
        self.AddRes.setMaximumSize(QtCore.QSize(80, 40))
        self.AddRes.setObjectName(_fromUtf8("AddRes"))
        self.pbAddRes_GIS = QtGui.QPushButton(self.Control)
        self.pbAddRes_GIS.setGeometry(QtCore.QRect(10, 36, 80, 20))
        self.pbAddRes_GIS.setObjectName(_fromUtf8("pbAddRes_GIS"))
        self.pbHelp = QtGui.QPushButton(self.Control)
        self.pbHelp.setGeometry(QtCore.QRect(105, 36, 80, 20))
        self.pbHelp.setObjectName(_fromUtf8("pbHelp"))
        self.AddHydTab = QtGui.QPushButton(self.Control)
        self.AddHydTab.setGeometry(QtCore.QRect(10, 60, 80, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddHydTab.sizePolicy().hasHeightForWidth())
        self.AddHydTab.setSizePolicy(sizePolicy)
        self.AddHydTab.setMinimumSize(QtCore.QSize(80, 20))
        self.AddHydTab.setMaximumSize(QtCore.QSize(20, 40))
        self.AddHydTab.setObjectName(_fromUtf8("AddHydTab"))
        self.CloseHydTab = QtGui.QPushButton(self.Control)
        self.CloseHydTab.setGeometry(QtCore.QRect(105, 60, 80, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseHydTab.sizePolicy().hasHeightForWidth())
        self.CloseHydTab.setSizePolicy(sizePolicy)
        self.CloseHydTab.setMinimumSize(QtCore.QSize(80, 20))
        self.CloseHydTab.setMaximumSize(QtCore.QSize(80, 40))
        self.CloseHydTab.setObjectName(_fromUtf8("CloseHydTab"))
        self.gridLayout_3.addWidget(self.Control, 4, 0, 1, 1)
        self.label3 = QtGui.QLabel(self.tab_1)
        self.label3.setMaximumSize(QtCore.QSize(300, 20))
        self.label3.setObjectName(_fromUtf8("label3"))
        self.gridLayout_3.addWidget(self.label3, 5, 0, 1, 1)
        self.locationDrop = QtGui.QComboBox(self.tab_1)
        self.locationDrop.setMaximumSize(QtCore.QSize(200, 20))
        self.locationDrop.setObjectName(_fromUtf8("locationDrop"))
        self.gridLayout_3.addWidget(self.locationDrop, 6, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label4 = QtGui.QLabel(self.tab_1)
        self.label4.setMaximumSize(QtCore.QSize(300, 20))
        self.label4.setObjectName(_fromUtf8("label4"))
        self.horizontalLayout_2.addWidget(self.label4)
        self.cb2ndAxis = QtGui.QCheckBox(self.tab_1)
        self.cb2ndAxis.setMaximumSize(QtCore.QSize(16777215, 20))
        self.cb2ndAxis.setObjectName(_fromUtf8("cb2ndAxis"))
        self.horizontalLayout_2.addWidget(self.cb2ndAxis)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 7, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ResTypeList = QtGui.QListWidget(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResTypeList.sizePolicy().hasHeightForWidth())
        self.ResTypeList.setSizePolicy(sizePolicy)
        self.ResTypeList.setMinimumSize(QtCore.QSize(10, 60))
        self.ResTypeList.setMaximumSize(QtCore.QSize(125, 300))
        self.ResTypeList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ResTypeList.setObjectName(_fromUtf8("ResTypeList"))
        self.horizontalLayout.addWidget(self.ResTypeList)
        self.ResTypeList_ax2 = QtGui.QListWidget(self.tab_1)
        self.ResTypeList_ax2.setEnabled(True)
        self.ResTypeList_ax2.setMaximumSize(QtCore.QSize(75, 300))
        self.ResTypeList_ax2.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ResTypeList_ax2.setObjectName(_fromUtf8("ResTypeList_ax2"))
        self.horizontalLayout.addWidget(self.ResTypeList_ax2)
        self.gridLayout_3.addLayout(self.horizontalLayout, 8, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pbAnimatePlot = QtGui.QPushButton(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbAnimatePlot.sizePolicy().hasHeightForWidth())
        self.pbAnimatePlot.setSizePolicy(sizePolicy)
        self.pbAnimatePlot.setMinimumSize(QtCore.QSize(50, 20))
        self.pbAnimatePlot.setMaximumSize(QtCore.QSize(70, 40))
        self.pbAnimatePlot.setObjectName(_fromUtf8("pbAnimatePlot"))
        self.horizontalLayout_5.addWidget(self.pbAnimatePlot)
        self.label_3 = QtGui.QLabel(self.tab_1)
        self.label_3.setMaximumSize(QtCore.QSize(70, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.dropExportExt = QtGui.QComboBox(self.tab_1)
        self.dropExportExt.setMaximumSize(QtCore.QSize(60, 20))
        self.dropExportExt.setObjectName(_fromUtf8("dropExportExt"))
        self.horizontalLayout_5.addWidget(self.dropExportExt)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 9, 0, 1, 1)
        self._2.addLayout(self.gridLayout_3)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label5 = QtGui.QLabel(self.tab_1)
        self.label5.setObjectName(_fromUtf8("label5"))
        self.gridLayout_2.addWidget(self.label5, 0, 0, 1, 1)
        self.IDList = QtGui.QListWidget(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IDList.sizePolicy().hasHeightForWidth())
        self.IDList.setSizePolicy(sizePolicy)
        self.IDList.setMinimumSize(QtCore.QSize(10, 0))
        self.IDList.setMaximumSize(QtCore.QSize(200, 160))
        self.IDList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.IDList.setObjectName(_fromUtf8("IDList"))
        self.gridLayout_2.addWidget(self.IDList, 1, 0, 1, 1)
        self.label6 = QtGui.QLabel(self.tab_1)
        self.label6.setObjectName(_fromUtf8("label6"))
        self.gridLayout_2.addWidget(self.label6, 2, 0, 1, 1)
        self.listTime = QtGui.QListWidget(self.tab_1)
        self.listTime.setMinimumSize(QtCore.QSize(10, 0))
        self.listTime.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listTime.setObjectName(_fromUtf8("listTime"))
        self.gridLayout_2.addWidget(self.listTime, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.tab_1)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.lwStatus = QtGui.QListWidget(self.tab_1)
        self.lwStatus.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lwStatus.setObjectName(_fromUtf8("lwStatus"))
        self.gridLayout_2.addWidget(self.lwStatus, 5, 0, 1, 1)
        self.pbClearStatus = QtGui.QPushButton(self.tab_1)
        self.pbClearStatus.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pbClearStatus.setObjectName(_fromUtf8("pbClearStatus"))
        self.gridLayout_2.addWidget(self.pbClearStatus, 6, 0, 1, 1)
        self._2.addLayout(self.gridLayout_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_for_plot = QtGui.QFrame(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_for_plot.sizePolicy().hasHeightForWidth())
        self.frame_for_plot.setSizePolicy(sizePolicy)
        self.frame_for_plot.setMinimumSize(QtCore.QSize(150, 0))
        self.frame_for_plot.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_for_plot.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_for_plot.setObjectName(_fromUtf8("frame_for_plot"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.frame_for_plot)
        self.verticalLayout_9.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pbUpdate = QtGui.QPushButton(self.frame_for_plot)
        self.pbUpdate.setObjectName(_fromUtf8("pbUpdate"))
        self.gridLayout_4.addWidget(self.pbUpdate, 0, 0, 1, 1)
        self.cbShowLegend = QtGui.QCheckBox(self.frame_for_plot)
        self.cbShowLegend.setObjectName(_fromUtf8("cbShowLegend"))
        self.gridLayout_4.addWidget(self.cbShowLegend, 0, 1, 1, 1)
        self.cbLegendUL = QtGui.QCheckBox(self.frame_for_plot)
        self.cbLegendUL.setObjectName(_fromUtf8("cbLegendUL"))
        self.gridLayout_4.addWidget(self.cbLegendUL, 0, 2, 1, 1)
        self.cbLegendUR = QtGui.QCheckBox(self.frame_for_plot)
        self.cbLegendUR.setObjectName(_fromUtf8("cbLegendUR"))
        self.gridLayout_4.addWidget(self.cbLegendUR, 0, 3, 1, 1)
        self.cbLegendLL = QtGui.QCheckBox(self.frame_for_plot)
        self.cbLegendLL.setObjectName(_fromUtf8("cbLegendLL"))
        self.gridLayout_4.addWidget(self.cbLegendLL, 0, 4, 1, 1)
        self.cbLegendLR = QtGui.QCheckBox(self.frame_for_plot)
        self.cbLegendLR.setObjectName(_fromUtf8("cbLegendLR"))
        self.gridLayout_4.addWidget(self.cbLegendLR, 0, 5, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_4)
        self.gridLayout.addWidget(self.frame_for_plot, 0, 0, 1, 1)
        self._2.addLayout(self.gridLayout)
        self.gridlayout.addLayout(self._2, 1, 0, 1, 1)
        self.frame_for_toolbar = QtGui.QFrame(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_for_toolbar.sizePolicy().hasHeightForWidth())
        self.frame_for_toolbar.setSizePolicy(sizePolicy)
        self.frame_for_toolbar.setMinimumSize(QtCore.QSize(600, 40))
        self.frame_for_toolbar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_for_toolbar.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_for_toolbar.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_for_toolbar.setObjectName(_fromUtf8("frame_for_toolbar"))
        self.gridlayout.addWidget(self.frame_for_toolbar, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_Options = QtGui.QWidget()
        self.tab_Options.setObjectName(_fromUtf8("tab_Options"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tab_Options)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 268, 199))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.cbDeactivate = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cbDeactivate.setMaximumSize(QtCore.QSize(600, 40))
        self.cbDeactivate.setObjectName(_fromUtf8("cbDeactivate"))
        self.verticalLayout_4.addWidget(self.cbDeactivate)
        self.cbXSRoughness = QtGui.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbXSRoughness.sizePolicy().hasHeightForWidth())
        self.cbXSRoughness.setSizePolicy(sizePolicy)
        self.cbXSRoughness.setMinimumSize(QtCore.QSize(80, 0))
        self.cbXSRoughness.setMaximumSize(QtCore.QSize(600, 40))
        self.cbXSRoughness.setObjectName(_fromUtf8("cbXSRoughness"))
        self.verticalLayout_4.addWidget(self.cbXSRoughness)
        self.cbForceXS = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cbForceXS.setObjectName(_fromUtf8("cbForceXS"))
        self.verticalLayout_4.addWidget(self.cbForceXS)
        self.cbForceRes = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cbForceRes.setObjectName(_fromUtf8("cbForceRes"))
        self.verticalLayout_4.addWidget(self.cbForceRes)
        self.cbCalcMedian = QtGui.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbCalcMedian.sizePolicy().hasHeightForWidth())
        self.cbCalcMedian.setSizePolicy(sizePolicy)
        self.cbCalcMedian.setMinimumSize(QtCore.QSize(80, 0))
        self.cbCalcMedian.setMaximumSize(QtCore.QSize(600, 40))
        self.cbCalcMedian.setObjectName(_fromUtf8("cbCalcMedian"))
        self.verticalLayout_4.addWidget(self.cbCalcMedian)
        self.cbCalcMean = QtGui.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbCalcMean.sizePolicy().hasHeightForWidth())
        self.cbCalcMean.setSizePolicy(sizePolicy)
        self.cbCalcMean.setMinimumSize(QtCore.QSize(80, 0))
        self.cbCalcMean.setMaximumSize(QtCore.QSize(600, 40))
        self.cbCalcMean.setObjectName(_fromUtf8("cbCalcMean"))
        self.verticalLayout_4.addWidget(self.cbCalcMean)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.cbMeanAbove = QtGui.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbMeanAbove.sizePolicy().hasHeightForWidth())
        self.cbMeanAbove.setSizePolicy(sizePolicy)
        self.cbMeanAbove.setMinimumSize(QtCore.QSize(80, 0))
        self.cbMeanAbove.setMaximumSize(QtCore.QSize(600, 40))
        self.cbMeanAbove.setChecked(True)
        self.cbMeanAbove.setObjectName(_fromUtf8("cbMeanAbove"))
        self.verticalLayout_4.addWidget(self.cbMeanAbove)
        self.cbMeanClosest = QtGui.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbMeanClosest.sizePolicy().hasHeightForWidth())
        self.cbMeanClosest.setSizePolicy(sizePolicy)
        self.cbMeanClosest.setMinimumSize(QtCore.QSize(80, 0))
        self.cbMeanClosest.setMaximumSize(QtCore.QSize(600, 40))
        self.cbMeanClosest.setObjectName(_fromUtf8("cbMeanClosest"))
        self.verticalLayout_4.addWidget(self.cbMeanClosest)
        self.tabWidget.addTab(self.tab_Options, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        tuflowqgis_TuPlot.setWidget(self.dockWidgetContents)

        self.retranslateUi(tuflowqgis_TuPlot)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(tuflowqgis_TuPlot)

    def retranslateUi(self, tuflowqgis_TuPlot):
        tuflowqgis_TuPlot.setWindowTitle(_translate("tuflowqgis_TuPlot", "TuPlot", None))
        self.label1.setText(_translate("tuflowqgis_TuPlot", "Results Files", None))
        self.label_4.setText(_translate("tuflowqgis_TuPlot", "1D Table Check Files", None))
        self.Control.setTitle(_translate("tuflowqgis_TuPlot", "Control", None))
        self.CloseRes.setText(_translate("tuflowqgis_TuPlot", "Close Results", None))
        self.AddRes.setText(_translate("tuflowqgis_TuPlot", "Add Results", None))
        self.pbAddRes_GIS.setText(_translate("tuflowqgis_TuPlot", "Add Res + GIS", None))
        self.pbHelp.setText(_translate("tuflowqgis_TuPlot", "Help / About", None))
        self.AddHydTab.setText(_translate("tuflowqgis_TuPlot", "Add 1D Table", None))
        self.CloseHydTab.setText(_translate("tuflowqgis_TuPlot", "Close 1D Table", None))
        self.label3.setText(_translate("tuflowqgis_TuPlot", "Plot Type", None))
        self.label4.setText(_translate("tuflowqgis_TuPlot", "Results Type", None))
        self.cb2ndAxis.setText(_translate("tuflowqgis_TuPlot", "Use Second Axis", None))
        self.pbAnimatePlot.setText(_translate("tuflowqgis_TuPlot", "Animate Plot", None))
        self.label_3.setText(_translate("tuflowqgis_TuPlot", "Export Format", None))
        self.label5.setText(_translate("tuflowqgis_TuPlot", "Selected Elements (display only)", None))
        self.label6.setText(_translate("tuflowqgis_TuPlot", "Current Time", None))
        self.label.setText(_translate("tuflowqgis_TuPlot", "Status Dialogue", None))
        self.pbClearStatus.setText(_translate("tuflowqgis_TuPlot", "Clear Status", None))
        self.pbUpdate.setText(_translate("tuflowqgis_TuPlot", "UPDATE PLOT", None))
        self.cbShowLegend.setText(_translate("tuflowqgis_TuPlot", "Legend", None))
        self.cbLegendUL.setText(_translate("tuflowqgis_TuPlot", "UL", None))
        self.cbLegendUR.setText(_translate("tuflowqgis_TuPlot", "UR", None))
        self.cbLegendLL.setText(_translate("tuflowqgis_TuPlot", "LL", None))
        self.cbLegendLR.setText(_translate("tuflowqgis_TuPlot", "LR", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("tuflowqgis_TuPlot", "&Graph", None))
        self.cbDeactivate.setText(_translate("tuflowqgis_TuPlot", "Deactivate Viewer", None))
        self.cbXSRoughness.setText(_translate("tuflowqgis_TuPlot", "Display Roughness (Cross-section only)", None))
        self.cbForceXS.setText(_translate("tuflowqgis_TuPlot", "Force Cross Section Layer (ignore attribute check)", None))
        self.cbForceRes.setText(_translate("tuflowqgis_TuPlot", "Force Results Layer (ignore attribute check)", None))
        self.cbCalcMedian.setText(_translate("tuflowqgis_TuPlot", "Show Median Event (Time-series Only)", None))
        self.cbCalcMean.setText(_translate("tuflowqgis_TuPlot", "Show Mean Event (Time-series Only)", None))
        self.label_2.setText(_translate("tuflowqgis_TuPlot", "Mean Event Method", None))
        self.cbMeanAbove.setText(_translate("tuflowqgis_TuPlot", "Event Above", None))
        self.cbMeanClosest.setText(_translate("tuflowqgis_TuPlot", "Event Closest", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Options), _translate("tuflowqgis_TuPlot", "Options", None))

