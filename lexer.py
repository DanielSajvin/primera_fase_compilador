from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QTextEdit,
    QMessageBox,
)
from PyQt5.uic import loadUiType
import os
import ply.lex as lex
import cairo 


Ui_MainWindow, QMainWindow = loadUiType(
    os.path.join(os.path.dirname(__file__), "views", "principal.ui")
)

# Diccionarios para contar la frecuencia de identificadores y palabras clave
conteo_identificadores = {}
conteo_palabras_clave = {}

# Definición de tokens
tokens = [
    "SI",  # if
    "SINO",  # else
    "MIENTRAS",  # while
    "IMPRIMIR",  # print
    "IDENTIFICADOR",  # Identificadores
    "NUMERO",  # Números
    "ASIGNACION",  # =
    "MAS",  # +
    "MENOS",  # -
    "MULTIPLICACION",  # *
    "DIVISION",  # /
    "PARENTESIS_IZQUIERDO",  # (
    "PARENTESIS_DERECHO",  # )
    "LLAVE_IZQUIERDA",  # {
    "LLAVE_DERECHA",  # }
    "PUNTO_Y_COMA",  # ;
    "COMILLAS_DOBLES",  # "
    "CADENA",  # Cadenas de texto
    "COMENTARIO",  # Comentarios
    "MAYOR_QUE",  # >
    "MENOR_QUE",  # <
    "MAYOR_IGUAL",  # >=
    "MENOR_IGUAL",  # <=
    "IGUALDAD",  # ==
    "DIFERENTE",  # !=
    "AND",  # &&
    "OR",  # ||
]

# Mapeo de palabras clave a tokens
palabras_clave = {"if": "SI", "else": "SINO", "while": "MIENTRAS", "print": "IMPRIMIR"}


class MainMenuPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainMenuPrincipal, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.verify_widgets()

        self.btn_buscar.clicked.connect(self.open_file)
        self.btn_exportar.clicked.connect(self.export_to_svg)

        self.tb_resultado.setColumnCount(2)
        self.tb_resultado.setHorizontalHeaderLabels(["Tipo", "Valor"])
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

        # Definición de tokens
        conteo_identificadores.clear()
        conteo_palabras_clave.clear()

        # Reglas para los tokens simples
        t_PARENTESIS_IZQUIERDO = r"\("
        t_PARENTESIS_DERECHO = r"\)"
        t_LLAVE_IZQUIERDA = r"\{"
        t_LLAVE_DERECHA = r"\}"
        t_ASIGNACION = r"="
        t_MAS = r"\+"
        t_MENOS = r"-"
        t_MULTIPLICACION = r"\*"
        t_DIVISION = r"/"
        t_PUNTO_Y_COMA = r";"
        t_COMILLAS_DOBLES = r"\""
        t_MAYOR_QUE = r">"
        t_MENOR_QUE = r"<"
        t_MAYOR_IGUAL = r">="
        t_MENOR_IGUAL = r"<="
        t_IGUALDAD = r"=="
        t_DIFERENTE = r"!="
        t_AND = r"&&"
        t_OR = r"\|\|"

        # Regla para manejar identificadores y palabras clave, incluyendo caracteres especiales
        def t_IDENTIFICADOR(t):
            r"[a-zA-Z_áéíóúñÁÉÍÓÚÑ][a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ]*"
            global conteo_identificadores, conteo_palabras_clave
            if t.value in palabras_clave:
                conteo_palabras_clave[t.value] = (
                    conteo_palabras_clave.get(t.value, 0) + 1
                )
                t.type = palabras_clave[t.value] 
            else:
                conteo_identificadores[t.value] = (
                    conteo_identificadores.get(t.value, 0) + 1
                )
            return t

        # Regla para manejar números
        t_NUMERO = r"\d+"

        # Regla para manejar cadenas de texto
        def t_CADENA(t):
            r"\"([^\\\n]|(\\.))*?\" "
            return t

        # Definir el estado para manejar los comentarios
        states = (("comment", "exclusive"),)

        # Regla para iniciar un comentario
        def t_comment(t):
            r"\/\*"
            t.lexer.begin("comment")

        # Regla para manejar el contenido de los comentarios
        def t_comment_content(t):
            r"[^\*]+"
            pass  # Ignorar el contenido del comentario

        # Regla para terminar un comentario
        def t_comment_end(t):
            r"\*\/"
            t.lexer.begin("INITIAL")

        # Ignorar cualquier cosa dentro del estado de comentario
        t_comment_ignore = " \t\n"

        # Manejo de errores en el estado de comentario
        def t_comment_error(t):
            t.lexer.skip(1)

        # Manejo de errores para caracteres ilegales
        def t_error(t,):
             print(
               f"Error de escaneo. Carácter ilegal '{t.value[0]}' en la posición {t.lexpos}"
             )
             t.lexer.skip(1)

        # Construir el lexer
        lexer = lex.lex()

        # Darle al lexer algunos datos de entrada
        lexer.input(data)

        # Limpiar las tablas antes de agregar nuevos datos
        self.tb_resultado.setRowCount(0)
        self.tb_palabras_clave.setRowCount(0)
        self.tb_identificadores.setRowCount(0)

        # Tokenizar: Extraer y mostrar los tokens
        for tok in lexer:
            self.tb_resultado.insertRow(self.tb_resultado.rowCount())
            self.tb_resultado.setItem(
                self.tb_resultado.rowCount() - 1, 0, QTableWidgetItem(tok.type)
            )
            self.tb_resultado.setItem(
                self.tb_resultado.rowCount() - 1, 1, QTableWidgetItem(tok.value)
            )

        # Imprimir el resultado de las frecuencias
        self.tb_palabras_clave.setRowCount(0)
        for palabra_clave, count in conteo_palabras_clave.items():
            self.tb_palabras_clave.insertRow(self.tb_palabras_clave.rowCount())
            self.tb_palabras_clave.setItem(
                self.tb_palabras_clave.rowCount() - 1,
                0,
                QTableWidgetItem(palabra_clave),
            )
            self.tb_palabras_clave.setItem(
                self.tb_palabras_clave.rowCount() - 1, 1, QTableWidgetItem(str(count))
            )



        self.tb_identificadores.setRowCount(0)
        for identificador, count in conteo_identificadores.items():
            self.tb_identificadores.insertRow(self.tb_identificadores.rowCount())
            self.tb_identificadores.setItem(
                self.tb_identificadores.rowCount() - 1,
                0,
                QTableWidgetItem(identificador),
            )
            self.tb_identificadores.setItem(
                self.tb_identificadores.rowCount() - 1, 1, QTableWidgetItem(str(count))
            )

    def export_to_svg(self):
        try:
            ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "SVG Files (*.svg)")

            if ruta_archivo:
                width, height = 12000, 400000  # Ajustar el tamaño del documento SVG para acomodar las tres tablas
                surface = cairo.SVGSurface(ruta_archivo, width, height)
                context = cairo.Context(surface)

                # Ajustes de fuente y posición inicial
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(12)

                # Posiciones iniciales para las tres tablas
                start_x1, start_y1 = 50, 50   # Primera tabla - Izquierda
                start_x2, start_y2 = 800, 50  # Segunda tabla - Centro
                start_x3, start_y3 = 1500, 50  # Tercera tabla - Derecha

                # Función para dibujar una tabla en el contexto SVG
                def draw_table(table_widget, title, start_x, start_y):
                    context.move_to(start_x, start_y)
                    context.show_text(title)
                    context.stroke()
                    
                    row_count = table_widget.rowCount()
                    column_count = table_widget.columnCount()

                    cell_width = 300
                    cell_height = 20

                    for row in range(row_count + 1):  # Incluye la fila de encabezado
                        for col in range(column_count):
                            rect_x = start_x + col * cell_width
                            rect_y = start_y + (row + 1) * cell_height

                            if row == 0:  # Dibujar encabezado
                                text = table_widget.horizontalHeaderItem(col).text()
                            else:  # Dibujar contenido
                                text = table_widget.item(row - 1, col).text()

                            context.rectangle(rect_x, rect_y, cell_width, cell_height)
                            context.move_to(rect_x + 5, rect_y + 15)  # Añade margen
                            context.show_text(text)

                            context.stroke()

                # Dibujar las tres tablas en el documento SVG en posiciones distintas
                draw_table(self.tb_resultado, "Resultado:", start_x1, start_y1)  # Primera tabla - Izquierda
                draw_table(self.tb_palabras_clave, "Palabras Clave:", start_x2, start_y2)  # Segunda tabla - Centro
                draw_table(self.tb_identificadores, "Identificadores:", start_x3, start_y3)  # Tercera tabla - Derecha

                # Finalizar la creación del archivo SVG
                surface.finish()
                QMessageBox.information(self, "Exportar a SVG", "El archivo SVG ha sido guardado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el archivo SVG: {str(e)}")
