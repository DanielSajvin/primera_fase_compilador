from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap
from estructura_base import definir_estructura_base  # Importar la nueva función
from arbol_derivacion import dibujar_arbol  # Importar la función para dibujar el árbol
import traceback
import os
import ply.lex as lex
import ply.yacc as yacc
import re

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
    "DOS_PUNTOS",  # Se agrega el token para el símbolo :
    "MAS",
    "MENOS",
    "MULTIPLICACION",
    "DIVISION",
    "PARENTESIS_IZQUIERDO",
    "PARENTESIS_DERECHO",
    "LLAVE_IZQUIERDA",
    "LLAVE_DERECHA",
    "PUNTO_Y_COMA",
    "IGUALDAD",
    "DIFERENTE",
    "PORCENTAJE",  # Para el operador %
    "CADENA"
]

# Mapeo de palabras clave a tokens
palabras_clave = {
    "if": "SI",
    "else": "SINO",
    "print": "IMPRIMIR",
}

# Agregar palabras clave al conjunto de tokens
tokens += list(set(palabras_clave.values()))

# Definición de expresiones regulares para tokens simples
t_ASIGNACION = r'='
t_DOS_PUNTOS = r':'  # Definición para los dos puntos (:)
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_PARENTESIS_IZQUIERDO = r'\('
t_PARENTESIS_DERECHO = r'\)'
t_LLAVE_IZQUIERDA = r'\{'
t_LLAVE_DERECHA = r'\}'
t_PUNTO_Y_COMA = r';'
t_IGUALDAD = r'=='
t_DIFERENTE = r'!='
t_PORCENTAJE = r'%'


def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value.strip('"')
    return t


def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in palabras_clave:
        t.type = palabras_clave[t.value]
        conteo_palabras_clave[t.value] = conteo_palabras_clave.get(
            t.value, 0) + 1
    else:
        conteo_identificadores[t.value] = conteo_identificadores.get(
            t.value, 0) + 1
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos


def t_error(t):
    error_message = f"Error léxico en línea {t.lineno}: Carácter ilegal '{t.value[0]}'"
    error_list.append(error_message)  # Guardar errores en la lista
    t.lexer.skip(1)


# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Construcción del lexer
lexer_instance = lex.lex()

# Reglas de la gramática para el parser


def p_program(p):
    '''program : statement_list'''
    derivations.append(f'program -> statement_list')


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        derivations.append(f'statement_list -> statement')
    else:
        derivations.append(f'statement_list -> statement_list statement')


def p_statement(p):
    '''statement : expression PUNTO_Y_COMA
                 | SI PARENTESIS_IZQUIERDO expression PARENTESIS_DERECHO DOS_PUNTOS statement_list
                 | SI PARENTESIS_IZQUIERDO expression PARENTESIS_DERECHO DOS_PUNTOS statement_list SINO DOS_PUNTOS statement_list
                 | IMPRIMIR PARENTESIS_IZQUIERDO CADENA PARENTESIS_DERECHO PUNTO_Y_COMA'''
    if len(p) == 3:
        derivations.append(f'statement -> expression PUNTO_Y_COMA')
    elif len(p) == 7:
        derivations.append(f'statement -> SI ( expression ) : statement_list')
    elif len(p) == 11:
        derivations.append(
            f'statement -> SI ( expression ) : statement_list SINO : statement_list')
    else:
        derivations.append(f'statement -> IMPRIMIR ( CADENA ) PUNTO_Y_COMA')


def p_expression(p):
    '''expression : term
                  | expression MAS term
                  | expression MENOS term
                  | expression PORCENTAJE term
                  | expression IGUALDAD term
                  | expression DIFERENTE term'''
    if len(p) == 2:
        derivations.append(f'expression -> term')
    else:
        derivations.append(f'expression -> expression {p[2]} term')


def p_term(p):
    '''term : IDENTIFICADOR
            | NUMERO'''
    derivations.append(f'term -> {p[1]}')


def p_error(p):
    if p:
        error_message = f"Error sintáctico en token '{p.value}' en la línea {p.lineno}"
    else:
        error_message = "Error sintáctico en EOF"
    error_list.append(error_message)


# Construcción del parser
parser_instance = yacc.yacc()

# Listas para guardar derivaciones y errores
derivations = []
error_list = []


