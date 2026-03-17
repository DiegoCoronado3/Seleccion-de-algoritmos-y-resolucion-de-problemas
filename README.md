# Tarea 2 — Inteligencia Artificial
### Selección de Algoritmos y Resolución de Problemas Clásicos de IA

> Implementación en Python de seis algoritmos clásicos de búsqueda y CSP, con salida visual en consola.
>
> Se agrega un pdf con mas informacion detallada de cada problema asi como la solucion y su implementacion

---

## Contenido del repositorio

```
tarea2-ia/
│
├# Archivos de entrada
│── mochila_10.csv                 # 10 objetos con peso y valor
│── mochila_100.csv                # 100 objetos con peso y valor
│── capacidades_mochila.txt        # Capacidades: CAP10=38, CAP100=1097
│── sudoku_9x9_es.txt              # Puzzle Sudoku 9×9
│── sudoku_16x16_es.txt            # Puzzle Hexadoku 16×16 (símbolos 0–9 y A–F)
│── mapa_5_paises_adyacencias.txt  # Grafo de 5 países (ciclo C₅)
│── mapa_100_paises_adyacencias.txt# Grafo grilla 10×10 (100 países)
│── cuadro_magico_10_especificacion.txt  # n=10, dominio 1–100, constante=505
│
├── mochila.py               # Recocido Simulado + DP exacto
├── reinas.py               # Min-Conflicts con contadores O(1)
├── sudoku9x9.py             # Backtracking + Forward Checking + MRV
├── hexadoku.py              # Backtracking + Forward Checking + MRV (16×16)
├── coloreo.py               # Backtracking + LCV real + Forward Checking
├── cuadro_magico.py         # Recocido Simulado
│
└── README.md
```

---

## Requisitos

- **Python 3.8 o superior**
- **Sin dependencias externas** — solo biblioteca estándar (`time`, `math`, `random`, `sys`, `csv`)

Verificar versión:
```bash
python3 --version
```

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/tarea2-ia.git
cd tarea2-ia
```

No se necesita instalar paquetes ni crear entornos virtuales.

---

## Ejecución

Todos los scripts se corren desde la raíz del repositorio. Cada uno pide la ruta de sus archivos de entrada de forma interactiva — si se presiona Enter sin escribir nada, usa el valor por defecto entre corchetes.

---

### Problema 1 — Mochila 0/1

**Algoritmo:** Recocido Simulado (n=100) + Programación Dinámica exacta (n=10)

```bash
python3 problema1_mochila.py
```

Los archivos de datos se leen automáticamente desde `data/`. No requiere input interactivo.

**Salida esperada:**
```
╔══════════════════════════════════╗
║  PROBLEMA 1: MOCHILA 0/1         ║
╚══════════════════════════════════╝

Objetos seleccionados: [1, 2, 3, 4, 5, 7, 8]
Peso total:            36
Valor total:           270
Restricción de peso:   CUMPLE
Iteraciones:           300
Tiempo de ejecución:   0.077 s
Valor óptimo (DP):     270  → ES ÓPTIMO
```

---

### Problema 2 — N-Reinas

**Algoritmo:** Min-Conflicts con contadores de ataques incrementales O(1)

```bash
python3 reinas.py
```

Pedirá el tamaño del tablero (por defecto prueba n=8 y n=100):

```
¿Cuántas reinas quieres resolver? [8, 100]: 
```

**Salida esperada:**
```
▶ 8-Reinas
  Solución: [1, 3, 5, 7, 2, 0, 6, 4]
  Conflictos: 0  ✓
  Iteraciones: 15  |  Tiempo: 0.0002 s

```

---

### Problema 3 — Sudoku 9×9

**Algoritmo:** Backtracking + Forward Checking + MRV (Minimum Remaining Values)

```bash
python3 sudoku.py
```

Pedirá la ruta del archivo:

```
Ruta del archivo [data/sudoku_9x9_es.txt]: 
```

**Salida esperada:**
```
SUDOKU - SOLUCIÓN

      1 2 3   4 5 6   7 8 9
    +-------+-------+-------+
