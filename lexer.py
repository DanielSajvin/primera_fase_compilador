from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QTextEdit, QMessageBox
from PyQt5.uic import loadUiType
import os
import ply.lex as lex

# Cargar el archivo .ui
Ui_MainWindow, QMainWindow = loadUiType(os.path.join(os.path.dirname(__file__), 'views', 'principal.ui'))

class MainMenuPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainMenuPrincipal, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        # Verificar si los widgets se cargaron correctamente
        self.verify_widgets()
        
        self.btn_buscar.clicked.connect(self.open_file)
        self.btn_exportar.clicked.connect(self.export_to_txt)  # Conectar el botón de exportación

        # Configurar las QTableWidget
        self.tb_resultado.setColumnCount(2)
        self.tb_resultado.setHorizontalHeaderLabels(['Tipo', 'Valor'])
        self.tb_palabras_clave.setColumnCount(2)
        self.tb_palabras_clave.setHorizontalHeaderLabels(['Valor', 'Frecuencia'])
        self.tb_identificadores.setColumnCount(2)
        self.tb_identificadores.setHorizontalHeaderLabels(['Valor', 'Frecuencia'])

    def verify_widgets(self):
        try:
            assert self.tb_resultado
            assert self.tb_palabras_clave
            assert self.tb_identificadores
            assert self.txt_fuente  # Asegúrate de que el QTextEdit está cargado
            print("Widgets cargados correctamente.")
        except AttributeError as e:
            print(f"Error en la carga de widgets: {e}")
            raise

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setViewMode(QFileDialog.List)
        
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.ln_ruta_archivo.setText(file_path)
            self.process_file(file_path)

    def process_file(self, file_path):
        # Leer y mostrar el contenido del archivo en el QTextEdit
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
                self.txt_fuente.setPlainText(data)  # Mostrar el contenido en el QTextEdit
        except FileNotFoundError:
            return

        # Definir tokens y palabras clave
        tokens = [
            'SI', 'SINO', 'MIENTRAS', 'IMPRIMIR', 'INT', 'PARENTESIS_IZQUIERDO',
            'PARENTESIS_DERECHO', 'LLAVE_IZQUIERDA', 'LLAVE_DERECHA', 'IDENTIFICADOR',
            'NUMERO', 'ASIGNACION', 'MAS', 'MENOS', 'MULTIPLICACION', 'DIVISION',
            'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUALDAD',
            'DIFERENTE', 'AND', 'OR', 'PUNTO_Y_COMA', 'COMILLAS_DOBLES', 'COMENTARIO'
        ]

        palabras_clave = {
            'if': 'SI', 'else': 'SINO', 'while': 'MIENTRAS', 'print': 'IMPRIMIR',
            'int': 'INT'
        }

        conteo_identificadores = {}
        conteo_palabras_clave = {}

        def t_IDENTIFICADOR(t):
            r'[a-zA-Z_áéíóúñÁÉÍÓÚÑ][a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ]*'
            if t.value in palabras_clave:
                conteo_palabras_clave[t.value] = conteo_palabras_clave.get(t.value, 0) + 1
                t.type = palabras_clave[t.value]
            else:
                conteo_identificadores[t.value] = conteo_identificadores.get(t.value, 0) + 1
            return t

        t_NUMERO = r'\d+'
        t_ignore = ' \t\n'
        states = (('comment', 'exclusive'),)
        def t_comment(t):
            r'\/\*'
            t.lexer.begin('comment')
        def t_comment_content(t):
            r'[^\*]+'
            pass
        def t_comment_end(t):
            r'\*\/'
            t.lexer.begin('INITIAL')
        t_comment_ignore = ' \t\n'
        def t_comment_error(t):
            t.lexer.skip(1)
        def t_error(t):
            t.lexer.skip(1)

        lexer = lex.lex()

        lexer.input(data)

        # Limpiar las tablas antes de llenarlas
        self.tb_resultado.setRowCount(0)
        self.tb_palabras_clave.setRowCount(0)
        self.tb_identificadores.setRowCount(0)

        # Agregar tokens a la tabla tb_resultado
        for tok in lexer:
            tipo = tok.type
            valor = tok.value
            if tipo in palabras_clave.values():
                categoria = "Palabra Clave"
            elif tipo == 'IDENTIFICADOR':
                categoria = "Identificador"
            elif tipo == 'NUMERO':
                categoria = "Número"
            elif tipo in {'PARENTESIS_IZQUIERDO', 'PARENTESIS_DERECHO', 'LLAVE_IZQUIERDA', 'LLAVE_DERECHA', 'ASIGNACION',
                          'MAS', 'MENOS', 'MULTIPLICACION', 'DIVISION', 'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL',
                          'MENOR_IGUAL', 'IGUALDAD', 'DIFERENTE', 'AND', 'OR', 'PUNTO_Y_COMA', 'COMILLAS_DOBLES'}:
                categoria = "Operador/Delimitador"
            else:
                categoria = "Comentario"
            row_position = self.tb_resultado.rowCount()
            self.tb_resultado.insertRow(row_position)
            self.tb_resultado.setItem(row_position, 0, QTableWidgetItem(categoria))
            self.tb_resultado.setItem(row_position, 1, QTableWidgetItem(valor))

        # Agregar frecuencia de palabras clave a la tabla tb_palabras_clave
        for palabra_clave, count in conteo_palabras_clave.items():
            row_position = self.tb_palabras_clave.rowCount()
            self.tb_palabras_clave.insertRow(row_position)
            self.tb_palabras_clave.setItem(row_position, 0, QTableWidgetItem(palabra_clave))
            self.tb_palabras_clave.setItem(row_position, 1, QTableWidgetItem(str(count)))

        # Agregar frecuencia de identificadores a la tabla tb_identificadores
        for identificador, count in conteo_identificadores.items():
            row_position = self.tb_identificadores.rowCount()
            self.tb_identificadores.insertRow(row_position)
            self.tb_identificadores.setItem(row_position, 0, QTableWidgetItem(identificador))
            self.tb_identificadores.setItem(row_position, 1, QTableWidgetItem(str(count)))

    def export_to_txt(self):
        # Obtener la ruta de la carpeta actual
        carpeta_actual = os.getcwd()
        ruta_archivo = os.path.join(carpeta_actual, 'resultado.txt')
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as file:
                file.write("Tokens:\n")
                for row in range(self.tb_resultado.rowCount()):
                    tipo = self.tb_resultado.item(row, 0).text()
                    valor = self.tb_resultado.item(row, 1).text()
                    file.write(f"Tipo: {tipo} - Valor: {valor}\n")
                
                file.write("\nFrecuencia de Palabras Clave:\n")
                for row in range(self.tb_palabras_clave.rowCount()):
                    palabra_clave = self.tb_palabras_clave.item(row, 0).text()
                    frecuencia = self.tb_palabras_clave.item(row, 1).text()
                    file.write(f"{palabra_clave}: {frecuencia}\n")

                file.write("\nFrecuencia de Identificadores:\n")
                for row in range(self.tb_identificadores.rowCount()):
                    identificador = self.tb_identificadores.item(row, 0).text()
                    frecuencia = self.tb_identificadores.item(row, 1).text()
                    file.write(f"{identificador}: {frecuencia}\n")

            QMessageBox.information(self, "Exportación Completa", "El archivo de resultados ha sido exportado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error al exportar el archivo: {e}")
