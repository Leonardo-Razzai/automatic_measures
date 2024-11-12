# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(957, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plot_osc_button = QtWidgets.QPushButton(self.centralwidget)
        self.plot_osc_button.setGeometry(QtCore.QRect(30, 50, 61, 23))
        self.plot_osc_button.setObjectName("plot_osc_button")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 79, 861, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.plot_osc = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.plot_osc.setContentsMargins(0, 0, 0, 0)
        self.plot_osc.setObjectName("plot_osc")
        self.freq_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.freq_box.setGeometry(QtCore.QRect(90, 20, 62, 22))
        self.freq_box.setObjectName("freq_box")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(27, 21, 81, 21))
        self.textBrowser.setObjectName("textBrowser")
        self.set_freq_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_freq_button.setGeometry(QtCore.QRect(150, 20, 75, 23))
        self.set_freq_button.setObjectName("set_freq_button")
        self.set_time_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_time_button.setGeometry(QtCore.QRect(630, 20, 71, 23))
        self.set_time_button.setObjectName("set_time_button")
        self.time_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.time_box.setGeometry(QtCore.QRect(567, 20, 61, 22))
        self.time_box.setObjectName("time_box")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(484, 20, 111, 21))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.set_voltage_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_voltage_button.setGeometry(QtCore.QRect(630, 49, 71, 23))
        self.set_voltage_button.setObjectName("set_voltage_button")
        self.voltage_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.voltage_box.setGeometry(QtCore.QRect(567, 49, 62, 22))
        self.voltage_box.setObjectName("voltage_box")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(470, 50, 121, 21))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(720, 20, 71, 23))
        self.start_button.setObjectName("start_button")
        self.set_freq_res_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_freq_res_button.setGeometry(QtCore.QRect(230, 20, 75, 23))
        self.set_freq_res_button.setObjectName("set_freq_res_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(720, 49, 71, 23))
        self.stop_button.setObjectName("stop_button")
        self.set_freq_opt_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_freq_opt_button.setGeometry(QtCore.QRect(310, 20, 75, 23))
        self.set_freq_opt_button.setObjectName("set_freq_opt_button")
        self.save_osc_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_osc_button.setGeometry(QtCore.QRect(310, 50, 75, 23))
        self.save_osc_button.setObjectName("save_osc_button")
        self.file_name_osc_input = QtWidgets.QLineEdit(self.centralwidget)
        self.file_name_osc_input.setGeometry(QtCore.QRect(160, 51, 141, 20))
        self.file_name_osc_input.setObjectName("file_name_osc_input")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_7.setGeometry(QtCore.QRect(100, 50, 111, 21))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(30, 370, 871, 321))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 40, 861, 251))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.plot_auto = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.plot_auto.setContentsMargins(0, 0, 0, 0)
        self.plot_auto.setObjectName("plot_auto")
        self.num_atoms_button = QtWidgets.QPushButton(self.tab)
        self.num_atoms_button.setGeometry(QtCore.QRect(700, 9, 71, 23))
        self.num_atoms_button.setObjectName("num_atoms_button")
        self.file_name_auto_input = QtWidgets.QLineEdit(self.tab)
        self.file_name_auto_input.setGeometry(QtCore.QRect(230, 10, 141, 20))
        self.file_name_auto_input.setObjectName("file_name_auto_input")
        self.save_acquisition_button = QtWidgets.QPushButton(self.tab)
        self.save_acquisition_button.setGeometry(QtCore.QRect(380, 9, 75, 23))
        self.save_acquisition_button.setObjectName("save_acquisition_button")
        self.num_atoms_output_text = QtWidgets.QLineEdit(self.tab)
        self.num_atoms_output_text.setGeometry(QtCore.QRect(780, 10, 80, 20))
        self.num_atoms_output_text.setObjectName("num_atoms_output_text")
        self.auto_acquire_button = QtWidgets.QPushButton(self.tab)
        self.auto_acquire_button.setGeometry(QtCore.QRect(0, 9, 111, 23))
        self.auto_acquire_button.setObjectName("auto_acquire_button")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(120, 10, 21, 20))
        self.label.setObjectName("label")
        self.swipe_to_res_checkBox = QtWidgets.QCheckBox(self.tab)
        self.swipe_to_res_checkBox.setEnabled(True)
        self.swipe_to_res_checkBox.setGeometry(QtCore.QRect(145, 12, 16, 17))
        self.swipe_to_res_checkBox.setText("")
        self.swipe_to_res_checkBox.setObjectName("swipe_to_res_checkBox")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(177, 10, 61, 20))
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 40, 861, 251))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.plot_fit = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.plot_fit.setContentsMargins(0, 0, 0, 0)
        self.plot_fit.setObjectName("plot_fit")
        self.fit_button = QtWidgets.QPushButton(self.tab_2)
        self.fit_button.setGeometry(QtCore.QRect(490, 10, 71, 23))
        self.fit_button.setObjectName("fit_button")
        self.start_time_fit_box = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.start_time_fit_box.setGeometry(QtCore.QRect(70, 10, 61, 22))
        self.start_time_fit_box.setObjectName("start_time_fit_box")
        self.set_range_time_fit_button = QtWidgets.QPushButton(self.tab_2)
        self.set_range_time_fit_button.setGeometry(QtCore.QRect(270, 10, 81, 23))
        self.set_range_time_fit_button.setObjectName("set_range_time_fit_button")
        self.end_time_fit_box = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.end_time_fit_box.setGeometry(QtCore.QRect(206, 10, 61, 22))
        self.end_time_fit_box.setObjectName("end_time_fit_box")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(0, 11, 71, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(140, 10, 71, 20))
        self.label_3.setObjectName("label_3")
        self.save_data_fit_button = QtWidgets.QPushButton(self.tab_2)
        self.save_data_fit_button.setGeometry(QtCore.QRect(770, 10, 81, 23))
        self.save_data_fit_button.setObjectName("save_data_fit_button")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(570, 10, 61, 20))
        self.label_5.setObjectName("label_5")
        self.file_name_fit_input = QtWidgets.QLineEdit(self.tab_2)
        self.file_name_fit_input.setGeometry(QtCore.QRect(623, 10, 141, 20))
        self.file_name_fit_input.setObjectName("file_name_fit_input")
        self.tabWidget.addTab(self.tab_2, "")
        self.textBrowser_7.raise_()
        self.textBrowser_3.raise_()
        self.textBrowser_2.raise_()
        self.plot_osc_button.raise_()
        self.verticalLayoutWidget.raise_()
        self.textBrowser.raise_()
        self.freq_box.raise_()
        self.set_freq_button.raise_()
        self.set_time_button.raise_()
        self.time_box.raise_()
        self.set_voltage_button.raise_()
        self.voltage_box.raise_()
        self.start_button.raise_()
        self.set_freq_res_button.raise_()
        self.stop_button.raise_()
        self.set_freq_opt_button.raise_()
        self.save_osc_button.raise_()
        self.file_name_osc_input.raise_()
        self.tabWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 957, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plot_osc_button.setText(_translate("MainWindow", "Plot"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Beat-note [MHz]:</p></body></html>"))
        self.set_freq_button.setText(_translate("MainWindow", "Set freq."))
        self.set_time_button.setText(_translate("MainWindow", "Set Time"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Time Range [s]:</p></body></html>"))
        self.set_voltage_button.setText(_translate("MainWindow", "Set Voltage"))
        self.textBrowser_3.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Voltage Range [V]:</p></body></html>"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.set_freq_res_button.setText(_translate("MainWindow", "Resonance"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.set_freq_opt_button.setText(_translate("MainWindow", "Optimal"))
        self.save_osc_button.setText(_translate("MainWindow", "Save"))
        self.textBrowser_7.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">File Name:</p></body></html>"))
        self.num_atoms_button.setText(_translate("MainWindow", "Num. Atoms"))
        self.save_acquisition_button.setText(_translate("MainWindow", "Save"))
        self.auto_acquire_button.setText(_translate("MainWindow", "Automatic Acquisition"))
        self.label.setText(_translate("MainWindow", "Res: "))
        self.label_4.setText(_translate("MainWindow", "File Name:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Acquisition"))
        self.fit_button.setText(_translate("MainWindow", "Fit"))
        self.set_range_time_fit_button.setText(_translate("MainWindow", "Set Fit Range"))
        self.label_2.setText(_translate("MainWindow", "Start Time [s]:"))
        self.label_3.setText(_translate("MainWindow", "End Time [s]:"))
        self.save_data_fit_button.setText(_translate("MainWindow", "Save Data Fit"))
        self.label_5.setText(_translate("MainWindow", "File Name:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Fit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