1   | 5 3 4 | 6 7 8 | 9 1 2 |
2   | 6 7 2 | 1 9 5 | 3 4 8 |
3   | 1 9 8 | 3 4 2 | 5 6 7 |
    +-------+-------+-------+
4   | 8 5 9 | 7 6 1 | 4 2 3 |
5   | 4 2 6 | 8 5 3 | 7 9 1 |
6   | 7 1 3 | 9 2 4 | 8 5 6 |
    +-------+-------+-------+
7   | 9 6 1 | 5 3 7 | 2 8 4 |
8   | 2 8 7 | 4 1 9 | 6 3 5 |
9   | 3 4 5 | 2 8 6 | 1 7 9 |
    +-------+-------+-------+

Métricas del algoritmo
Estado: RESUELTO
Expansiones: 52
Retrocesos: 0
Tiempo: 2.07 ms

SOLUCIÓN VÁLIDA

```

---

### Problema 4 — Hexadoku 16×16

**Algoritmo:** Backtracking + Forward Checking + MRV (símbolos 0–9, A–F)

```bash
python3 hexadoku.py
```

Pedirá la ruta del archivo:

```
Ruta del archivo [data/sudoku_16x16_es.txt]: 
```

**Salida esperada:**
```
SUDOKU 16x16 - SOLUCION

      0 1 2 3  4 5 6 7  8 9 A B  C D E F 
    +----------------+----------------+----
0 | 0 9 2 B | 4 6 7 5 | 8 1 3 A | C D E F |
1 | 6 5 4 7 | 8 B A D | C E 9 F | 2 0 1 3 |
2 | 8 1 A F | C 0 E 3 | B D 2 4 | 5 9 6 7 |
3 | C 3 E D | 2 1 9 F | 0 5 6 7 | 8 A 4 B |
    +----------------+----------------+----
4 | 2 C 3 4 | 6 7 F 0 | 1 A B 8 | D 5 9 E |
5 | D F 5 8 | 9 A B C | 4 7 E 0 | 1 2 3 6 |
6 | 9 A B 1 | D 8 5 E | 2 3 C 6 | 0 F 7 4 |
7 | E 6 7 0 | 1 2 3 4 | 5 9 F D | B 8 A C |
    +----------------+----------------+----
8 | F E 8 C | 5 D 6 9 | A 2 7 3 | 4 B 0 1 |
9 | B 7 6 9 | A 4 C 8 | D F 0 1 | E 3 2 5 |
A | A D 0 3 | B F 2 1 | E C 4 5 | 6 7 8 9 |
B | 4 2 1 5 | E 3 0 7 | 6 B 8 9 | A C F D |
    +----------------+----------------+----
C | 5 4 C 6 | 7 9 8 A | 3 0 D E | F 1 B 2 |
D | 3 8 9 E | 0 C D B | F 6 1 2 | 7 4 5 A |
E | 7 0 D A | F E 1 2 | 9 4 5 B | 3 6 C 8 |
F | 1 B F 2 | 3 5 4 6 | 7 8 A C | 9 E D 0 |
    +----------------+----------------+----

Métricas
Estado: RESUELTO
Expansiones: 22452
Retrocesos: 24697
Tiempo: 0.622 segundos
Solución verificada correctamente
```

---

### Problema 5 — Coloreo de Mapas

**Algoritmo:** Backtracking + LCV corregida + Forward Checking  
Encuentra el número cromático mínimo χ(G) para cada grafo.

```bash
python3 problema5_coloreo.py
```

Pedirá las rutas de ambos mapas:

```
Ruta mapa  5 países  [data/mapa_5_paises_adyacencias.txt]: 
Ruta mapa 100 países [data/mapa_100_paises_adyacencias.txt]: 
```

**Salida esperada:**
```
▶ Mapa 5 países
  χ(G) = 3 colores
  Expansiones: 6  |  Retrocesos: 0  |  Tiempo: 0.0001 s  ✓

