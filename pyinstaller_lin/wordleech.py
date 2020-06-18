# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wordleech.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.grp_load = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_load.setObjectName("grp_load")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.grp_load)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.grp_load)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_reset = QtWidgets.QPushButton(self.grp_load)
        self.btn_reset.setObjectName("btn_reset")
        self.horizontalLayout.addWidget(self.btn_reset)
        self.btn_process = QtWidgets.QPushButton(self.grp_load)
        self.btn_process.setEnabled(False)
        self.btn_process.setObjectName("btn_process")
        self.horizontalLayout.addWidget(self.btn_process)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 4, 1, 1)
        self.label = QtWidgets.QLabel(self.grp_load)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.pb_process = QtWidgets.QProgressBar(self.grp_load)
        self.pb_process.setProperty("value", 0)
        self.pb_process.setObjectName("pb_process")
        self.gridLayout_2.addWidget(self.pb_process, 2, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 4, 1, 1)
        self.btn_load_dict = QtWidgets.QPushButton(self.grp_load)
        self.btn_load_dict.setObjectName("btn_load_dict")
        self.gridLayout_2.addWidget(self.btn_load_dict, 0, 1, 1, 1)
        self.lbl_loaded_dict = QtWidgets.QLabel(self.grp_load)
        self.lbl_loaded_dict.setObjectName("lbl_loaded_dict")
        self.gridLayout_2.addWidget(self.lbl_loaded_dict, 0, 3, 1, 1)
        self.btn_load_source = QtWidgets.QPushButton(self.grp_load)
        self.btn_load_source.setObjectName("btn_load_source")
        self.gridLayout_2.addWidget(self.btn_load_source, 1, 1, 1, 1)
        self.lbl_loaded_sources = QtWidgets.QLabel(self.grp_load)
        self.lbl_loaded_sources.setObjectName("lbl_loaded_sources")
        self.gridLayout_2.addWidget(self.lbl_loaded_sources, 1, 3, 1, 1)
        self.lbl_status = QtWidgets.QLabel(self.grp_load)
        self.lbl_status.setObjectName("lbl_status")
        self.gridLayout_2.addWidget(self.lbl_status, 2, 0, 1, 4)
        self.btn_download_dict = QtWidgets.QPushButton(self.grp_load)
        self.btn_download_dict.setObjectName("btn_download_dict")
        self.gridLayout_2.addWidget(self.btn_download_dict, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.grp_load, 0, 0, 1, 1)
        self.grp_results = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_results.setEnabled(False)
        self.grp_results.setObjectName("grp_results")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.grp_results)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_add_all = QtWidgets.QPushButton(self.grp_results)
        self.btn_add_all.setObjectName("btn_add_all")
        self.verticalLayout.addWidget(self.btn_add_all)
        self.btn_add = QtWidgets.QPushButton(self.grp_results)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout.addWidget(self.btn_add)
        self.btn_remove = QtWidgets.QPushButton(self.grp_results)
        self.btn_remove.setObjectName("btn_remove")
        self.verticalLayout.addWidget(self.btn_remove)
        self.btn_remove_all = QtWidgets.QPushButton(self.grp_results)
        self.btn_remove_all.setObjectName("btn_remove_all")
        self.verticalLayout.addWidget(self.btn_remove_all)
        self.gridLayout_3.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.lbl_new = QtWidgets.QLabel(self.grp_results)
        self.lbl_new.setObjectName("lbl_new")
        self.gridLayout_3.addWidget(self.lbl_new, 0, 0, 1, 1)
        self.lbl_add = QtWidgets.QLabel(self.grp_results)
        self.lbl_add.setObjectName("lbl_add")
        self.gridLayout_3.addWidget(self.lbl_add, 0, 2, 1, 1)
        self.btn_generate = QtWidgets.QPushButton(self.grp_results)
        self.btn_generate.setObjectName("btn_generate")
        self.gridLayout_3.addWidget(self.btn_generate, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.grp_results)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.lst_found = QtWidgets.QListWidget(self.grp_results)
        self.lst_found.setObjectName("lst_found")
        self.gridLayout_3.addWidget(self.lst_found, 1, 0, 1, 1)
        self.lst_add = QtWidgets.QListWidget(self.grp_results)
        self.lst_add.setObjectName("lst_add")
        self.gridLayout_3.addWidget(self.lst_add, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.grp_results, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WordLeech"))
        self.grp_load.setTitle(_translate("MainWindow", "Load Files"))
        self.label_2.setText(_translate("MainWindow", "Source File(s)"))
        self.btn_reset.setText(_translate("MainWindow", "Reset"))
        self.btn_process.setText(_translate("MainWindow", "Process"))
        self.label.setText(_translate("MainWindow", "Dictionary File"))
        self.btn_load_dict.setText(_translate("MainWindow", "Browse..."))
        self.lbl_loaded_dict.setText(_translate("MainWindow", "No File Loaded."))
        self.btn_load_source.setText(_translate("MainWindow", "Browse..."))
        self.lbl_loaded_sources.setText(_translate("MainWindow", "No Sources Loaded."))
        self.lbl_status.setText(_translate("MainWindow", "Idle"))
        self.btn_download_dict.setText(_translate("MainWindow", "Download Latest"))
        self.grp_results.setTitle(_translate("MainWindow", "Results"))
        self.btn_add_all.setText(_translate("MainWindow", ">>"))
        self.btn_add.setText(_translate("MainWindow", ">"))
        self.btn_remove.setText(_translate("MainWindow", "<"))
        self.btn_remove_all.setText(_translate("MainWindow", "<<"))
        self.lbl_new.setText(_translate("MainWindow", "New Words Found"))
        self.lbl_add.setText(_translate("MainWindow", "Words To Add"))
        self.btn_generate.setText(_translate("MainWindow", "Generate Updated Dictionary"))
        self.label_5.setText(_translate("MainWindow", "v1.0 | 2020 Keith Vassallo"))
