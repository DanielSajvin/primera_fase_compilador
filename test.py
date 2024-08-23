import ply.lex as lex

# Diccionarios para contar la frecuencia de identificadores y palabras clave
conteo_identificadores = {}
conteo_palabras_clave = {}

# Definición de tokens
tokens = [
    'SI',                     # if
    'SINO',                   # else
    'MIENTRAS',               # while
    'IMPRIMIR',               # print
    'PARENTESIS_IZQUIERDO',   # (
    'PARENTESIS_DERECHO',     # )
    'LLAVE_IZQUIERDA',        # {
    'LLAVE_DERECHA',          # }
    'IDENTIFICADOR',          # Identificadores
    'NUMERO',                 # Números
    'ASIGNACION',             # =
    'MAS',                    # +
    'MENOS',                  # -
    'MULTIPLICACION',         # *
    'DIVISION',               # /
    'COMENTARIO'              # Comentarios
]

# Mapeo de palabras clave a tokens
palabras_clave = {
    'if': 'SI',
    'else': 'SINO',
    'while': 'MIENTRAS',
    'print': 'IMPRIMIR'
}

# Reglas para los tokens simples
t_PARENTESIS_IZQUIERDO = r'\('
t_PARENTESIS_DERECHO = r'\)'
t_LLAVE_IZQUIERDA = r'\{'
t_LLAVE_DERECHA = r'\}'
t_ASIGNACION = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'

# Regla para manejar identificadores y palabras clave, incluyendo caracteres especiales
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_áéíóúñÁÉÍÓÚÑ][a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ]*'
    global conteo_identificadores, conteo_palabras_clave
    if t.value in palabras_clave:
        conteo_palabras_clave[t.value] = conteo_palabras_clave.get(t.value, 0) + 1
        t.type = palabras_clave[t.value]  # Usar el nombre de token correcto
    else:
        conteo_identificadores[t.value] = conteo_identificadores.get(t.value, 0) + 1
    return t

# Regla para manejar números
t_NUMERO = r'\d+'

# Ignorar espacios en blanco
t_ignore = ' \t\n'

# Definir el estado para manejar los comentarios
states = (
    ('comment', 'exclusive'),
)

# Regla para iniciar un comentario
def t_comment(t):
    r'\/\*'
    t.lexer.begin('comment')

# Regla para manejar el contenido de los comentarios
def t_comment_content(t):
    r'[^\*]+'
    pass  # Ignorar el contenido del comentario

# Regla para terminar un comentario
def t_comment_end(t):
    r'\*\/'
    t.lexer.begin('INITIAL')

# Ignorar cualquier cosa dentro del estado de comentario
t_comment_ignore = ' \t\n'

# Manejo de errores en el estado de comentario
def t_comment_error(t):
    t.lexer.skip(1)

# Manejo de errores para caracteres ilegales
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Leer el archivo de entrada con codificación UTF-8
print("Leyendo el archivo 'test2.txt'...")
try:
    with open('test.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    print("Archivo leído exitosamente.")
except FileNotFoundError:
    print("Error: El archivo 'test2.txt' no se encontró.")
    exit(1)

# Darle al lexer algunos datos de entrada
print("Datos de entrada")
lexer.input(data)

# Tokenizar: Extraer y mostrar los tokens
for tok in lexer:
    print(tok)

print("Tokenización completada.")

# Imprimir el resultado de las frecuencias
print("\nFrecuencia de Palabras Clave:")
for palabra_clave, count in conteo_palabras_clave.items():
    print(f"{palabra_clave}: {count}")

print("\nFrecuencia de Identificadores:")
for identificador, count in conteo_identificadores.items():
    print(f"{identificador}: {count}")