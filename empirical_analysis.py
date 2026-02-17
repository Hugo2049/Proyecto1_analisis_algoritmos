import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from turing_machine import TuringMachine
from tm_loader import load_turing_machine_from_file
from unary_utils import decimal_to_unary


def measure_execution_time(tm, input_string, repetitions=5):
    """
    Mide el tiempo de ejecución promedio de la MT para una entrada dada.
    
    Args:
        tm: Instancia de TuringMachine
        input_string: Cadena de entrada
        repetitions: Número de repeticiones para promediar
        
    Returns:
        Tupla (tiempo_promedio_segundos, numero_de_pasos)
    """
    times = []
    steps = 0
    
    for _ in range(repetitions):
        start_time = time.time()
        accepted, configurations, _ = tm.run(input_string, max_steps=10000)
        end_time = time.time()
        
        times.append(end_time - start_time)
        steps = len(configurations)
    
    avg_time = np.mean(times)
    return avg_time, steps


def run_empirical_analysis(config_file="fibonacci_tm.txt", max_n=15):
    """
    Ejecuta el análisis empírico completo.
    
    Args:
        config_file: Archivo de configuración de la MT
        max_n: Valor máximo de n a probar
    """
    print("="*70)
    print(" ANÁLISIS EMPÍRICO - TIEMPO DE EJECUCIÓN")
    print("="*70)
    
    # Cargar la MT
    print(f"\nCargando MT desde '{config_file}'...")
    result = load_turing_machine_from_file(config_file)
    if result is None:
        print("Error al cargar la configuración.")
        return
    
    states, alphabet, transitions, initial_state, accept_states = result
    tm = TuringMachine(states, alphabet, transitions, initial_state, accept_states)
    
    # Preparar datos para el análisis
    test_inputs = []
    input_sizes = []
    execution_times = []
    num_steps = []
    
    print("\nEjecutando pruebas...")
    print("-"*70)
    print(f"{'n':<5} {'Input':<15} {'Tamaño':<10} {'Pasos':<10} {'Tiempo (s)':<15}")
    print("-"*70)
    
    # Realizar mediciones
    for n in range(max_n + 1):
        input_string = decimal_to_unary(n)
        input_size = len(input_string)
        
        avg_time, steps = measure_execution_time(tm, input_string, repetitions=3)
        
        test_inputs.append(n)
        input_sizes.append(input_size)
        execution_times.append(avg_time)
        num_steps.append(steps)
        
        print(f"{n:<5} {input_string[:12]+'...' if len(input_string) > 12 else input_string:<15} "
              f"{input_size:<10} {steps:<10} {avg_time:<15.6f}")
    
    print("-"*70)
    
    # Convertir a arrays de numpy
    X = np.array(input_sizes).reshape(-1, 1)
    y_time = np.array(execution_times)
    y_steps = np.array(num_steps)
    
    # Guardar datos
    save_data(test_inputs, input_sizes, execution_times, num_steps)
    
    # Realizar regresiones polinomiales
    print("\n" + "="*70)
    print(" REGRESIÓN POLINOMIAL")
    print("="*70)
    
    best_degree_time = find_best_polynomial(X, y_time, "Tiempo de Ejecución")
    best_degree_steps = find_best_polynomial(X, y_steps, "Número de Pasos")
    
    # Crear gráficas
    create_plots(input_sizes, execution_times, num_steps, best_degree_time, best_degree_steps)
    
    print("\n✓ Análisis completado exitosamente.")
    print("✓ Archivos generados:")
    print("  - datos_empiricos.txt")
    print("  - grafica_tiempo.png")
    print("  - grafica_pasos.png")
    print("  - grafica_combinada.png")


