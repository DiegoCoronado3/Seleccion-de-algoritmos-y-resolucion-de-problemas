import random
import time

# Algoritmo Min-Conflicts
def min_conflicts(n, max_iter=50000, seed=42):

    random.seed(seed)

    sol = list(range(n))
    random.shuffle(sol)

    col_c = [0] * n
    diag1 = [0] * (2 * n)
    diag2 = [0] * (2 * n)

    for r in range(n):
        c = sol[r]
        col_c[c] += 1
        diag1[r - c + n] += 1
        diag2[r + c] += 1

    def conf_reina(r):
        c = sol[r]
        return (col_c[c] - 1) + (diag1[r - c + n] - 1) + (diag2[r + c] - 1)

    def conf_si_muevo(r, c_nuevo):
        c_old = sol[r]

        col_c[c_old] -= 1
        diag1[r - c_old + n] -= 1
        diag2[r + c_old] -= 1

        conf = col_c[c_nuevo] + diag1[r - c_nuevo + n] + diag2[r + c_nuevo]

        col_c[c_old] += 1
        diag1[r - c_old + n] += 1
        diag2[r + c_old] += 1

        return conf

    def mover(r, c_nuevo):
        c_old = sol[r]

        col_c[c_old] -= 1
        diag1[r - c_old + n] -= 1
        diag2[r + c_old] -= 1

        sol[r] = c_nuevo

        col_c[c_nuevo] += 1
        diag1[r - c_nuevo + n] += 1
        diag2[r + c_nuevo] += 1

    for it in range(max_iter):

        conflictivas = [r for r in range(n) if conf_reina(r) > 0]

        if not conflictivas:
            return sol, it, 0

        r = random.choice(conflictivas)

        min_c = min(conf_si_muevo(r, c) for c in range(n))
        candidatos = [c for c in range(n) if conf_si_muevo(r, c) == min_c]

        mover(r, random.choice(candidatos))

    total_conf = sum(conf_reina(r) for r in range(n)) // 2
    return sol, max_iter, total_conf



# Mostrar tablero
def tablero(sol):

    n = len(sol)

    print("\nTablero:")

    print("   ", end="")
    for c in range(n):
        print(f"{c+1:2}", end=" ")
    print()

    print("  +" + "---"*n + "+")

    for fila in range(n):

        print(f"{fila+1:2}|", end=" ")

        for col in range(n):

            if sol[fila] == col:
                print("Q", end="  ")
            else:
                print(".", end="  ")

        print("|")

    print("  +" + "---"*n + "+")



def mostrar_solucion(n, sol, iters, conflictos, tiempo):

    print("\nRESULTADO")
    print("--------------------------")
    print("Conflictos:", conflictos)
    print("Iteraciones:", iters)
    print("Tiempo:", round(tiempo, 4), "s")

    print("\nCOLOCACIÓN DE REINAS (fila -> columna)")
    print("--------------------------------------")

    for r in range(n):
        print(f"Fila {r+1} -> Columna {sol[r]+1}")

    tablero(sol)


# MAIN
if __name__ == "__main__":

    n = int(input("Ingrese el número de reinas (N): "))

    inicio = time.time()

    sol, iters, conflictos = min_conflicts(n)

    tiempo = time.time() - inicio

    mostrar_solucion(n, sol, iters, conflictos, tiempo)