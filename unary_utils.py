def decimal_to_unary(n):
    """
    Convierte un número decimal a representación unaria.
    
    Args:
        n: Número entero no negativo
        
    Returns:
        Cadena de unos representando n+1 unos
        
    Ejemplo:
        decimal_to_unary(0) -> '1'
        decimal_to_unary(5) -> '111111'
    """
    if n < 0:
        raise ValueError("El número debe ser no negativo")
    return '1' * (n + 1)


def unary_to_decimal(unary_str):
    """
    Convierte una cadena unaria a número decimal.
    
    Args:
        unary_str: Cadena de unos
        
    Returns:
        Número entero representado
        
    Ejemplo:
        unary_to_decimal('1') -> 0
        unary_to_decimal('111111') -> 5
    """
    if not unary_str or not all(c == '1' for c in unary_str):
        raise ValueError("La cadena debe contener solo unos")
    return len(unary_str) - 1


def fibonacci(n):
    """
    Calcula el n-ésimo número de Fibonacci.
    
    Args:
        n: Posición en la sucesión (n >= 0)
        
    Returns:
        F(n)
    """
    if n < 0:
        raise ValueError("n debe ser no negativo")
    
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Cálculo iterativo para evitar recursión
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def get_fibonacci_sequence(max_n):
    """
    Genera la sucesión de Fibonacci hasta F(max_n).
    
    Args:
        max_n: Posición máxima
        
    Returns:
        Lista de valores [F(0), F(1), ..., F(max_n)]
    """
    sequence = []
    for i in range(max_n + 1):
        sequence.append(fibonacci(i))
    return sequence


def verify_fibonacci_result(n, result_unary):
    """
    Verifica si el resultado en unario es correcto para F(n).
    
    Args:
        n: Posición en la sucesión
        result_unary: Resultado en notación unaria
        
    Returns:
        True si es correcto, False en caso contrario
    """
    try:
        result = unary_to_decimal(result_unary)
        expected = fibonacci(n)
        return result == expected
    except:
        return False


if __name__ == "__main__":
    # Pruebas
    print("Pruebas de conversión unaria:")
    print("-" * 40)
    for i in range(10):
        unary = decimal_to_unary(i)
        back = unary_to_decimal(unary)
        print(f"{i} -> '{unary}' -> {back}")
    
    print("\nSucesión de Fibonacci:")
    print("-" * 40)
    for i in range(10):
        fib = fibonacci(i)
        fib_unary = decimal_to_unary(fib)
        print(f"F({i}) = {fib} -> '{fib_unary}'")
