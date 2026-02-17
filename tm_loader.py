"""Carga configuración de Máquina de Turing desde archivo CSV."""

def load_turing_machine_from_file(filename):
    """Carga MT desde archivo en formato: estado,símbolo,nuevo_estado,escribe,dirección."""
    states = set()
    alphabet = set()
    transitions = {}
    initial_state = None
    accept_states = set()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(',')
                if len(parts) != 5:
                    print(f"Advertencia: Línea {line_num} ignorada: {line}")
                    continue
                
                current_state, read_symbol, next_state, write_symbol, direction = parts
                current_state = current_state.strip()
                read_symbol = read_symbol.strip()
                next_state = next_state.strip()
                write_symbol = write_symbol.strip()
                direction = direction.strip().upper()
                
                if direction not in ['L', 'R', 'S']:
                    print(f"Advertencia: Línea {line_num} dirección inválida: {direction}")
                    continue
                
                states.add(current_state)
                states.add(next_state)
                alphabet.add(read_symbol)
                alphabet.add(write_symbol)
                
                key = (current_state, read_symbol)
                if key in transitions:
                    print(f"Advertencia: Transición duplicada línea {line_num}: {key}")
                transitions[key] = (next_state, write_symbol, direction)
                
                if initial_state is None and current_state not in ['qf', 'halt', 'accept']:
                    initial_state = current_state
                
                if next_state in ['qf', 'halt', 'accept']:
                    accept_states.add(next_state)
                if current_state in ['qf', 'halt', 'accept']:
                    accept_states.add(current_state)
    
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    if not transitions:
        print("Error: No hay transiciones válidas.")
        return None
    
    if initial_state is None:
        # Usar el primer estado como inicial
        initial_state = 'q0'
        if initial_state not in states:
            initial_state = min(states)  # Usar el primero alfabéticamente
    
    if not accept_states:
        accept_states = {'qf'}
    
    alphabet.add('_')
    return (states, alphabet, transitions, initial_state, accept_states)


def print_tm_info(states, alphabet, transitions, initial_state, accept_states):
    """Imprime información de la MT cargada."""
    print("\n" + "="*70)
    print("INFORMACIÓN DE LA MÁQUINA DE TURING")
    print("="*70)
    print(f"Estados: {sorted(states)}")
    print(f"Alfabeto: {sorted(alphabet)}")
    print(f"Estado inicial: {initial_state}")
    print(f"Estados de aceptación: {sorted(accept_states)}")
    print(f"Número de transiciones: {len(transitions)}")
    print("="*70)
