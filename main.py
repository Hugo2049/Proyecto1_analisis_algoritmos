import sys
from turing_machine import TuringMachine
from tm_loader import load_turing_machine_from_file, print_tm_info
from unary_utils import decimal_to_unary, unary_to_decimal, fibonacci, verify_fibonacci_result


def main():
    """Función principal del programa."""
    
    print("="*70)
    print(" SIMULADOR DE MÁQUINA DE TURING - SUCESIÓN DE FIBONACCI")
    print("="*70)
    
    # 1. Cargar la configuración de la MT desde archivo
    config_file = input("\nIngrese el nombre del archivo de configuración (Enter para usar 'fibonacci_tm.txt'): ").strip()
    if not config_file:
        config_file = "fibonacci_tm.txt"
    
    print(f"\nCargando configuración desde '{config_file}'...")
    result = load_turing_machine_from_file(config_file)
    
    if result is None:
        print("Error al cargar la configuración. Terminando programa.")
        return
    
    states, alphabet, transitions, initial_state, accept_states = result
    
    # Mostrar información de la MT
    print_tm_info(states, alphabet, transitions, initial_state, accept_states)
    
    # 2. Crear instancia de la Máquina de Turing
    tm = TuringMachine(states, alphabet, transitions, initial_state, accept_states)
    
    # 3. Solicitar entrada al usuario
    while True:
        print("\n" + "="*70)
        print("OPCIONES:")
        print("1. Calcular F(n) ingresando n en decimal")
        print("2. Ingresar cadena directamente en notación unaria")
        print("3. Salir")
        print("="*70)
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "3":
            print("\n¡Hasta luego!")
            break
        
        elif opcion == "1":
            try:
                n = int(input("\nIngrese el valor de n (posición en Fibonacci, n >= 0): "))
                if n < 0:
                    print("Error: n debe ser no negativo.")
                    continue
                
                # Convertir a unario
                input_string = decimal_to_unary(n)
                print(f"\nEntrada en decimal: n = {n}")
                print(f"Entrada en unario: '{input_string}' ({len(input_string)} unos)")
                print(f"Valor esperado: F({n}) = {fibonacci(n)}")
                
            except ValueError:
                print("Error: Ingrese un número entero válido.")
                continue
        
        elif opcion == "2":
            input_string = input("\nIngrese la cadena en notación unaria (solo '1'): ").strip()
            if not input_string or not all(c == '1' for c in input_string):
                print("Error: La cadena debe contener solo el símbolo '1'.")
                continue
            
            try:
                n = unary_to_decimal(input_string)
                print(f"\nEntrada en unario: '{input_string}'")
                print(f"Esto representa: n = {n}")
                print(f"Valor esperado: F({n}) = {fibonacci(n)}")
            except:
                print("Error al interpretar la entrada.")
                continue
        
        else:
            print("Opción inválida.")
            continue
        
        # 4. Ejecutar la simulación
        print("\n" + "-"*70)
        print("Ejecutando simulación...")
        print("-"*70)
        
        accepted, configurations, output_tape = tm.run(input_string, max_steps=5000)
        
        # 5. Mostrar resultados
        print("\n" + "="*70)
        print("RESULTADOS DE LA SIMULACIÓN")
        print("="*70)
        
        if accepted:
            print(f"Estado final: ACEPTADO ✓")
        else:
            print(f"Estado final: NO ACEPTADO ✗")
        
        print(f"Número de pasos: {len(configurations)}")
        print(f"Contenido final de la cinta: '{output_tape}'")
        
        # Intentar interpretar el resultado
        try:
            if output_tape and output_tape != 'E' and all(c == '1' for c in output_tape):
                result_value = unary_to_decimal(output_tape)
                print(f"Resultado en decimal: {result_value}")
                
                # Verificar si es correcto
                if verify_fibonacci_result(n, output_tape):
                    print(f"✓ Resultado CORRECTO: F({n}) = {result_value}")
                else:
                    expected = fibonacci(n)
                    print(f"✗ Resultado INCORRECTO")
                    print(f"  Se esperaba: F({n}) = {expected}")
                    print(f"  Se obtuvo: {result_value}")
            else:
                print("(No se pudo interpretar el resultado)")
        except:
            print("(Error al interpretar el resultado)")
        
        print("="*70)
        
        # Preguntar si quiere ver las configuraciones
        ver_config = input("\n¿Desea ver todas las configuraciones de la simulación? (s/n): ").strip().lower()
        if ver_config == 's':
            tm.print_configurations()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
