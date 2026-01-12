# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LineTrim_Rev01.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LineTrim(object):
    def setupUi(self, LineTrim):
        LineTrim.setObjectName("LineTrim")
        LineTrim.resize(1079, 797)
        self.centralwidget = QtWidgets.QWidget(LineTrim)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_Main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_Main.setObjectName("verticalLayout_Main")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_Main.addWidget(self.widget)
        
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setMaximumSize(QtCore.QSize(5000, 150))
        self.verticalLayout_Main.addWidget(self.frame)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.formLayoutIdentification = QtWidgets.QFormLayout()
        self.formLayoutIdentification.setObjectName("formLayoutIdentification")
        
        self.label_Identification = QtWidgets.QLabel(self.frame)
        self.label_Identification.setObjectName("label_Identification")
        self.formLayoutIdentification.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_Identification)
        self.lineEdit_Identification = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Identification.setObjectName("lineEdit_Identification")
        self.formLayoutIdentification.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Identification)
        self.horizontalLayout.addLayout(self.formLayoutIdentification)

        self.label_Measurement = QtWidgets.QLabel(self.frame)
        self.label_Measurement.setObjectName("label_Measurement")
        self.lineEdit_Measurement = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Measurement.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setPointSize(52)
        self.lineEdit_Measurement.setFont(font)
        self.lineEdit_Measurement.setObjectName("lineEdit_Measurement")
        self.formLayoutIdentification.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Measurement)
        self.formLayoutIdentification.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Measurement)
        

        self.formLayoutInput = QtWidgets.QFormLayout()
        self.formLayoutInput.setObjectName("formLayoutInput")
        self.label_Row = QtWidgets.QLabel(self.frame)
        self.label_Row.setObjectName("label_Row")
        self.formLayoutInput.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_Row)
        self.comboBox_Row = QtWidgets.QComboBox(self.frame)
        self.comboBox_Row.setObjectName("comboBox_Row")
        self.formLayoutInput.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_Row)
        self.label_Number = QtWidgets.QLabel(self.frame)
        self.label_Number.setObjectName("label_Number")
        self.formLayoutInput.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Number)
        self.comboBox_Number = QtWidgets.QComboBox(self.frame)
        self.comboBox_Number.setObjectName("comboBox_Number")
        self.formLayoutInput.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_Number)

        self.label_Side = QtWidgets.QLabel(self.frame)
        self.label_Side.setObjectName("label_Side")
        self.formLayoutInput.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Side)
        self.comboBox_Side = QtWidgets.QComboBox(self.frame)
        self.comboBox_Side.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox_Side.setObjectName("comboBox_Side")
        self.formLayoutInput.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_Side)
        self.comboBox_Direction = QtWidgets.QComboBox(self.frame)
        self.comboBox_Direction.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox_Direction.setObjectName("comboBox_Direction")
        self.formLayoutInput.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_Direction)
        self.label_Direction = QtWidgets.QLabel(self.frame)
        self.label_Direction.setObjectName("label_Direction")
        self.formLayoutInput.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_Direction)
        self.horizontalLayout.addLayout(self.formLayoutInput)

#        self.verticalLayout_2.addLayout(self.horizontalLayout)  # self.horizontalLayout -> là ou va verticalLayout_2

        LineTrim.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LineTrim)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1079, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        LineTrim.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LineTrim)
        self.statusbar.setObjectName("statusbar")
        LineTrim.setStatusBar(self.statusbar)
        self.actionLoad_project = QtWidgets.QAction(LineTrim)
        self.actionLoad_project.setObjectName("actionLoad_project")
        self.actionLoad_line_length = QtWidgets.QAction(LineTrim)
        self.actionLoad_line_length.setObjectName("actionLoad_line_length")
        self.actionSaveAs_project = QtWidgets.QAction(LineTrim)
        self.actionSaveAs_project.setObjectName("actionSaveAs_project")
        self.actionSave_project = QtWidgets.QAction(LineTrim)
        self.actionSave_project.setObjectName("actionSave_project")
        self.actionExportPDFReport = QtWidgets.QAction(LineTrim)
        self.actionExportPDFReport.setObjectName("actionExportPDFReport")
        self.actionSound = QtWidgets.QAction(LineTrim)
        self.actionSound.setObjectName("actionSound")
        self.menuFile.addAction(self.actionLoad_project)
        self.menuFile.addAction(self.actionSaveAs_project)
        self.menuFile.addAction(self.actionSave_project)
        self.menuFile.addAction(self.actionLoad_line_length)
        self.menuFile.addAction(self.actionExportPDFReport)
        self.menuFile.addAction(self.actionSound)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(LineTrim)
        QtCore.QMetaObject.connectSlotsByName(LineTrim)

    def retranslateUi(self, LineTrim):
        _translate = QtCore.QCoreApplication.translate
        LineTrim.setWindowTitle(_translate("LineTrim", "MainWindow"))
        self.label_Identification.setText(_translate("LineTrim", "Identification"))
        self.label_Measurement.setText(_translate("LineTrim", "Measured value"))
        self.label_Row.setText(_translate("LineTrim", "Row"))
        self.label_Number.setText(_translate("LineTrim", "Number"))
        self.label_Side.setText(_translate("LineTrim", "Wing side"))
        self.label_Direction.setText(_translate("LineTrim", "Direction"))
        self.menuFile.setTitle(_translate("LineTrim", "File"))
        self.actionLoad_project.setText(_translate("LineTrim", "Open project"))
        self.actionLoad_line_length.setText(_translate("LineTrim", "Load line length"))
        self.actionSaveAs_project.setText(_translate("LineTrim", "Save project as"))
        self.actionSave_project.setText(_translate("LineTrim", "Save project"))
        self.actionExportPDFReport.setText(_translate("LineTrim", "Export PDF report"))
        self.actionSound.setText(_translate("LineTrim", "Sound Off"))
