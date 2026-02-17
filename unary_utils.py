"""Utilidades para conversión unaria ↔ decimal y cálculo de Fibonacci."""

def decimal_to_unary(n):
    """Convierte decimal a unario: n → n+1 unos. Ej: 5 → '111111'."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    return '1' * (n + 1)


def unary_to_decimal(unary_str):
    """Convierte unario a decimal: '111111' → 5."""
    if not unary_str or not all(c == '1' for c in unary_str):
        raise ValueError("Solo se permiten unos")
    return len(unary_str) - 1


def fibonacci(n):
    """Calcula F(n) iterativamente."""
    if n < 0:
        raise ValueError("n >= 0")
    
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
    """Genera lista [F(0), F(1), ..., F(max_n)]."""
    sequence = []
    for i in range(max_n + 1):
        sequence.append(fibonacci(i))
    return sequence


def verify_fibonacci_result(n, result_unary):
    """Verifica si result_unary es F(n) correcto en unario."""
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