▶ Mapa 100 países
  χ(G) = 2 colores
  Expansiones: 101  |  Retrocesos: 0  |  Tiempo: 0.0016 s  ✓
```

---

### Problema 6 — Cuadro Mágico 10×10

**Algoritmo:** Recocido Simulado  
Busca una permutación de 1–100 tal que todas las filas, columnas y diagonales sumen 505.

```bash
python3 problema6_cuadro_magico.py
```

Pedirá la ruta del archivo de especificación:

```
Ruta del archivo de especificación [data/cuadro_magico_10_especificacion.txt]:
```

**Salida esperada:**
```
      C01 C02 C03 C04 C05 C06 C07 C08 C09 C10  Σfila
     -------------------------------------------------------
F01 |  99  86  56  50  39  34   1  73  51  16 | 505
F02 |   4   5  42  47  60  84  62  66  95  40 | 505
F03 |  15  85  65  29  89  33  12  27  70  80 | 505
F04 |  38  54  32 100  46  69  36  79   3  48 | 505
F05 |  82  76  71   6  43  20  57  81  52  17 | 505
F06 |  31  22  92  64  28  30  94   2  98  44 | 505
F07 |  55  37  25  96  58  63  91  21  24  35 | 505
F08 |  90  72  61  13  23  11  75   9  68  83 | 505
F09 |  14  49   8  93  41  87  10  88  18  97 | 505
F10 |  77  19  53   7  78  74  67  59  26  45 | 505
     -------------------------------------------------------
Σcol 505 505 505 505 505 505 505 505 505 505 

Diagonal \ = 505
Diagonal / = 505
```

---


## Resumen de resultados

| Problema | Algoritmo | Resultado | Tiempo |
|----------|-----------|-----------|--------|
| Mochila 10 | DP exacto | Valor=270, Peso=36/38 | 0.073 s |
| Mochila 100 | Recocido Simulado | Valor=7406, Peso=1095/1097 | 0.686 s |
| 8-Reinas | Min-Conflicts | 0 conflictos | 0.0002 s |
| 100-Reinas | Min-Conflicts | 0 conflictos | 0.009 s |
| Sudoku 9×9 | BT+FC+MRV | Resuelto | 1.46 ms |
| Hexadoku 16×16 | BT+FC+MRV | Resuelto | 0.626 s |
| Coloreo 5 países | BT+LCV+FC | χ=3, 0 retrocesos | 0.0001 s |
| Coloreo 100 países | BT+LCV+FC | χ=2, 0 retrocesos | 0.0016 s |

---

## Estructura de archivos de datos

### `mochila_10.csv` / `mochila_100.csv`
```
id,peso,valor
1,5,30
2,3,20
...
```

### `capacidades_mochila.txt`
```
CAP10=38
CAP100=1097
```

### `sudoku_9x9_es.txt` / `sudoku_16x16_es.txt`
```
# Sudoku 9x9
# Formato: 9 filas, valores separados por espacio, 0 = celda vacía
5 3 0 0 7 0 0 0 0
...
```

### `mapa_5_paises_adyacencias.txt` / `mapa_100_paises_adyacencias.txt`
```
# Formato: nodo: vecino1,vecino2,...
A: B,E
B: A,C
...
```

### `cuadro_magico_10_especificacion.txt`
```
n=10
dominio=1-100
constante=505
```

---
Cada problema explora una técnica distinta o eso es lo que se intento hacer:

- **Problemas 1 y 6** — Búsqueda local (Recocido Simulado)
- **Problema 2** — CSP con reparación iterativa (Min-Conflicts)
- **Problemas 3 y 4** — CSP con backtracking sistemático y propagación
- **Problema 5** — CSP con heurísticas LCV + Forward Checking

Los ejercicios teóricos (E1–E7) cubren búsqueda en espacios de creencias, formulaciones CSP, análisis de heurísticas y consistencia de arcos (AC-3).
