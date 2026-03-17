import time

# Símbolos permitidos
SIMBOLOS = "0123456789ABCDEF"

# Leer archivo
def leer(path):
    grid = []

    with open(path) as f:
        for line in f:
            vals = line.strip().split()
            if len(vals) == 16:
                fila = []
                for v in vals:
                    if v == ".":
                        fila.append(".")
                    else:
                        fila.append(v.upper())
                grid.append(fila)

    if len(grid) != 16:
        raise ValueError("El archivo no tiene 16 filas válidas")

    return grid


# Vecinos
def vecinos(r, c):

    v = set()

    for i in range(16):
        if i != c:
            v.add((r, i))
        if i != r:
            v.add((i, c))

    br = (r // 4) * 4
    bc = (c // 4) * 4

    for i in range(4):
        for j in range(4):
            nr = br + i
            nc = bc + j
            if (nr, nc) != (r, c):
                v.add((nr, nc))

    return v


VECINOS = {(r, c): vecinos(r, c) for r in range(16) for c in range(16)}


# Dominio
def dominio(grid, r, c):

    usados = {grid[nr][nc] for nr, nc in VECINOS[(r, c)] if grid[nr][nc] != "."}

    return set(SIMBOLOS) - usados



# Backtracking + MRV + Forward Checking
def resolver(grid):

    expansiones = [0]
    retrocesos = [0]

    def bt(g, doms):

        expansiones[0] += 1

        vacias = [(r, c) for r in range(16) for c in range(16) if g[r][c] == "."]

        if not vacias:
            return True

        r, c = min(vacias, key=lambda x: len(doms[x]))

        for v in sorted(doms[(r, c)]):

            g[r][c] = v

            nuevos = {}
            ok = True

            for nr, nc in VECINOS[(r, c)]:
                if g[nr][nc] == ".":

                    nd = doms[(nr, nc)] - {v}

                    if not nd:
                        ok = False
                        break

                    nuevos[(nr, nc)] = nd

            if ok:

                doms2 = {**doms, **nuevos}
                doms2.pop((r, c), None)

                if bt(g, doms2):
                    return True

            retrocesos[0] += 1
            g[r][c] = "."

        return False

    doms = {(r, c): dominio(grid, r, c)
            for r in range(16)
            for c in range(16)
            if grid[r][c] == "."}

    t0 = time.time()

    exito = bt(grid, doms)

    tiempo = time.time() - t0

    return exito, expansiones[0], retrocesos[0], tiempo



# Imprimir tablero
def imprimir(grid):

    print("\n      ", end="")
    for c in range(16):
        print(f"{SIMBOLOS[c]} ", end="")
        if c in (3,7,11):
            print(" ", end="")
    print()

    print("    +" + "----"*4 + "+" + "----"*4 + "+" + "----"*4 + "+" + "----"*4 + "+")

    for r in range(16):

        if r in (4,8,12):
            print("    +" + "----"*4 + "+" + "----"*4 + "+" + "----"*4 + "+" + "----"*4 + "+")

        print(f"{SIMBOLOS[r]} |", end=" ")

        for c in range(16):

            v = grid[r][c]

            if v == ".":
                v = "."

            print(v, end=" ")

            if c in (3,7,11):
                print("|", end=" ")

        print("|")

    print("    +" + "----"*4 + "+" + "----"*4 + "+" + "----"*4 + "+" + "----"*4 + "+")


# Verificar solución
def verificar(grid):

    ref = set(SIMBOLOS)

    for r in range(16):
        if set(grid[r]) != ref:
            return False

    for c in range(16):
        if {grid[r][c] for r in range(16)} != ref:
            return False

    for br in range(4):
        for bc in range(4):

            s = set()

            for i in range(4):
                for j in range(4):
                    s.add(grid[br*4+i][bc*4+j])

            if s != ref:
                return False

    return True


# MAIN
if __name__ == "__main__":

    ruta = input("Archivo sudoku 16x16 [sudoku_16x16_es.txt]: ").strip()
    if ruta == "":
        ruta = "sudoku_16x16_es.txt"

    grid = leer(ruta)

    print("\nSUDOKU 16x16 - ESTADO INICIAL")
    imprimir(grid)

    print("\nResolviendo...\n")

    exito, exp, back, t = resolver(grid)

    if exito:

        print("SUDOKU 16x16 - SOLUCION")
        imprimir(grid)

        print("\nMétricas")
        print("Estado: RESUELTO")
        print("Expansiones:", exp)
        print("Retrocesos:", back)
        print("Tiempo:", round(t,3), "segundos")

        if verificar(grid):
            print("Solución verificada correctamente")

    else:
        print("No se encontró solución")