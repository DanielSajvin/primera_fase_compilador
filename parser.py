from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt5.uic import loadUiType
import os


Ui_MainWindow, QMainWindow = loadUiType(
    os.path.join(os.path.dirname(__file__), "views", ".ui")
)


class Parser(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.btn_buscar_2.clicked.connect(self.open_file)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.ln_ruta_archivo.setText(file_path)
            self.process_file(file_path)
