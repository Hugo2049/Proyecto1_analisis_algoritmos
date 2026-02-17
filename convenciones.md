``` 
# Convenciones para la Máquina de Turing - Fibonacci

## 1. Representación de Números en la Cinta

### Sistema Unario
Los números enteros no negativos se representan en **notación unaria**:

- Un número **n** se representa como **(n+1) símbolos '1'**
- Ejemplos:
  - 0 → `1`
  - 1 → `11`
  - 2 → `111`
  - 3 → `1111`
  - 5 → `111111`

### Símbolos de la Cinta
- `1`: Representa una unidad
- `0`: Separador entre números
- `_`: Blanco (celda vacía)

## 2. Entrada y Salida

### Entrada
La cinta inicial contiene el número **n** en unario, representando la posición en la sucesión de Fibonacci que queremos calcular.

**Ejemplo:** Para calcular F(5):
```
Entrada: 111111  (representa n=5)
```

### Salida
Al finalizar, la cinta contendrá el resultado **F(n)** en notación unaria.

**Ejemplo:** Para F(5) = 5:
```
Salida: 111111  (representa 5)
```

## 3. Sucesión de Fibonacci

La sucesión se define como:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) para n ≥ 2

**Primeros valores:**
- F(0) = 0 → `1` (en unario)
- F(1) = 1 → `11`
- F(2) = 1 → `11`
- F(3) = 2 → `111`
- F(4) = 3 → `1111`
- F(5) = 5 → `111111`
- F(6) = 8 → `111111111`

## 4. Configuración de la Máquina de Turing

### Estados
- `q0`: Estado inicial
- `qf`: Estado final/aceptación

### Formato de Transiciones
Cada línea del archivo de configuración representa una transición:
```
estado_actual,símbolo_leído,nuevo_estado,símbolo_escribir,dirección
```

Donde:
- `estado_actual`: Estado actual de la MT
- `símbolo_leído`: Símbolo que lee la cabeza
- `nuevo_estado`: Estado al que transiciona
- `símbolo_escribir`: Símbolo que escribe en la cinta
- `dirección`: `R` (derecha), `L` (izquierda), `S` (stay/quieto)

### Ejemplo de línea de transición:
```
q0,1,q1,0,R
```
Significa: "Si estoy en q0 y leo un 1, voy a q1, escribo 0 y muevo a la derecha"
```