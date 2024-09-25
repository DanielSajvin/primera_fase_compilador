# Definir la tabla LL(1) como un diccionario
tabla_ll1 = {
    'S': {
        'if': ['IF_STMT']
    },
    'IF_STMT': {
        'if': ['if', '(', 'COND', ')', '{', 'STMT', '}', 'else', '{', 'STMT', '}']
    },
    'COND': {
        'ID': ['EXPR'],
        'NUM': ['EXPR']
    },
    'EXPR': {
        'ID': ['TERM', "EXPR'"],
        'NUM': ['TERM', "EXPR'"]
    },
    'EXPR\'': {
        '+': ['+', 'TERM', "EXPR'"],
        ')': [],  # ε (vacío)
        '}': []  # ε (vacío)
    },
    'TERM': {
        'ID': ['FACTOR', "TERM'"],
        'NUM': ['FACTOR', "TERM'"]
    },
    'TERM\'': {
        '*': ['*', 'FACTOR', "TERM'"],
        '+': [],  # ε (vacío)
        ')': [],  # ε (vacío)
        '}': []  # ε (vacío)
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
        'print': ['print', '(', 'ID', ')']
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
                print(
                    f"Error: token inesperado {token_actual}, esperado {top}")
                return False
        else:
            print(f"Error: símbolo no reconocido {top}")
            return False

    if cursor == len(tokens):
        print("Entrada aceptada.")
        return True
    else:
        print(
            f"Error: tokens sobrantes. Cursor en: {cursor}, tokens restantes: {tokens[cursor:]}")
        return False


# Ejemplo de tokens de entrada
tokens = ['if', '(', 'ID', '+', 'NUM', ')',
          '{', 'ID', '=', 'ID', '*', 'NUM', '}', 'else', '{', 'print', '(', 'ID', ')', '}', '$']

# Llamada al parser
parser(tokens)
