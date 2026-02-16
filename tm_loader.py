def load_turing_machine_from_file(filename):
    """
    Carga una Máquina de Turing desde un archivo de configuración.
    
    Formato del archivo:
    estado_actual,símbolo_leído,nuevo_estado,símbolo_escribir,dirección
    
    Args:
        filename: Nombre del archivo de configuración
        
    Returns:
        Tupla (states, alphabet, transitions, initial_state, accept_states)
    """
    states = set()
    alphabet = set()
    transitions = {}
    initial_state = None
    accept_states = set()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                # Ignorar comentarios y líneas vacías
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parsear la línea
                parts = line.split(',')
                if len(parts) != 5:
                    print(f"Advertencia: Línea {line_num} ignorada (formato incorrecto): {line}")
                    continue
                
                current_state, read_symbol, next_state, write_symbol, direction = parts
                current_state = current_state.strip()
                read_symbol = read_symbol.strip()
                next_state = next_state.strip()
                write_symbol = write_symbol.strip()
                direction = direction.strip().upper()
                
                # Validar dirección
                if direction not in ['L', 'R', 'S']:
                    print(f"Advertencia: Línea {line_num} - Dirección inválida: {direction}")
                    continue
                
                # Agregar estados
                states.add(current_state)
                states.add(next_state)
                
                # Agregar símbolos al alfabeto
                alphabet.add(read_symbol)
                alphabet.add(write_symbol)
                
                # Agregar transición
                key = (current_state, read_symbol)
                if key in transitions:
                    print(f"Advertencia: Transición duplicada en línea {line_num}: {key}")
                transitions[key] = (next_state, write_symbol, direction)
                
                # Detectar estado inicial (primer estado que aparece)
                if initial_state is None and current_state not in ['qf', 'halt', 'accept']:
                    initial_state = current_state
                
                # Detectar estados de aceptación
                if next_state in ['qf', 'halt', 'accept']:
                    accept_states.add(next_state)
                if current_state in ['qf', 'halt', 'accept']:
                    accept_states.add(current_state)
    
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
    # Validaciones
    if not transitions:
        print("Error: No se encontraron transiciones válidas.")
        return None
    
    if initial_state is None:
        # Usar el primer estado como inicial
        initial_state = 'q0'
        if initial_state not in states:
            initial_state = min(states)  # Usar el primero alfabéticamente
    
    if not accept_states:
        accept_states = {'qf'}  # Estado de aceptación por defecto
    
    alphabet.add('_')  # Asegurar que el blanco esté en el alfabeto
    
    return (states, alphabet, transitions, initial_state, accept_states)


def print_tm_info(states, alphabet, transitions, initial_state, accept_states):
    """
    Imprime información sobre la Máquina de Turing cargada.
    """
    print("\n" + "="*70)
    print("INFORMACIÓN DE LA MÁQUINA DE TURING")
    print("="*70)
    print(f"Estados: {sorted(states)}")
    print(f"Alfabeto: {sorted(alphabet)}")
    print(f"Estado inicial: {initial_state}")
    print(f"Estados de aceptación: {sorted(accept_states)}")
    print(f"Número de transiciones: {len(transitions)}")
    print("="*70)
