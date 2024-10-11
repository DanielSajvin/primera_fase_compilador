# estructura_base.py

def definir_estructura_base(expresion):
    """
    Esta función analiza la expresión y devuelve la estructura base correspondiente.
    Manejaremos expresiones condicionales y ciclos básicos como 'if', 'while', y 'do'.
    """
    expresion = expresion.strip()

    # Para expresiones condicionales 'if-else'
    if expresion.startswith("if") and "else" in expresion:
        return "S -> if (E) { C } else { C }"

    # Para expresiones condicionales 'if' sin 'else'
    elif expresion.startswith("if") and "else" not in expresion:
        return "S -> if (E) { C }"

    # Para ciclos 'while'
    elif expresion.startswith("while"):
        return "S -> while (E) { C }"

    # Para ciclos 'do-while'
    elif expresion.startswith("do"):
        return "S -> do { C } while (E);"





    # Si no se reconoce la expresión
    else:
        return "Estructura no reconocida o expresión no soportada"
