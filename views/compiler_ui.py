# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\USUARIO\Desktop\2do. Semestre 2024\primera_fase_compilador\views\compiler.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1145, 760)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 1141, 721))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(10, 9, 793, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 0, 771, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_buscar = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_buscar.setIconSize(QtCore.QSize(30, 30))
        self.btn_buscar.setObjectName("btn_buscar")
        self.horizontalLayout.addWidget(self.btn_buscar)
        self.ln_ruta_archivo = QtWidgets.QLineEdit(self.layoutWidget)
        self.ln_ruta_archivo.setObjectName("ln_ruta_archivo")
        self.horizontalLayout.addWidget(self.ln_ruta_archivo)
        self.frame_2 = QtWidgets.QFrame(self.tab)
        self.frame_2.setGeometry(QtCore.QRect(20, 100, 501, 581))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.splitter = QtWidgets.QSplitter(self.frame_2)
        self.splitter.setGeometry(QtCore.QRect(10, 0, 471, 571))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.txt_fuente = QtWidgets.QTextEdit(self.layoutWidget1)
        self.txt_fuente.setObjectName("txt_fuente")
        self.verticalLayout.addWidget(self.txt_fuente)
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.txt_errores = QtWidgets.QTextEdit(self.layoutWidget2)
        self.txt_errores.setObjectName("txt_errores")
        self.verticalLayout_2.addWidget(self.txt_errores)
        self.frame_3 = QtWidgets.QFrame(self.tab)
        self.frame_3.setGeometry(QtCore.QRect(540, 100, 591, 501))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.layoutWidget3 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 10, 261, 471))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.tb_resultado = QtWidgets.QTableWidget(self.layoutWidget3)
        self.tb_resultado.setObjectName("tb_resultado")
        self.tb_resultado.setColumnCount(2)
        self.tb_resultado.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_resultado.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_resultado.setHorizontalHeaderItem(1, item)
        self.verticalLayout_3.addWidget(self.tb_resultado)
        self.layoutWidget4 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget4.setGeometry(QtCore.QRect(290, 20, 258, 221))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_4.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.tb_palabras_clave = QtWidgets.QTableWidget(self.layoutWidget4)
        self.tb_palabras_clave.setObjectName("tb_palabras_clave")
        self.tb_palabras_clave.setColumnCount(2)
        self.tb_palabras_clave.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_palabras_clave.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_palabras_clave.setHorizontalHeaderItem(1, item)
        self.verticalLayout_4.addWidget(self.tb_palabras_clave)
        self.layoutWidget5 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget5.setGeometry(QtCore.QRect(290, 260, 258, 221))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_5.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.tb_identificadores = QtWidgets.QTableWidget(self.layoutWidget5)
        self.tb_identificadores.setObjectName("tb_identificadores")
        self.tb_identificadores.setColumnCount(2)
        self.tb_identificadores.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_identificadores.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_identificadores.setHorizontalHeaderItem(1, item)
        self.verticalLayout_5.addWidget(self.tb_identificadores)
        self.btn_exportar = QtWidgets.QPushButton(self.tab)
        self.btn_exportar.setGeometry(QtCore.QRect(1000, 630, 105, 35))
        self.btn_exportar.setObjectName("btn_exportar")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget6 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget6.setGeometry(QtCore.QRect(20, 20, 771, 71))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_buscar_2 = QtWidgets.QPushButton(self.layoutWidget6)
        self.btn_buscar_2.setIconSize(QtCore.QSize(30, 30))
        self.btn_buscar_2.setObjectName("btn_buscar_2")
        self.horizontalLayout_2.addWidget(self.btn_buscar_2)
        self.ln_ruta_archivo_2 = QtWidgets.QLineEdit(self.layoutWidget6)
        self.ln_ruta_archivo_2.setObjectName("ln_ruta_archivo_2")
        self.horizontalLayout_2.addWidget(self.ln_ruta_archivo_2)
        self.frame_4 = QtWidgets.QFrame(self.tab_2)
        self.frame_4.setGeometry(QtCore.QRect(10, 110, 481, 561))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.layoutWidget7 = QtWidgets.QWidget(self.frame_4)
        self.layoutWidget7.setGeometry(QtCore.QRect(10, 20, 431, 251))
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget7)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget7)
        self.label_6.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.txt_fuente_2 = QtWidgets.QTextEdit(self.layoutWidget7)
        self.txt_fuente_2.setObjectName("txt_fuente_2")
        self.verticalLayout_6.addWidget(self.txt_fuente_2)
        self.layoutWidget8 = QtWidgets.QWidget(self.frame_4)
        self.layoutWidget8.setGeometry(QtCore.QRect(10, 280, 431, 241))
        self.layoutWidget8.setObjectName("layoutWidget8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget8)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget8)
        self.label_8.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_7.addWidget(self.label_8)
        self.txt_fuente_3 = QtWidgets.QTextEdit(self.layoutWidget8)
        self.txt_fuente_3.setObjectName("txt_fuente_3")
        self.verticalLayout_7.addWidget(self.txt_fuente_3)
        self.frame_5 = QtWidgets.QFrame(self.tab_2)
        self.frame_5.setGeometry(QtCore.QRect(500, 110, 621, 561))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_7 = QtWidgets.QLabel(self.frame_5)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 429, 28))
        self.label_7.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_7.setObjectName("label_7")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_buscar.setText(_translate("MainWindow", "Buscar"))
        self.label.setText(_translate("MainWindow", "Código Fuente"))
        self.label_2.setText(_translate("MainWindow", "Caracteres No Definidos"))
        self.label_3.setText(_translate("MainWindow", "Caracteres"))
        item = self.tb_resultado.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Tipo"))
        item = self.tb_resultado.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Valor"))
        self.label_4.setText(_translate("MainWindow", "Frecuencia de Palabras Clave"))
        item = self.tb_palabras_clave.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Valor"))
        item = self.tb_palabras_clave.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Frecuencia"))
        self.label_5.setText(_translate("MainWindow", "Frecuencia de Identificadores"))
        item = self.tb_identificadores.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Valor"))
        item = self.tb_identificadores.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Frecuencia"))
        self.btn_exportar.setText(_translate("MainWindow", "Exportar SVG"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.btn_buscar_2.setText(_translate("MainWindow", "Buscar"))
        self.label_6.setText(_translate("MainWindow", "Reglas de Derivación"))
        self.label_8.setText(_translate("MainWindow", "Errores"))
        self.label_7.setText(_translate("MainWindow", "Árbol de Derivación"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Página"))
