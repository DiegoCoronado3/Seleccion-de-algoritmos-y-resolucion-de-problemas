import time
import sys

# ── Lectura del archivo ──
def leer(path):
    grid = []
    with open(path) as f:
        for line in f:
            nums = line.strip().split()
            if len(nums) == 9 and all(n.isdigit() for n in nums):
                grid.append(list(map(int, nums)))

    if len(grid) != 9:
        print("Error: el archivo no tiene 9 filas válidas.")
        sys.exit(1)

    return grid


# ── Vecindad precalculada ──
def _vecinas(r, c):
    v = set()

    for i in range(9):
        if i != c:
            v.add((r, i))
        if i != r:
            v.add((i, c))

    br, bc = 3 * (r // 3), 3 * (c // 3)

    for i in range(3):
        for j in range(3):
            nr, nc = br + i, bc + j
            if (nr, nc) != (r, c):
                v.add((nr, nc))
    return v


VEC = {(r, c): _vecinas(r, c) for r in range(9) for c in range(9)}


# ── Dominio inicial ──
def posibles(g, r, c):
    usados = {g[nr][nc] for nr, nc in VEC[(r, c)] if g[nr][nc] != 0}
    return set(range(1, 10)) - usados


#  BACKTRACKING + MRV + FORWARD CHECKING
def resolver(grid):

    expansiones = [0]
    retrocesos = [0]

    def bt(g, doms):

        expansiones[0] += 1

        vacias = [(r, c) for r in range(9) for c in range(9) if g[r][c] == 0]

        if not vacias:
            return True

        r, c = min(vacias, key=lambda x: len(doms[x]))

        if not doms[(r, c)]:
            return False

        for v in sorted(doms[(r, c)]):

            g[r][c] = v

            nuevos = {}
            ok = True

            for nr, nc in VEC[(r, c)]:

                if g[nr][nc] == 0:

                    nuevo_dom = doms[(nr, nc)] - {v}

                    if not nuevo_dom:
                        ok = False
                        break

                    nuevos[(nr, nc)] = nuevo_dom

            if ok:
                doms2 = {**doms, **nuevos}
                doms2.pop((r, c), None)

                if bt(g, doms2):
                    return True

            retrocesos[0] += 1
            g[r][c] = 0

        return False

    doms = {(r, c): posibles(grid, r, c)
            for r in range(9) for c in range(9) if grid[r][c] == 0}

    t0 = time.time()

    exito = bt(grid, doms)

    return exito, expansiones[0], retrocesos[0], time.time() - t0


#  VISUALIZACIÓN DEL TABLERO
def pintar_tablero(grid):

    print("\n      1 2 3   4 5 6   7 8 9")
    print("    +-------+-------+-------+")

    for r in range(9):

        if r in (3, 6):
            print("    +-------+-------+-------+")

        print(f"{r+1}   |", end=" ")

        for c in range(9):

            val = grid[r][c]
            char = "." if val == 0 else str(val)

            print(char, end=" ")

            if c in (2, 5):
                print("|", end=" ")

        print("|")

    print("    +-------+-------+-------+")

#  VERIFICACIÓN
def verificar(grid):

    ref = set(range(1, 10))

    for r in range(9):
        if set(grid[r]) != ref:
            return False

    for c in range(9):
        if {grid[r][c] for r in range(9)} != ref:
            return False

    for br in range(3):
        for bc in range(3):

            bloque = {grid[br*3+i][bc*3+j] for i in range(3) for j in range(3)}

            if bloque != ref:
                return False

    return True

#  MAIN
if __name__ == "__main__":

    print("\nPROBLEMA 3: SUDOKU 9x9 - SOLVER")

    ruta_default = "sudoku_9x9_es.txt"
    entrada = input(f"Ruta del archivo [{ruta_default}]: ").strip()
    ruta = entrada if entrada else ruta_default

    original = leer(ruta)
    grid = [fila[:] for fila in original]

    print("\nSUDOKU - ESTADO INICIAL")
    pintar_tablero(original)

    vacias_total = sum(1 for r in range(9) for c in range(9) if original[r][c] == 0)
    pistas = 81 - vacias_total

    print("\nEstadísticas del puzzle")
    print("Celdas dadas:", pistas)
    print("Celdas vacías:", vacias_total)

    print("\nResolviendo...")

    exito, expansiones, retrocesos, t = resolver(grid)

    print("\nSUDOKU - SOLUCIÓN")

    if exito:

        pintar_tablero(grid)

        print("\nMétricas del algoritmo")
        print("Estado: RESUELTO")
        print("Expansiones:", expansiones)
        print("Retrocesos:", retrocesos)
        print("Tiempo:", round(t*1000, 2), "ms")

        if verificar(grid):
            print("\nSOLUCIÓN VÁLIDA")
        else:
            print("\nLa solución no es válida")

    else:
        print("No se encontró solución.")

    print("\n" + "="*50 + "\n")