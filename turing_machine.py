"""Máquina de Turing determinista de una cinta."""

class TuringMachine:
    """Máquina de Turing para procesar cadenas."""
    
    def __init__(self, states, alphabet, transitions, initial_state, accept_states, blank='_'):
        """Inicializa la MT con estados, alfabeto y transiciones."""
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.blank = blank
        self.tape = []
        self.head_position = 0
        self.current_state = initial_state
        self.configurations = []
        
    def load_tape(self, input_string):
        """Carga la cinta con entrada."""
        self.tape = list(input_string) if input_string else [self.blank]
        self.head_position = 0
        self.current_state = self.initial_state
        self.configurations = []
        
    def read_symbol(self):
        """Lee símbolo actual expandiendo cinta si es necesario."""
        if self.head_position < 0:
            self.tape.insert(0, self.blank)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank)
        return self.tape[self.head_position]
    
    def write_symbol(self, symbol):
        """Escribe símbolo expandiendo cinta si es necesario."""
        if self.head_position < 0:
            self.tape.insert(0, symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(symbol)
    
    def move_head(self, direction):
        """Mueve cabeza: R(derecha), L(izquierda), S(queda)."""
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
    
    def get_configuration(self):
        """Retorna configuración actual: (estado, posición, cinta)."""
        tape_str = ''.join(self.tape).strip(self.blank) or self.blank
        return (self.current_state, self.head_position, tape_str)
    
    def step(self):
        """Ejecuta un paso de la MT, retorna False si no hay transición."""
        current_symbol = self.read_symbol()
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            return False
        
        new_state, write_symbol, direction = self.transitions[key]
        self.configurations.append(self.get_configuration())
        self.write_symbol(write_symbol)
        self.move_head(direction)
        self.current_state = new_state
        return True
    
    def run(self, input_string, max_steps=10000):
        """Ejecuta MT hasta aceptar, rechazar o alcanzar max_steps."""
        self.load_tape(input_string)
        steps = 0
        
        while steps < max_steps:
            if self.current_state in self.accept_states:
                self.configurations.append(self.get_configuration())
                tape_output = ''.join(self.tape).strip(self.blank) or self.blank
                return (True, self.configurations, tape_output)
            
            if not self.step():
                tape_output = ''.join(self.tape).strip(self.blank) or self.blank
                return (False, self.configurations, tape_output)
            
            steps += 1
        
        tape_output = ''.join(self.tape).strip(self.blank) or self.blank
        return (False, self.configurations, tape_output)
    
    def print_configurations(self):
        """Imprime todas las configuraciones guardadas."""
        print("\n" + "="*70)
        print("CONFIGURACIONES DE LA SIMULACIÓN")
        print("="*70)
        print(f"{'Paso':<6} {'Estado':<10} {'Posición':<10} {'Cinta'}")
        print("-"*70)
        
        for i, (state, pos, tape) in enumerate(self.configurations):
            print(f"{i:<6} {state:<10} {pos:<10} {tape}")
        
        print("="*70)
