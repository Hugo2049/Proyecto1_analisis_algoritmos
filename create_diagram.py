try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Advertencia: graphviz no está instalado. Se creará un diagrama de texto.")


def create_text_diagram():
    """Crea una representación en texto del diagrama de la MT."""
    
    diagram = """
================================================================================
        DIAGRAMA DE MÁQUINA DE TURING - FIBONACCI (Versión Simplificada)
================================================================================

CONVENCIÓN:
  Estado -> (símbolo_leído/símbolo_escrito, dirección) -> Nuevo_Estado

ESTRUCTURA GENERAL:
  - La MT verifica la longitud de la entrada para determinar qué F(n) calcular
  - Marca los símbolos con 'X' mientras cuenta
  - Construye el resultado en unario

================================================================================
TRANSICIONES PRINCIPALES:
================================================================================

INICIO:
  [q0] --(1/X,R)--> [q1]
          |
          Comienza a verificar el tamaño de la entrada

CASO F(0): entrada = '1'
  [q1] --(_/_,L)--> [q_f0] --(X/_,R)--> [q_res0] --(_/1,S)--> [qf]
  
  Resultado: '1' (representa 0 en unario)

CASO F(1): entrada = '11'  
  [q1] --(1/X,R)--> [q2] --(_/_,L)--> [q_f1]
  [q_f1] --(X/_,L)--> [q_res1] --(X/1,R)--> [q_res1b] --(_/1,S)--> [qf]
  
  Resultado: '11' (representa 1 en unario)

CASO F(2): entrada = '111'
  [q2] --(1/X,R)--> [q3] --(_/_,L)--> [q_f2]
  [q_f2] --(X/_,L)--> [q_res2] --(X/_,L)--> [q_res2b] 
  [q_res2b] --(X/1,R)--> [q_res2c] --(_/1,S)--> [qf]
  
  Resultado: '11' (representa 1 en unario)

CASO F(3): entrada = '1111'
  [q3] --(1/X,R)--> [q4] --> ... --> [qf]
  
  Resultado: '111' (representa 2 en unario)

CASO F(4): entrada = '11111'
  [q4] --(1/X,R)--> [q5] --> ... --> [qf]
  
  Resultado: '1111' (representa 3 en unario)

CASO F(5): entrada = '111111'
  [q5] --(1/X,R)--> [q6] --> ... --> [qf]
  
  Resultado: '111111' (representa 5 en unario)

ERROR: entrada con n > 5
  [q6] --(1/X,S)--> [q_error] --(X/E,S)--> [qf]
  
  Resultado: 'E' (error, no implementado)

================================================================================
ESTADO FINAL:
================================================================================
  
  [qf] = Estado de aceptación
    - Acepta cualquier símbolo y se queda en qf
    - Transiciones: (1,1,S), (_,_,S), (E,E,S)

================================================================================
NOTACIÓN BIG-O:
================================================================================

Para esta implementación simplificada que solo maneja casos específicos:

  Tiempo de ejecución: O(n)
  
  Donde n es el tamaño de la entrada (número de unos).
  
  Cada caso específico realiza un número constante de operaciones proporcional
  al tamaño de la entrada más el tamaño de la salida.
  
  Para una MT que calcule Fibonacci de forma general (no implementada aquí),
  el tiempo sería O(F(n)) donde F(n) crece exponencialmente.

================================================================================
"""
    
    with open('diagrama_mt.txt', 'w', encoding='utf-8') as f:
        f.write(diagram)
    
    print("✓ Diagrama de texto creado: diagrama_mt.txt")


def create_graphviz_diagram():
    """Crea un diagrama visual usando Graphviz."""
    
    if not GRAPHVIZ_AVAILABLE:
        print("Graphviz no disponible. Use: pip install graphviz")
        create_text_diagram()
        return
    
    # Crear grafo dirigido
    dot = Digraph(comment='Máquina de Turing - Fibonacci')
    dot.attr(rankdir='LR', size='12,8')
    dot.attr('node', shape='circle', style='filled', fillcolor='lightblue')
    
    # Estado inicial
    dot.node('start', '', shape='none')
    dot.node('q0', 'q0')
    dot.edge('start', 'q0')
    
    # Estados principales
    dot.node('q1', 'q1')
    dot.node('q2', 'q2')
    dot.node('q3', 'q3')
    dot.node('q4', 'q4')
    dot.node('q5', 'q5')
    dot.node('q6', 'q6')
    
    # Estados de resultado para F(0)
    dot.node('q_f0', 'q_f0', fillcolor='lightyellow')
    dot.node('q_res0', 'q_res0', fillcolor='lightyellow')
    
    # Estado final
    dot.node('qf', 'qf', shape='doublecircle', fillcolor='lightgreen')
    
    # Transiciones principales
    dot.edge('q0', 'q1', label='1/X,R')
    dot.edge('q1', 'q2', label='1/X,R')
    dot.edge('q2', 'q3', label='1/X,R')
    dot.edge('q3', 'q4', label='1/X,R')
    dot.edge('q4', 'q5', label='1/X,R')
    dot.edge('q5', 'q6', label='1/X,R')
    
    # Caso F(0)
    dot.edge('q1', 'q_f0', label='_/_,L')
    dot.edge('q_f0', 'q_res0', label='X/_,R')
    dot.edge('q_res0', 'qf', label='_/1,S')
    
    # Estado de error
    dot.node('q_error', 'ERROR', fillcolor='lightcoral')
    dot.edge('q6', 'q_error', label='1/X,S')
    dot.edge('q_error', 'qf', label='X/E,S')
    
    # Auto-loop en estado final
    dot.edge('qf', 'qf', label='1/1,S\\n_/_,S', style='dashed')
    
    # Guardar
    try:
        dot.render('diagrama_mt', format='png', cleanup=True)
        print("✓ Diagrama visual creado: diagrama_mt.png")
    except Exception as e:
        print(f"Error al crear diagrama visual: {e}")
        print("Creando versión de texto...")
        create_text_diagram()
    
    # También crear versión de texto
    create_text_diagram()


if __name__ == "__main__":
    print("Creando diagrama de la Máquina de Turing...")
    create_graphviz_diagram()
    print("\n✓ Diagrama completado.")
