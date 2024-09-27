import graphviz
import os

def dibujar_arbol(estructura_base, expresiones):
    try:
        dot = graphviz.Digraph(comment='Árbol de Derivación', format='png')

        # Configuración para mejorar la apariencia del árbol
        dot.attr(rankdir='TB', size='5,5')  # Dirigir de arriba hacia abajo (top-bottom)
        dot.attr('node', shape='ellipse', fontsize='12')  # Definir forma de los nodos y tamaño de fuente

        # Nodo raíz
        dot.node('S', 'S')

        # Verificar si es una expresión if-else
        if 'if' in estructura_base:
            dot.node('1', 'if (E)')
            dot.node('2', '{ C }')
            dot.node('3', 'else { C }')

            # Agregar las expresiones dinámicas para if-else
            condicion_1 = expresiones.get('condicion_1', 'Condición no encontrada')
            cuerpo_1 = expresiones.get('cuerpo_1', 'Cuerpo no encontrado')
            condicion_2 = expresiones.get('condicion_2', 'Condición no encontrada')
            cuerpo_2 = expresiones.get('cuerpo_2', 'Cuerpo no encontrado')

            # Nodos específicos
            dot.node('4', condicion_1)
            dot.node('5', cuerpo_1)
            dot.node('6', condicion_2)
            dot.node('7', cuerpo_2)

            # Conectar las expresiones dinámicas
            dot.edge('S', '1')
            dot.edge('S', '2')
            dot.edge('S', '3')
            dot.edge('1', '4')  # Condición del primer if
            dot.edge('2', '5')  # Cuerpo del primer if
            dot.edge('3', '6')  # Condición del else if
            dot.edge('3', '7')  # Cuerpo del else if

        # Verificar si es un ciclo while
        elif 'while' in estructura_base:
            dot.node('1', 'while (E)')
            dot.node('2', '{ C }')

            # Agregar las expresiones dinámicas para while
            condicion = expresiones.get('condicion_1', 'Condición no encontrada')
            cuerpo = expresiones.get('cuerpo_1', 'Cuerpo no encontrado')

            # Nodos específicos para while
            dot.node('3', condicion)
            dot.node('4', cuerpo)

            # Conectar las expresiones dinámicas
            dot.edge('S', '1')
            dot.edge('S', '2')
            dot.edge('1', '3')  # Condición del while
            dot.edge('2', '4')  # Cuerpo del while

        # Verificar si es un ciclo do-while
        elif 'do' in estructura_base:
            dot.node('1', 'do { C }')
            dot.node('2', 'while (E);')

            # Agregar las expresiones dinámicas para do-while
            cuerpo = expresiones.get('cuerpo_1', 'Cuerpo no encontrado')
            condicion = expresiones.get('condicion_1', 'Condición no encontrada')

            # Nodos específicos para do-while
            dot.node('3', cuerpo)
            dot.node('4', condicion)

            # Conectar las expresiones dinámicas
            dot.edge('S', '1')
            dot.edge('S', '2')
            dot.edge('1', '3')  # Cuerpo del do
            dot.edge('2', '4')  # Condición del while

        else:
            dot.node('error', 'Estructura no reconocida')

        # Guardar el gráfico como un archivo PNG
        imagen_path = os.path.join(os.path.dirname(__file__), 'arbol_derivacion')
        dot.render(imagen_path, format='png')

        return imagen_path + '.png'

    except Exception as e:
        print("Error al generar el árbol de derivación:")
        print(e)
        return None
