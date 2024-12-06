import pygame
import sys
import heapq

# Inicialización de Pygame
pygame.init()

# Tamaño de la ventana
ANCHO, ALTO = 480, 480
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo A*")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255,255,53)

# Dimensiones del grid
tamano_celda = 40
columnas = 12
filas = 12

# Nodos de inicio y final
inicio = (0, 0)
fin = (columnas - 1, filas - 1)

# Obstáculos
obstaculos = [[False for _ in range(filas)] for _ in range(columnas)]

# Lista cerrada
lista_cerrada = set()

# Heurística de Manhattan
def heuristica(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

# Implementación de A*
def a_estrella(inicio, fin):
    lista_abierta = []
    heapq.heappush(lista_abierta, (0, inicio))
    came_from = {}
    g_score = {inicio: 0}
    f_score = {inicio: heuristica(inicio, fin)}
    en_lista_abierta = {inicio}

    while lista_abierta:
        _, actual = heapq.heappop(lista_abierta)
        en_lista_abierta.remove(actual)

        if actual == fin:
            return reconstruir_camino(came_from, actual)

        lista_cerrada.add(actual)

        vecinos = obtener_vecinos(actual)
        for vecino in vecinos:
            if vecino in lista_cerrada or obstaculos[vecino[0]][vecino[1]]:
                continue

            tentative_g_score = g_score[actual] + 1

            if vecino not in en_lista_abierta or tentative_g_score < g_score.get(vecino, float('inf')):
                came_from[vecino] = actual
                g_score[vecino] = tentative_g_score
                f_score[vecino] = tentative_g_score + heuristica(vecino, fin)
                if vecino not in en_lista_abierta:
                    heapq.heappush(lista_abierta, (f_score[vecino], vecino))
                    en_lista_abierta.add(vecino)

    return None

# Reconstrucción del camino final
def reconstruir_camino(came_from, actual):
    camino = [actual]
    while actual in came_from:
        actual = came_from[actual]
        camino.append(actual)
    camino.reverse()
    return camino

# Obtener vecinos de un nodo dado
def obtener_vecinos(nodo):
    (x, y) = nodo
    vecinos = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < columnas and 0 <= ny < filas:
            vecinos.append((nx, ny))
    return vecinos

# Imprimir lista cerrada
def imprimir_lista_cerrada():
    print("Lista Cerrada:")
    print("+--------+--------+")
    print("|   X    |   Y    |")
    print("+--------+--------+")
    for nodo in sorted(lista_cerrada):
        x, y = nodo
        print(f"| {x:6} | {y:6} |")
    print("+--------+--------+")

# Ciclo principal
camino = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // tamano_celda, y // tamano_celda
            obstaculos[grid_x][grid_y] = not obstaculos[grid_x][grid_y]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lista_cerrada.clear()
                camino = a_estrella(inicio, fin) or []
                imprimir_lista_cerrada()

    # Rellenar la ventana
    ventana.fill(BLANCO)

    # Dibujar el grid
    for x in range(columnas):
        for y in range(filas):
            color = NEGRO if obstaculos[x][y] else BLANCO
            pygame.draw.rect(ventana, color, (x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda))
            pygame.draw.rect(ventana, NEGRO, (x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda), 1)

    # Dibujar el camino encontrado
    for (x, y) in camino:
        pygame.draw.rect(ventana, AMARILLO, (x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda))

    # Dibujar nodos de inicio y fin
    pygame.draw.rect(ventana, AZUL, (inicio[0] * tamano_celda, inicio[1] * tamano_celda, tamano_celda, tamano_celda))
    pygame.draw.rect(ventana, VERDE, (fin[0] * tamano_celda, fin[1] * tamano_celda, tamano_celda, tamano_celda))

    # Actualizar la pantalla
    pygame.display.flip()