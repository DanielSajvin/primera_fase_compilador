# Definir la tabla LL(1) como un diccionario
tabla_ll1 = {
    'S': {
        'if': ['IF_STMT'],
        'while': ['WHILE_STMT'],
        'for': ['FOR_STMT'],
        'def': ['FUNC_DEF'],
        'ID': ['STMT'],
        'print': ['PRINT_STMT'],
        'return': ['RETURN_STMT']
    },
    'IF_STMT': {
        'if': ['if', '(', 'COND', ')', ':', 'BLOCK', 'ELSE_PART']
    },
    'ELSE_PART': {
        'else': ['else', ':', 'BLOCK'],
        '$': []  # ε (vacío)
    },
    'WHILE_STMT': {
        'while': ['while', '(', 'COND', ')', ':', 'BLOCK']
    },
    'FOR_STMT': {
        'for': ['for', 'ID', 'in', 'EXPR', ':', 'BLOCK']
    },
    'FUNC_DEF': {
        'def': ['def', 'ID', '(', 'PARAMS', ')', ':', 'BLOCK']
    },
    'PARAMS': {
        'ID': ['ID', "PARAMS'"],
        ')': []  # ε (vacío)
    },
    "PARAMS'": {
        ',': [',', 'ID', "PARAMS'"],
        ')': []  # ε (vacío)
    },
    'COND': {
        'ID': ['EXPR'],
        'NUM': ['EXPR'],
        'True': ['EXPR'],
        'False': ['EXPR']
    },
    'EXPR': {
        'ID': ['TERM', "EXPR'"],
        'NUM': ['TERM', "EXPR'"],
        '(': ['(', 'EXPR', ')']
    },
    "EXPR'": {
        '+': ['+', 'TERM', "EXPR'"],
        '-': ['-', 'TERM', "EXPR'"],
        '==': ['==', 'TERM', "EXPR'"],
        ')': [],  # ε (vacío)
        ':': []  # ε (vacío)
    },
    'TERM': {
        'ID': ['FACTOR', "TERM'"],
        'NUM': ['FACTOR', "TERM'"]
    },
    "TERM'": {
        '*': ['*', 'FACTOR', "TERM'"],
        '/': ['/', 'FACTOR', "TERM'"],
        '+': [],  # ε (vacío)
        '-': [],  # ε (vacío)
        '==': [],  # ε (vacío)
        ')': [],  # ε (vacío)
        ':': []  # ε (vacío)
    },
    'FACTOR': {
        'ID': ['ID'],
        'NUM': ['NUM']
    },
    'STMT': {
        'ID': ['ID', '=', 'EXPR'],
        'print': ['PRINT_STMT']
    },
    'PRINT_STMT': {
        'print': ['print', '(', 'EXPR', ')']
    },
    'RETURN_STMT': {
        'return': ['return', 'EXPR']
    },
    'BLOCK': {
        'ID': ['STMT', "BLOCK'"],
        'print': ['STMT', "BLOCK'"],
        'return': ['STMT', "BLOCK'"],
        'if': ['STMT', "BLOCK'"],
        'while': ['STMT', "BLOCK'"],
        'for': ['STMT', "BLOCK'"],
        '$': []  # ε (vacío)
    },
    "BLOCK'": {
        'ID': ['STMT', "BLOCK'"],
        'print': ['STMT', "BLOCK'"],
        'return': ['STMT', "BLOCK'"],
        'if': ['STMT', "BLOCK'"],
        'while': ['STMT', "BLOCK'"],
        'for': ['STMT', "BLOCK'"],
        '$': []  # ε (vacío)
    }
}


def parser(tokens):
    # Iniciar la pila con el símbolo de entrada y el símbolo inicial 'S'
    pila = ['$', 'S']
    cursor = 0
    while len(pila) > 0:
        top = pila.pop()
        token_actual = tokens[cursor]

        if top == token_actual:  # Coincidencia de terminales incluyendo '$'
            print(f"Coincidencia: {top}")
            cursor += 1  # Consumir el token
        elif top in tabla_ll1:  # No terminal, buscar en la tabla LL(1)
            if token_actual in tabla_ll1[top]:
                regla = tabla_ll1[top][token_actual]
                if regla:
                    print(f"Aplicar regla: {top} -> {regla}")
                    pila.extend(reversed(regla))  # Añadir regla a la pila
                else:
                    print(f"Aplicar regla: {top} -> ε (vacío)")
            else:
                print(f"Error: token inesperado {token_actual}, esperado {top}")
                return False
        else:
            print(f"Error: símbolo no reconocido {top}")
            return False

    if cursor == len(tokens):
        print("Entrada aceptada.")
        return True
    else:
        print(f"Error: tokens sobrantes. Cursor en: {cursor}, tokens restantes: {tokens[cursor:]}")
        return False


# Ejemplo de tokens de entrada para un bloque de código Python
tokens = ['def', 'ID', '(', 'ID', ')', ':', 'ID', '=', 'NUM', '+', 'NUM', '$']

# Llamada al parser
parser(tokens)
