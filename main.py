"""Programa principal: menú unificado para ejecutar todos los módulos."""
import sys
from turing_machine import TuringMachine
from tm_loader import load_turing_machine_from_file, print_tm_info
from unary_utils import decimal_to_unary, unary_to_decimal, fibonacci, verify_fibonacci_result
from create_diagram import create_graphviz_diagram
from empirical_analysis import run_empirical_analysis


def simulator():
    """Ejecuta el simulador interactivo de Máquina de Turing."""
    print("\n" + "="*70)
    print(" SIMULADOR DE MÁQUINA DE TURING - FIBONACCI")
    print("="*70)
    
    config_file = input("\nArchivo de configuración (Enter para 'fibonacci_tm.txt'): ").strip()
    if not config_file:
        config_file = "fibonacci_tm.txt"
    
    result = load_turing_machine_from_file(config_file)
    if result is None:
        print("Error al cargar.")
        return
    
    states, alphabet, transitions, initial_state, accept_states = result
    print_tm_info(states, alphabet, transitions, initial_state, accept_states)
    tm = TuringMachine(states, alphabet, transitions, initial_state, accept_states)
    
    while True:
        print("\n" + "="*70)
        print("1. F(n) decimal  2. Cadena unaria  3. Volver")
        print("="*70)
        
        opcion = input("Opción: ").strip()
        
        if opcion == "3":
            break
        
        elif opcion == "1":
            try:
                n = int(input("Valor n: "))
                if n < 0:
                    print("Error: n >= 0")
                    continue
                input_string = decimal_to_unary(n)
                print(f"Decimal n={n}, Unario='{input_string}', Esperado F({n})={fibonacci(n)}")
            except ValueError:
                print("Error: número inválido")
                continue
        
        elif opcion == "2":
            input_string = input("Cadena unaria (solo '1'): ").strip()
            if not input_string or not all(c == '1' for c in input_string):
                print("Error: solo '1'")
                continue
            try:
                n = unary_to_decimal(input_string)
                print(f"Unario='{input_string}', n={n}, Esperado F({n})={fibonacci(n)}")
            except:
                print("Error interpretando entrada")
                continue
        
        else:
            print("Opción inválida")
            continue
        
        print("\nEjecutando simulación...")
        accepted, configurations, output_tape = tm.run(input_string, max_steps=5000)
        
        print("\n" + "="*70)
        print("RESULTADOS")
        print("="*70)
        print(f"Estado: {'ACEPTADO ✓' if accepted else 'NO ACEPTADO ✗'}")
        print(f"Pasos: {len(configurations)}")
        print(f"Cinta final: '{output_tape}'")
        
        try:
            if output_tape and output_tape != 'E' and all(c == '1' for c in output_tape):
                result_value = unary_to_decimal(output_tape)
                print(f"Resultado decimal: {result_value}")
                if verify_fibonacci_result(n, output_tape):
                    print(f"✓ CORRECTO: F({n}) = {result_value}")
                else:
                    expected = fibonacci(n)
                    print(f"✗ INCORRECTO: esperado F({n})={expected}, obtenido {result_value}")
        except:
            pass
        
        print("="*70)
        
        ver = input("\n¿Ver configuraciones? (s/n): ").strip().lower()
        if ver == 's':
            tm.print_configurations()


def diagrams():
    """Genera diagramas ASCII y PNG de la Máquina de Turing."""
    print("\n" + "="*70)
    print(" GENERADOR DE DIAGRAMAS")
    print("="*70)
    print("\nGenerando diagramas...")
    try:
        create_graphviz_diagram()
        print("✓ Diagramas creados:")
        print("  - diagrama_mt.txt (ASCII)")
        print("  - diagrama_mt.png (si Graphviz está instalado)")
    except Exception as e:
        print(f"Error: {e}")


def analysis():
    """Ejecuta análisis empírico de tiempo/pasos."""
    print("\n" + "="*70)
    print(" ANÁLISIS EMPÍRICO")
    print("="*70)
    
    config_file = input("Archivo de configuración (Enter para 'fibonacci_tm.txt'): ").strip()
    if not config_file:
        config_file = "fibonacci_tm.txt"
    
    try:
        max_n = int(input("Máximo n a analizar (Enter para 10): ").strip() or "10")
    except ValueError:
        max_n = 10
    
    run_empirical_analysis(config_file, max_n=max_n)


def main_menu():
    """Menú principal con todas las opciones."""
    while True:
        print("\n" + "="*70)
        print(" PROYECTO: ANÁLISIS DE ALGORITMOS - MÁQUINA DE TURING FIBONACCI")
        print("="*70)
        print("\n1. Simulador interactivo")
        print("2. Generar diagramas")
        print("3. Análisis empírico")
        print("4. Ejecutar TODO")
        print("5. Salir")
        print("="*70)
        
        opcion = input("Seleccione opción (1-5): ").strip()
        
        if opcion == "1":
            simulator()
        elif opcion == "2":
            diagrams()
        elif opcion == "3":
            analysis()
        elif opcion == "4":
            print("\n⏳ Ejecutando todos los módulos...\n")
            diagrams()
            print("\n" + "-"*70)
            analysis()
            print("\n" + "-"*70)
            simulator()
        elif opcion == "5":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