class MainMenuPrincipal(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainMenuPrincipal, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.verify_widgets()

        # Conectar botones a funciones
        self.btn_buscar.clicked.connect(self.open_file)
        self.btn_exportar.clicked.connect(self.export_to_svg)
        self.btn_buscar_2.clicked.connect(self.open_file)

        self.tb_resultado.setColumnCount(4)
        self.tb_resultado.setHorizontalHeaderLabels(
            ["Tipo", "Valor", "Línea", "Posición"])
        self.tb_palabras_clave.setColumnCount(2)
        self.tb_palabras_clave.setHorizontalHeaderLabels(
            ["Valor", "Frecuencia"])
        self.tb_identificadores.setColumnCount(2)
        self.tb_identificadores.setHorizontalHeaderLabels(
            ["Valor", "Frecuencia"])

    def verify_widgets(self):
        try:
            assert self.tb_resultado
            assert self.tb_palabras_clave
            assert self.tb_identificadores
            assert self.txt_fuente
            assert self.txt_errores
            assert self.txt_fuente_2
            assert self.txt_fuente_3
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
        self.txt_fuente_2.clear()
        self.txt_fuente_3.clear()
        self.tb_resultado.setRowCount(0)
        self.tb_palabras_clave.setRowCount(0)
        self.tb_identificadores.setRowCount(0)

        # Limpiar las listas de derivaciones y errores del parser
        derivations.clear()
        error_list.clear()

        # Definir la estructura base de la expresión
        estructura_base = definir_estructura_base(data)
        self.txt_fuente_2.setPlainText(estructura_base)

        # Extraer las expresiones del texto de manera flexible
        expresiones = self.extraer_expresiones(data)

        # Llamar a la función para dibujar y mostrar el árbol con las expresiones dinámicas
        self.dibujar_y_mostrar_arbol(estructura_base, expresiones)

        # Lexical analysis
        lexer_instance.input(data)
        while True:
            tok = lexer_instance.token()
            if not tok:
                break
            row_position = self.tb_resultado.rowCount()
            self.tb_resultado.insertRow(row_position)
            self.tb_resultado.setItem(
                row_position, 0, QTableWidgetItem(tok.type))
            self.tb_resultado.setItem(
                row_position, 1, QTableWidgetItem(str(tok.value)))
            self.tb_resultado.setItem(
                row_position, 2, QTableWidgetItem(str(tok.lineno)))
            self.tb_resultado.setItem(
                row_position, 3, QTableWidgetItem(str(tok.lexpos)))

        # Mostrar errores léxicos
        if error_list:
            for error in error_list:
                self.txt_errores.append(error)

        # Parser analysis
        result = parser_instance.parse(data, lexer=lexer_instance)

        # Mostrar reglas de derivación
        if derivations:
            for derivation in derivations:
                self.txt_fuente_2.append(derivation)

        # Mostrar contenido de parser.out
        self.show_parser_out()

        # Mostrar errores sintácticos
        if error_list:
            for error in error_list:
                self.txt_fuente_3.append(error)

        # Llenar tabla de palabras clave con su frecuencia
        for palabra, count in conteo_palabras_clave.items():
            row_position = self.tb_palabras_clave.rowCount()
            self.tb_palabras_clave.insertRow(row_position)
            self.tb_palabras_clave.setItem(
                row_position, 0, QTableWidgetItem(palabra))
            self.tb_palabras_clave.setItem(
                row_position, 1, QTableWidgetItem(str(count)))

        # Llenar tabla de identificadores con su frecuencia
        for identificador, count in conteo_identificadores.items():
            row_position = self.tb_identificadores.rowCount()
            self.tb_identificadores.insertRow(row_position)
            self.tb_identificadores.setItem(
                row_position, 0, QTableWidgetItem(identificador))
            self.tb_identificadores.setItem(
                row_position, 1, QTableWidgetItem(str(count)))

    def show_parser_out(self):
        """Lee el contenido del archivo parser.out y lo muestra en txt_fuente_2"""
        try:
            with open("parser.out", "r") as f:
                content = f.read()
                self.txt_fuente_2.append("\n--- Contenido de parser.out ---\n")
                self.txt_fuente_2.append(content)
        except FileNotFoundError:
            self.txt_fuente_2.append("\n--- parser.out no encontrado ---\n")

    def dibujar_y_mostrar_arbol(self, estructura_base, expresiones):
        try:
            # Dibujar el árbol de derivación, pasando tanto estructura_base como expresiones
            imagen_arbol = dibujar_arbol(estructura_base, expresiones)

            if not imagen_arbol or not os.path.exists(imagen_arbol):
                print("Error: No se pudo generar la imagen del árbol de derivación.")
                self.label_arbol.setText("Error: No se pudo generar la imagen.")
                return

            print(f"Imagen generada correctamente en: {imagen_arbol}")

            # Mostrar el árbol en label_arbol
            pixmap = QPixmap(imagen_arbol)
            if pixmap.isNull():
                print("Error al cargar la imagen del árbol.")
                self.label_arbol.setText("Error: No se pudo cargar el árbol de derivación.")
            else:
                # Obtener el tamaño actual del QLabel
                label_width = self.label_arbol.width()
                label_height = self.label_arbol.height()

                # Escalar la imagen para que se ajuste al tamaño del QLabel
                scaled_pixmap = pixmap.scaled(label_width, label_height, aspectRatioMode=True)  # Mantener proporción
                self.label_arbol.setPixmap(scaled_pixmap)
                self.label_arbol.setScaledContents(True)  # Asegura que la imagen se ajuste al tamaño del QLabel

        except Exception as e:
            print("Ocurrió un error al dibujar o mostrar el árbol.")
            import traceback
            traceback.print_exc()

    def extraer_expresiones(self, data):
        expresiones = {}

        # Buscar todas las condiciones que están entre paréntesis
        condiciones = re.findall(r'\((.*?)\)', data)

        # Buscar todos los cuerpos que están entre llaves, incluyendo el contenido entre ellas
        cuerpos = re.findall(r'\{(.*?)\}', data, re.DOTALL)

        # Asignar las condiciones encontradas al diccionario
        for i, condicion in enumerate(condiciones):
            expresiones[f'condicion_{i + 1}'] = condicion.strip()

        # Asignar los cuerpos encontrados al diccionario
        for i, cuerpo in enumerate(cuerpos):
            expresiones[f'cuerpo_{i + 1}'] = cuerpo.strip()

        # Asegurarse de que haya valores por defecto en caso de que no se encuentren
        expresiones.setdefault('condicion_1', 'Condición no encontrada')
        expresiones.setdefault('cuerpo_1', 'Cuerpo no encontrado')

        return expresiones

    def export_to_svg(self):
        # Código de exportación a SVG
        pass

    def show_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.show()
