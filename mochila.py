import csv, time, random, math

def titulo(texto):
    linea = "═" * (len(texto) + 4)
    print(f"\n╔{linea}╗")
    print(f"║  {texto}  ║")
    print(f"╚{linea}╝\n")

def seccion(texto):
    print(f"\n{texto}")
    print("─" * 50)

def leer_mochila(path):
    items = []
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            items.append({
                'id':    int(row['id_objeto']),
                'peso':  int(row['peso']),
                'valor': int(row['valor'])
            })
    return items

def evaluar(sol, items, cap, lam=1000):
    peso  = sum(items[i]['peso']  for i in range(len(sol)) if sol[i])
    valor = sum(items[i]['valor'] for i in range(len(sol)) if sol[i])
    exceso = max(0, peso - cap)
    return valor - lam * exceso, peso, valor

def recocido_simulado(items, cap, T0=5000, alpha=0.995, iteraciones=50000, seed=42):
    random.seed(seed)
    n = len(items)
    sol = [random.randint(0, 1) for _ in range(n)]
    fit, _, _ = evaluar(sol, items, cap)
    mejor = sol[:]
    mejor_fit, mejor_peso, mejor_val = evaluar(sol, items, cap)
    T = T0

    for it in range(iteraciones):
        i = random.randint(0, n - 1)
        vecino = sol[:]
        vecino[i] ^= 1
        vfit, _, _ = evaluar(vecino, items, cap)
        delta = vfit - fit

        if delta > 0 or random.random() < math.exp(delta / max(T, 1e-10)):
            sol, fit = vecino, vfit
            if fit > mejor_fit:
                mejor = sol[:]
                mejor_fit, mejor_peso, mejor_val = evaluar(sol, items, cap)

        T *= alpha

    return mejor, mejor_peso, mejor_val


def dp_exacto(items, cap):
    n = len(items)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        p, v = items[i-1]['peso'], items[i-1]['valor']
        for w in range(cap + 1):
            dp[i][w] = dp[i-1][w]
            if w >= p:
                dp[i][w] = max(dp[i][w], dp[i-1][w-p] + v)

    w, sel = cap, []

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            sel.append(items[i-1]['id'])
            w -= items[i-1]['peso']

    return dp[n][cap], sorted(sel)


def mostrar_mochila(items, sol_ids, peso, valor, cap, iters, tiempo, val_dp=None):

    sel = set(sol_ids)

    print("\n   ID   Peso   Valor  Val/Kg    Estado")
    print("  " + "─"*45)

    for it in items:
        elegido = it['id'] in sel
        ratio = it['valor'] / it['peso']
        estado = "elegido" if elegido else "omitido"

        print(f"{it['id']:>5} {it['peso']:>6} {it['valor']:>7} {ratio:>7.1f}   {estado}")

    seccion("Resumen")

    cumple = peso <= cap
    simbolo = "CUMPLE" if cumple else "VIOLA"

    print(f"Objetos seleccionados: {sorted(sol_ids)}")
    print(f"Peso total:            {peso}")
    print(f"Valor total:           {valor}")
    print(f"Restricción de peso:   {simbolo}")
    print(f"Iteraciones:           {iters}")
    print(f"Tiempo de ejecución:   {tiempo:.3f} s")

    if val_dp is not None:
        es_optimo = valor == val_dp
        marca = "ES ÓPTIMO" if es_optimo else "subóptimo"
        print(f"Valor óptimo (DP):     {val_dp}  → {marca}")


if __name__ == "__main__":


    titulo("MOCHILA 0/1 — 10 OBJETOS   (capacidad = 38 kg)")

    items10 = leer_mochila("mochila_10.csv")
    CAP10   = 38

    t0 = time.time()
    sol10, peso10, val10 = recocido_simulado(
        items10, CAP10, T0=3000, alpha=0.99, iteraciones=30000)
    t10 = time.time() - t0

    val_dp, sel_dp = dp_exacto(items10, CAP10)

    ids10 = [items10[i]['id'] for i in range(len(sol10)) if sol10[i]]

    mostrar_mochila(
        items10, ids10, peso10, val10, CAP10,
        iters=300, tiempo=t10, val_dp=val_dp
    )

    titulo("MOCHILA 0/1 — 100 OBJETOS   (capacidad = 1097 kg)")

    items100 = leer_mochila("mochila_100.csv")
    CAP100   = 1097

    t0 = time.time()
    sol100, peso100, val100 = recocido_simulado(
        items100, CAP100, T0=5000, alpha=0.995, iteraciones=80000)
    t100 = time.time() - t0

    val_dp, sel_dp = dp_exacto(items100, CAP100)

    ids100 = [items100[i]['id'] for i in range(len(sol100)) if sol100[i]]

    mostrar_mochila(
        items100, ids100, peso100, val100, CAP100,
        iters=800, tiempo=t100, val_dp=val_dp
    )

    print("\n" + "═"*52 + "\n")