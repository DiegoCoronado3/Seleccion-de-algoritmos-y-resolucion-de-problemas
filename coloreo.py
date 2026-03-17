import time

def leer_mapa(nombre_archivo):

    grafo = {}

    with open(nombre_archivo, "r") as f:

        for linea in f:

            linea = linea.strip()

            if ":" not in linea:
                continue

            pais, vecinos = linea.split(":")

            vecinos = vecinos.split(",")

            grafo[pais.strip()] = [v.strip() for v in vecinos if v.strip()]

    return grafo


# Verificar si un color es válido
def es_valido(pais, color, asignacion, grafo):

    for vecino in grafo[pais]:

        if vecino in asignacion and asignacion[vecino] == color:
            return False

    return True


# Heurística LCV
# Ordena colores por el que menos restringe
def ordenar_lcv(pais, k, asignacion, grafo):

    colores = list(range(k))
    impacto = []

    for color in colores:

        restricciones = 0

        for vecino in grafo[pais]:

            if vecino not in asignacion:

                restricciones += 1

        impacto.append((restricciones, color))

    impacto.sort()

    return [color for _, color in impacto]


# -------------------------------------------------
# Backtracking
# -------------------------------------------------
def colorear_bt(paises, grafo, k, asignacion, i, contador):

    contador[0] += 1

    if i == len(paises):
        return True

    pais = paises[i]

    colores = ordenar_lcv(pais, k, asignacion, grafo)

    for color in colores:

        if es_valido(pais, color, asignacion, grafo):

            asignacion[pais] = color

            if colorear_bt(paises, grafo, k, asignacion, i + 1, contador):
                return True

            del asignacion[pais]

    return False



# Buscar mínimo número de colores
def minimo_colores(grafo):

    paises = list(grafo.keys())

    paises.sort(key=lambda x: len(grafo[x]), reverse=True)

    for k in range(1, len(paises) + 1):

        asignacion = {}
        contador = [0]

        if colorear_bt(paises, grafo, k, asignacion, 0, contador):
            return k, asignacion, contador[0]

    return None

def resolver(nombre_archivo):

    grafo = leer_mapa(nombre_archivo)

    inicio = time.time()

    colores, solucion, pasos = minimo_colores(grafo)

    fin = time.time()

    print("\nArchivo:", nombre_archivo)
    print("Colores mínimos:", colores)
    print("Pasos de búsqueda:", pasos)
    print("Tiempo:", round(fin - inicio, 4), "segundos")

    print("\nAsignación de colores:")

    for pais in sorted(solucion.keys()):
        print(pais, "->", solucion[pais])


# Programa principal
def main():

    resolver("mapa_5_paises_adyacencias.txt")

    resolver("mapa_100_paises_adyacencias.txt")


if __name__ == "__main__":
    main()