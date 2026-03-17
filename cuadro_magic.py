import random
import math
import time

N = 10
M = 505


# FUNCIONES DE EVALUACIÓN

def sumas_filas(g):
    return [sum(g[r*N:(r+1)*N]) for r in range(N)]


def sumas_cols(g):
    return [sum(g[c::N]) for c in range(N)]


def diag1(g):
    return sum(g[i*N+i] for i in range(N))


def diag2(g):
    return sum(g[i*N+(N-1-i)] for i in range(N))


def costo(g):
    e = 0
    for r in range(N):
        e += (sum(g[r*N:(r+1)*N]) - M)**2

    for c in range(N):
        e += (sum(g[c::N]) - M)**2

    e += (diag1(g) - M)**2
    e += (diag2(g) - M)**2

    return e


def costo_ponderado(g, w=50):
    e = 0

    for r in range(N):
        e += (sum(g[r*N:(r+1)*N]) - M)**2

    for c in range(N):
        e += (sum(g[c::N]) - M)**2

    e += w * (diag1(g) - M)**2
    e += w * (diag2(g) - M)**2

    return e


# RECOCIDO SIMULADO — FASE 1

def fase1(seed, T0=4.0, alpha=0.99995, max_iter=2_000_000):

    random.seed(seed)

    g = list(range(1, 101))
    random.shuffle(g)

    T = T0
    c = costo(g)

    mejor = g[:]
    mc = c

    sin_mejora = 0

    for _ in range(max_iter):

        i, j = random.sample(range(100), 2)
        g[i], g[j] = g[j], g[i]

        cn = costo(g)
        delta = cn - c

        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            c = cn
            sin_mejora = 0

            if c < mc:
                mc = c
                mejor = g[:]

            if mc == 0:
                return mejor, 0

        else:
            g[i], g[j] = g[j], g[i]
            sin_mejora += 1

        if sin_mejora > 40000:
            for _ in range(4):
                i, j = random.sample(range(100), 2)
                g[i], g[j] = g[j], g[i]

            c = costo(g)
            sin_mejora = 0
            T = min(T * 3, T0 * 0.5)

        T = max(T * alpha, 1e-6)

    return mejor, mc



# RECOCIDO SIMULADO — FASE 2
def fase2(g_base, seed, T0=2.0, alpha=0.99997, max_iter=5_000_000):

    random.seed(seed)

    g = g_base[:]

    for _ in range(3):
        i, j = random.sample(range(100), 2)
        g[i], g[j] = g[j], g[i]

    T = T0
    c = costo_ponderado(g)

    mejor = g[:]
    mc = costo(g)

    for _ in range(max_iter):

        i, j = random.sample(range(100), 2)
        g[i], g[j] = g[j], g[i]

        cn = costo_ponderado(g)
        delta = cn - c

        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            c = cn

            cc = costo(g)

            if cc < mc:
                mc = cc
                mejor = g[:]

            if mc == 0:
                return mejor, 0

        else:
            g[i], g[j] = g[j], g[i]

        T = max(T * alpha, 1e-6)

    return mejor, mc



# VISUALIZACIÓN DEL CUADRO
def pintar_cuadro(g):

    sf = sumas_filas(g)
    sc = sumas_cols(g)

    print("\n      ", end="")
    for c in range(N):
        print(f"C{c+1:02d} ", end="")
    print(" Σfila")

    print("     " + "-" * 55)

    for r in range(N):

        print(f"F{r+1:02d} |", end=" ")

        for c in range(N):
            print(f"{g[r*N+c]:3d}", end=" ")

        print(f"| {sf[r]}")

    print("     " + "-" * 55)

    print("Σcol ", end="")

    for c in range(N):
        print(f"{sc[c]:3d}", end=" ")

    print()

    print("\nDiagonal \\ =", diag1(g))
    print("Diagonal / =", diag2(g))



# MAIN
if __name__ == "__main__":

    inicio = time.time()

    mejor_f1 = None
    mc_f1 = float('inf')

    for seed in range(10):

        g, mc = fase1(seed)

        if mc < mc_f1:
            mc_f1 = mc
            mejor_f1 = g[:]

        if mc_f1 == 0:
            break

    if mc_f1 > 0:

        mejor_f2 = None
        mc_f2 = float('inf')

        for seed in range(20):

            g, mc = fase2(mejor_f1, seed)

            if mc < mc_f2:
                mc_f2 = mc
                mejor_f2 = g[:]

            if mc_f2 == 0:
                break

        solucion = mejor_f2
        mc_final = mc_f2

    else:

        solucion = mejor_f1
        mc_final = 0

    tiempo = time.time() - inicio

    print("\nCUADRO MAGICO 10x10\n")

    pintar_cuadro(solucion)

    print("\nMETRICAS\n")

    print("Tiempo total:", round(tiempo, 2), "segundos")
    print("Costo final:", mc_final)

    if mc_final == 0:
        print("Restricciones satisfechas: 22/22")
    else:
        sf = sumas_filas(solucion)
        sc = sumas_cols(solucion)

        print("Filas correctas:", sum(1 for s in sf if s == M), "/10")
        print("Columnas correctas:", sum(1 for s in sc if s == M), "/10")
        print("Diagonal \\:", diag1(solucion))
        print("Diagonal /:", diag2(solucion))