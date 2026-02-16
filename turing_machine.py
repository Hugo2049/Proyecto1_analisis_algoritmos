class TuringMachine:
    """
    Clase que representa una Máquina de Turing determinista de una cinta.
    """
    
    def __init__(self, states, alphabet, transitions, initial_state, accept_states, blank='_'):
        """
        Inicializa la Máquina de Turing.
        
        Args:
            states: Conjunto de estados
            alphabet: Alfabeto de la cinta
            transitions: Diccionario de transiciones {(estado, símbolo): (nuevo_estado, escribir, dirección)}
            initial_state: Estado inicial
            accept_states: Conjunto de estados de aceptación
            blank: Símbolo blanco (por defecto '_')
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.blank = blank
        
        # Estado de ejecución
        self.tape = []
        self.head_position = 0
        self.current_state = initial_state
        self.configurations = []
        
    def load_tape(self, input_string):
        """
        Carga la cinta con una cadena de entrada.
        
        Args:
            input_string: Cadena para cargar en la cinta
        """
        self.tape = list(input_string) if input_string else [self.blank]
        self.head_position = 0
        self.current_state = self.initial_state
        self.configurations = []
        
    def read_symbol(self):
        """
        Lee el símbolo en la posición actual de la cabeza.
        
        Returns:
            Símbolo en la posición actual
        """
        # Expandir la cinta si es necesario
        if self.head_position < 0:
            self.tape.insert(0, self.blank)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank)
            
        return self.tape[self.head_position]
    
    def write_symbol(self, symbol):
        """
        Escribe un símbolo en la posición actual de la cabeza.
        
        Args:
            symbol: Símbolo a escribir
        """
        if self.head_position < 0:
            self.tape.insert(0, symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(symbol)
        else:
            self.tape[self.head_position] = symbol
    
    def move_head(self, direction):
        """
        Mueve la cabeza en la dirección especificada.
        
        Args:
            direction: 'L' (izquierda), 'R' (derecha), 'S' (sin movimiento)
        """
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'S' no hace nada
    
    def get_configuration(self):
        """
        Obtiene la configuración actual de la máquina.
        
        Returns:
            Tupla (estado, posición_cabeza, contenido_cinta)
        """
        tape_str = ''.join(self.tape).strip(self.blank) or self.blank
        return (self.current_state, self.head_position, tape_str)
    
    def step(self):
        """
        Ejecuta un paso de la máquina de Turing.
        
        Returns:
            True si se pudo ejecutar el paso, False si no hay transición
        """
        current_symbol = self.read_symbol()
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            return False
        
        new_state, write_symbol, direction = self.transitions[key]
        
        # Guardar configuración antes de la transición
        self.configurations.append(self.get_configuration())
        
        # Ejecutar transición
        self.write_symbol(write_symbol)
        self.move_head(direction)
        self.current_state = new_state
        
        return True
    
    def run(self, input_string, max_steps=10000):
        """
        Ejecuta la máquina de Turing con una entrada dada.
        
        Args:
            input_string: Cadena de entrada
            max_steps: Número máximo de pasos (para evitar loops infinitos)
            
        Returns:
            Tupla (aceptado, configuraciones, contenido_final_cinta)
        """
        self.load_tape(input_string)
        steps = 0
        
        while steps < max_steps:
            if self.current_state in self.accept_states:
                # Agregar configuración final
                self.configurations.append(self.get_configuration())
                tape_output = ''.join(self.tape).strip(self.blank) or self.blank
                return (True, self.configurations, tape_output)
            
            if not self.step():
                # No hay transición válida
                tape_output = ''.join(self.tape).strip(self.blank) or self.blank
                return (False, self.configurations, tape_output)
            
            steps += 1
        
        # Excedió el máximo de pasos
        tape_output = ''.join(self.tape).strip(self.blank) or self.blank
        return (False, self.configurations, tape_output)
    
    def print_configurations(self):
        """
        Imprime todas las configuraciones guardadas.
        """
        print("\n" + "="*70)
        print("CONFIGURACIONES DE LA SIMULACIÓN")
        print("="*70)
        print(f"{'Paso':<6} {'Estado':<10} {'Posición':<10} {'Cinta'}")
        print("-"*70)
        
        for i, (state, pos, tape) in enumerate(self.configurations):
            print(f"{i:<6} {state:<10} {pos:<10} {tape}")
        
        print("="*70)
