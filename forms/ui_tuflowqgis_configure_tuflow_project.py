# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Ellis.Symons\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\tuflow\forms\ui_tuflowqgis_configure_tuflow_project.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tuflowqgis_configure_tf(object):
    def setupUi(self, tuflowqgis_configure_tf):
        tuflowqgis_configure_tf.setObjectName("tuflowqgis_configure_tf")
        tuflowqgis_configure_tf.resize(362, 447)
        self.gridLayout_2 = QtWidgets.QGridLayout(tuflowqgis_configure_tf)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_1 = QtWidgets.QLabel(tuflowqgis_configure_tf)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.crsDesc = QtWidgets.QLineEdit(tuflowqgis_configure_tf)
        self.crsDesc.setDragEnabled(False)
        self.crsDesc.setReadOnly(True)
        self.crsDesc.setObjectName("crsDesc")
        self.gridLayout.addWidget(self.crsDesc, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 14, 0, 1, 1)
        self.browseoutfile = QtWidgets.QPushButton(tuflowqgis_configure_tf)
        self.browseoutfile.setObjectName("browseoutfile")
        self.gridLayout.addWidget(self.browseoutfile, 7, 1, 1, 1)
        self.pbSelectCRS = QtWidgets.QPushButton(tuflowqgis_configure_tf)
        self.pbSelectCRS.setObjectName("pbSelectCRS")
        self.gridLayout.addWidget(self.pbSelectCRS, 5, 1, 1, 1)
        self.browseexe = QtWidgets.QPushButton(tuflowqgis_configure_tf)
        self.browseexe.setObjectName("browseexe")
        self.gridLayout.addWidget(self.browseexe, 9, 1, 1, 1)
        self.cbGlobal = QtWidgets.QCheckBox(tuflowqgis_configure_tf)
        self.cbGlobal.setObjectName("cbGlobal")
        self.gridLayout.addWidget(self.cbGlobal, 11, 0, 1, 2)
        self.cbRun = QtWidgets.QCheckBox(tuflowqgis_configure_tf)
        self.cbRun.setObjectName("cbRun")
        self.gridLayout.addWidget(self.cbRun, 13, 0, 1, 2)
        self.cbCreate = QtWidgets.QCheckBox(tuflowqgis_configure_tf)
        self.cbCreate.setObjectName("cbCreate")
        self.gridLayout.addWidget(self.cbCreate, 12, 0, 1, 2)
        self.TUFLOW_exe = QtWidgets.QLineEdit(tuflowqgis_configure_tf)
        self.TUFLOW_exe.setReadOnly(False)
        self.TUFLOW_exe.setObjectName("TUFLOW_exe")
        self.gridLayout.addWidget(self.TUFLOW_exe, 9, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(tuflowqgis_configure_tf)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.sourcelayer = QtWidgets.QComboBox(tuflowqgis_configure_tf)
        self.sourcelayer.setObjectName("sourcelayer")
        self.gridLayout.addWidget(self.sourcelayer, 1, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(tuflowqgis_configure_tf)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.form_crsID = QtWidgets.QLineEdit(tuflowqgis_configure_tf)
        self.form_crsID.setDragEnabled(False)
        self.form_crsID.setReadOnly(True)
        self.form_crsID.setObjectName("form_crsID")
        self.gridLayout.addWidget(self.form_crsID, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(tuflowqgis_configure_tf)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(tuflowqgis_configure_tf)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.outdir = QtWidgets.QLineEdit(tuflowqgis_configure_tf)
        self.outdir.setReadOnly(False)
        self.outdir.setObjectName("outdir")
        self.gridLayout.addWidget(self.outdir, 7, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(tuflowqgis_configure_tf)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rbTuflowCla = QtWidgets.QRadioButton(self.groupBox)
        self.rbTuflowCla.setChecked(True)
        self.rbTuflowCla.setObjectName("rbTuflowCla")
        self.engine = QtWidgets.QButtonGroup(tuflowqgis_configure_tf)
        self.engine.setObjectName("engine")
        self.engine.addButton(self.rbTuflowCla)
        self.verticalLayout.addWidget(self.rbTuflowCla)
        self.rbTuflowFM = QtWidgets.QRadioButton(self.groupBox)
        self.rbTuflowFM.setObjectName("rbTuflowFM")
        self.engine.addButton(self.rbTuflowFM)
        self.verticalLayout.addWidget(self.rbTuflowFM)
        self.gridLayout.addWidget(self.groupBox, 10, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(tuflowqgis_configure_tf)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(tuflowqgis_configure_tf)
        self.buttonBox.accepted.connect(tuflowqgis_configure_tf.accept)
        self.buttonBox.rejected.connect(tuflowqgis_configure_tf.reject)
        QtCore.QMetaObject.connectSlotsByName(tuflowqgis_configure_tf)

    def retranslateUi(self, tuflowqgis_configure_tf):
        _translate = QtCore.QCoreApplication.translate
        tuflowqgis_configure_tf.setWindowTitle(_translate("tuflowqgis_configure_tf", "Configure TUFLOW Project"))
        self.label_1.setText(_translate("tuflowqgis_configure_tf", "Source Projection Layer"))
        self.crsDesc.setText(_translate("tuflowqgis_configure_tf", "<projection description>"))
        self.browseoutfile.setText(_translate("tuflowqgis_configure_tf", "Browse..."))
        self.pbSelectCRS.setText(_translate("tuflowqgis_configure_tf", "Select CRS"))
        self.browseexe.setText(_translate("tuflowqgis_configure_tf", "Browse..."))
        self.cbGlobal.setText(_translate("tuflowqgis_configure_tf", "Save Default Settings Globally (for all projects)"))
        self.cbRun.setText(_translate("tuflowqgis_configure_tf", "Run TUFLOW to create template files"))
        self.cbCreate.setText(_translate("tuflowqgis_configure_tf", "Create TUFLOW Folder Structure"))
        self.TUFLOW_exe.setText(_translate("tuflowqgis_configure_tf", "<TUFLOW exe>"))
        self.label_3.setText(_translate("tuflowqgis_configure_tf", "Folder which contains TUFLOW"))
        self.label_5.setText(_translate("tuflowqgis_configure_tf", "Projection ID (display only)"))
        self.form_crsID.setText(_translate("tuflowqgis_configure_tf", "<projection id>"))
        self.label_4.setText(_translate("tuflowqgis_configure_tf", "TUFLOW executable"))
        self.label_2.setText(_translate("tuflowqgis_configure_tf", "Projection Description (display only)"))
        self.outdir.setText(_translate("tuflowqgis_configure_tf", "<directory>"))
        self.groupBox.setTitle(_translate("tuflowqgis_configure_tf", "TUFLOW Engine"))
        self.rbTuflowCla.setText(_translate("tuflowqgis_configure_tf", "TUFLOW Classic / HPC"))
        self.rbTuflowFM.setText(_translate("tuflowqgis_configure_tf", "TUFLOW Flexible Mesh"))