def find_best_polynomial(X, y, label, max_degree=5):
    """
    Encuentra el mejor grado de polinomio para ajustar los datos.
    
    Args:
        X: Tamaños de entrada
        y: Valores a ajustar
        label: Etiqueta para imprimir
        max_degree: Grado máximo a probar
        
    Returns:
        Mejor grado encontrado
    """
    print(f"\n{label}:")
    print("-"*70)
    
    best_degree = 1
    best_r2 = -np.inf
    
    for degree in range(1, max_degree + 1):
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        y_pred = model.predict(X_poly)
        
        r2 = r2_score(y, y_pred)
        
        print(f"  Grado {degree}: R² = {r2:.6f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_degree = degree
    
    print(f"\n  Mejor ajuste: Polinomio de grado {best_degree} (R² = {best_r2:.6f})")
    return best_degree


def create_plots(input_sizes, execution_times, num_steps, degree_time, degree_steps):
    """
    Crea las gráficas de dispersión y regresión.
    """
    X = np.array(input_sizes).reshape(-1, 1)
    
    # Gráfica 1: Tiempo de ejecución
    plt.figure(figsize=(10, 6))
    plt.scatter(input_sizes, execution_times, color='blue', label='Datos medidos', alpha=0.6, s=50)
    
    # Regresión polinomial
    poly_features = PolynomialFeatures(degree=degree_time)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, execution_times)
    
    X_plot = np.linspace(min(input_sizes), max(input_sizes), 100).reshape(-1, 1)
    X_plot_poly = poly_features.transform(X_plot)
    y_plot = model.predict(X_plot_poly)
    
    plt.plot(X_plot, y_plot, color='red', label=f'Regresión (grado {degree_time})', linewidth=2)
    plt.xlabel('Tamaño de entrada (número de símbolos)', fontsize=12)
    plt.ylabel('Tiempo de ejecución (segundos)', fontsize=12)
    plt.title('Análisis Empírico: Tiempo de Ejecución vs Tamaño de Entrada', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafica_tiempo.png', dpi=300)
    print("\n✓ Gráfica de tiempo guardada: grafica_tiempo.png")
    
    # Gráfica 2: Número de pasos
    plt.figure(figsize=(10, 6))
    plt.scatter(input_sizes, num_steps, color='green', label='Datos medidos', alpha=0.6, s=50)
    
    poly_features = PolynomialFeatures(degree=degree_steps)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, num_steps)
    
    y_plot = model.predict(X_plot_poly)
    
    plt.plot(X_plot, y_plot, color='orange', label=f'Regresión (grado {degree_steps})', linewidth=2)
    plt.xlabel('Tamaño de entrada (número de símbolos)', fontsize=12)
    plt.ylabel('Número de pasos', fontsize=12)
    plt.title('Análisis Empírico: Número de Pasos vs Tamaño de Entrada', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafica_pasos.png', dpi=300)
    print("✓ Gráfica de pasos guardada: grafica_pasos.png")
    
    # Gráfica 3: Combinada
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    ax1.scatter(input_sizes, execution_times, color='blue', alpha=0.6, s=50)
    poly_features = PolynomialFeatures(degree=degree_time)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, execution_times)
    X_plot_poly = poly_features.transform(X_plot)
    y_plot = model.predict(X_plot_poly)
    ax1.plot(X_plot, y_plot, color='red', linewidth=2)
    ax1.set_xlabel('Tamaño de entrada', fontsize=11)
    ax1.set_ylabel('Tiempo de ejecución (s)', fontsize=11)
    ax1.set_title('Tiempo de Ejecución', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.scatter(input_sizes, num_steps, color='green', alpha=0.6, s=50)
    poly_features = PolynomialFeatures(degree=degree_steps)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, num_steps)
    X_plot_poly = poly_features.transform(X_plot)
    y_plot = model.predict(X_plot_poly)
    ax2.plot(X_plot, y_plot, color='orange', linewidth=2)
    ax2.set_xlabel('Tamaño de entrada', fontsize=11)
    ax2.set_ylabel('Número de pasos', fontsize=11)
    ax2.set_title('Número de Pasos', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafica_combinada.png', dpi=300)
    print("✓ Gráfica combinada guardada: grafica_combinada.png")
    plt.close('all')


def save_data(test_inputs, input_sizes, execution_times, num_steps):
    """Guarda los datos empíricos en un archivo."""
    with open('datos_empiricos.txt', 'w', encoding='utf-8') as f:
        f.write("DATOS EMPÍRICOS - ANÁLISIS DE TIEMPO DE EJECUCIÓN\n")
        f.write("="*70 + "\n\n")
        f.write(f"{'n':<5} {'Tamaño':<10} {'Pasos':<10} {'Tiempo (s)':<15}\n")
        f.write("-"*70 + "\n")
        
        for n, size, time_val, steps in zip(test_inputs, input_sizes, execution_times, num_steps):
            f.write(f"{n:<5} {size:<10} {steps:<10} {time_val:<15.8f}\n")
    
    print("\n✓ Datos guardados en: datos_empiricos.txt")


if __name__ == "__main__":
    import sys
    
    # Verificar si se especificó un archivo
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "fibonacci_tm.txt"
    
    # Ejecutar análisis
    try:
        run_empirical_analysis(config_file, max_n=10)
    except Exception as e:
        print(f"\nError durante el análisis: {e}")
        import traceback
        traceback.print_exc()
