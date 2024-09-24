from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt5.uic import loadUiType
import os
import ply.lex as lex
import cairo

Ui_MainWindow, QMainWindow = loadUiType(
    os.path.join(os.path.dirname(__file__), "views", "compiler.ui")
)

# Diccionarios para contar la frecuencia de identificadores y palabras clave
conteo_identificadores = {}
conteo_palabras_clave = {}

# Definición de tokens
tokens = [
    "IDENTIFICADOR",
    "NUMERO",
    "ASIGNACION",
    "MAS",
    "MENOS",
    "MULTIPLICACION",
    "DIVISION",
    "PARENTESIS_IZQUIERDO",
    "PARENTESIS_DERECHO",
    "LLAVE_IZQUIERDA",
    "LLAVE_DERECHA",
    "PUNTO_Y_COMA",
    "COMILLAS_DOBLES",
    "CADENA",
    "MAYOR_QUE",
    "MENOR_QUE",
    "MAYOR_IGUAL",
    "MENOR_IGUAL",
    "IGUALDAD",
    "DIFERENTE",
    "AND",
    "OR",
    "PUNTO",  # Agregado para reconocer '.'
]

# Mapeo de palabras clave a tokens
palabras_clave = {
    "if": "SI",
    "else": "SINO",
    "while": "MIENTRAS",
    "print": "IMPRIMIR",
    "entero": "ENTERO",
    "decimal": "DECIMAL",
    "si": "SI",
    "sino": "SINO",
    "mientras": "MIENTRAS",
    "imprimir": "IMPRIMIR",
}

# Agregar palabras clave al conjunto de tokens
tokens += list(set(palabras_clave.values()))

class MainMenuPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainMenuPrincipal, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.verify_widgets()

        self.btn_buscar.clicked.connect(self.open_file)
        self.btn_exportar.clicked.connect(self.export_to_svg)

        self.tb_resultado.setColumnCount(4)
        self.tb_resultado.setHorizontalHeaderLabels(["Tipo", "Valor", "Línea", "Posición"])
        self.tb_palabras_clave.setColumnCount(2)
        self.tb_palabras_clave.setHorizontalHeaderLabels(["Valor", "Frecuencia"])
        self.tb_identificadores.setColumnCount(2)
        self.tb_identificadores.setHorizontalHeaderLabels(["Valor", "Frecuencia"])

    def verify_widgets(self):
        try:
            assert self.tb_resultado
            assert self.tb_palabras_clave
            assert self.tb_identificadores
            assert self.txt_fuente
            assert self.txt_errores
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
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
                self.txt_fuente.setPlainText(data)
        except FileNotFoundError:
            return

        # Limpiar contadores y áreas de texto
        conteo_identificadores.clear()
        conteo_palabras_clave.clear()
        self.txt_errores.clear()
        self.tb_resultado.setRowCount(0)
        self.tb_palabras_clave.setRowCount(0)
        self.tb_identificadores.setRowCount(0)

        # Definición de tokens con expresiones regulares
        t_ignore = ' \t'  # Ignorar espacios y tabulaciones

        t_ASIGNACION = r'='
        t_MAS = r'\+'
        t_MENOS = r'-'
        t_MULTIPLICACION = r'\*'
        t_DIVISION = r'/'
        t_PARENTESIS_IZQUIERDO = r'\('
        t_PARENTESIS_DERECHO = r'\)'
        t_LLAVE_IZQUIERDA = r'\{'
        t_LLAVE_DERECHA = r'\}'
        t_PUNTO_Y_COMA = r';'
        t_COMILLAS_DOBLES = r'\"'
        t_MAYOR_QUE = r'>'
        t_MENOR_QUE = r'<'
        t_MAYOR_IGUAL = r'>='
        t_MENOR_IGUAL = r'<='
        t_IGUALDAD = r'=='
        t_DIFERENTE = r'!='
        t_AND = r'&&'
        t_OR = r'\|\|'
        t_PUNTO = r'\.'

        def t_CADENA(t):
            r'\"([^\\\n]|(\\.))*?\"'
            t.value = t.value.strip('"')  # Eliminar comillas dobles de inicio y fin
            return t

        def t_NUMERO(t):
            r'\d+(\.\d+)?'
            if '.' in t.value:
                t.type = 'DECIMAL'
                t.value = float(t.value)
            else:
                t.type = 'ENTERO'
                t.value = int(t.value)
            return t

        def t_IDENTIFICADOR(t):
            r'[a-zA-Z_áéíóúñÁÉÍÓÚÑ][a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ]*'
            if t.value in palabras_clave:
                t.type = palabras_clave[t.value]
                conteo_palabras_clave[t.value] = conteo_palabras_clave.get(t.value, 0) + 1
            else:
                conteo_identificadores[t.value] = conteo_identificadores.get(t.value, 0) + 1
            return t

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        def t_error(t):
            error_message = (
                f"Error de escaneo. Carácter ilegal '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}"
            )
            self.txt_errores.append(error_message)
            t.lexer.skip(1)

        lexer = lex.lex()
        lexer.input(data)

        while True:
            tok = lexer.token()
            if not tok:
                break
            row_position = self.tb_resultado.rowCount()
            self.tb_resultado.insertRow(row_position)
            self.tb_resultado.setItem(row_position, 0, QTableWidgetItem(tok.type))
            self.tb_resultado.setItem(row_position, 1, QTableWidgetItem(str(tok.value)))
            self.tb_resultado.setItem(row_position, 2, QTableWidgetItem(str(tok.lineno)))
            self.tb_resultado.setItem(row_position, 3, QTableWidgetItem(str(tok.lexpos)))

        # Llenar tabla de palabras clave con su frecuencia
        for palabra, count in conteo_palabras_clave.items():
            row_position = self.tb_palabras_clave.rowCount()
            self.tb_palabras_clave.insertRow(row_position)
            self.tb_palabras_clave.setItem(row_position, 0, QTableWidgetItem(palabra))
            self.tb_palabras_clave.setItem(row_position, 1, QTableWidgetItem(str(count)))

        # Llenar tabla de identificadores con su frecuencia
        for identificador, count in conteo_identificadores.items():
            row_position = self.tb_identificadores.rowCount()
            self.tb_identificadores.insertRow(row_position)
            self.tb_identificadores.setItem(row_position, 0, QTableWidgetItem(identificador))
            self.tb_identificadores.setItem(row_position, 1, QTableWidgetItem(str(count)))

    def export_to_svg(self):
        try:
            ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "SVG Files (*.svg)")

            if ruta_archivo:
                # Definir el tamaño del SVG (Ajustar según el contenido)
                width, height = 1500, 10000
                surface = cairo.SVGSurface(ruta_archivo, width, height)
                context = cairo.Context(surface)

                # Configuración de fuente
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(10)

                # Posiciones iniciales para las tres tablas y errores
                start_x1, start_y1 = 50, 50  # Primera tabla - Izquierda (tb_resultado)
                start_x2, start_y2 = 700, 50  # Segunda tabla - Centro (tb_palabras_clave)
                start_x3, start_y3 = 1200, 50  # Tercera tabla - Derecha (tb_identificadores)
                start_x4, start_y4 = 700, 380  # Errores - Debajo de las tablas

                # Función para dibujar una tabla en el contexto SVG
                def draw_table(table_widget, title, start_x, start_y):
                    context.move_to(start_x, start_y)
                    context.show_text(title)
                    context.stroke()

                    row_count = table_widget.rowCount()
                    column_count = table_widget.columnCount()

                    cell_width = 150  # Ajustar el ancho de las celdas
                    cell_height = 25  # Ajustar la altura de las celdas

                    # Dibujar encabezado de la tabla
                    for col in range(column_count):
                        rect_x = start_x + col * cell_width
                        rect_y = start_y + cell_height
                        text = table_widget.horizontalHeaderItem(col).text()

                        context.rectangle(rect_x, rect_y, cell_width, cell_height)
                        context.move_to(rect_x + 5, rect_y + 15)  # Añade margen
                        context.show_text(text)
                        context.stroke()

                    # Dibujar filas de la tabla
                    for row in range(row_count):
                        for col in range(column_count):
                            rect_x = start_x + col * cell_width
                            rect_y = start_y + (row + 2) * cell_height  # +2 para dejar espacio para el encabezado

                            item = table_widget.item(row, col)
                            if item is not None:
                                text = item.text()
                                # Si es la columna de "Posición", modificar para que muestre "Línea X" en lugar de la posición.
                                if col == 2:  # Asumiendo que la columna 2 es la de "Posición"
                                    text = f"Línea {text}"  # Cambia "Posición" por "Línea"
                            else:
                                text = ""

                            context.rectangle(rect_x, rect_y, cell_width, cell_height)
                            context.move_to(rect_x + 5, rect_y + 15)  # Añade margen
                            context.show_text(text)
                            context.stroke()

                # Función para dibujar los errores desde txt_errores
                def draw_errors(text_widget, title, start_x, start_y):
                    context.move_to(start_x, start_y)
                    context.show_text(title)
                    context.stroke()

                    errors = text_widget.toPlainText().split('\n')
                    for i, error in enumerate(errors):
                        context.move_to(start_x, start_y + (i + 1) * 20)  # Ajustar la posición de las líneas
                        context.show_text(error)
                        context.stroke()

                # Dibujar las tablas
                draw_table(self.tb_resultado, "Resultado:", start_x1, start_y1)
                draw_table(self.tb_palabras_clave, "Palabras Clave:", start_x2, start_y2)
                draw_table(self.tb_identificadores, "Identificadores:", start_x3, start_y3)

                # Dibujar los errores
                draw_errors(self.txt_errores, "Errores:", start_x4, start_y4)

                # Finalizar la creación del archivo SVG
                surface.finish()
                QMessageBox.information(self, "Exportar a SVG", "El archivo SVG ha sido guardado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el archivo SVG: {str(e)}")

    def show_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.show()
