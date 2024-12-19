import pygame
import sys
import heapq

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_camino(self):
        self.color = VERDE

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col])
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col])
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila][self.col + 1])
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila][self.col - 1])
        # Diagonales
        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col - 1])
        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col + 1])
        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col - 1])
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col + 1])

# Distancia de Manhattan
def heuristica(a, b):
    x1, y1 = a
    x2, y2 = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx + dy + (1.4 - 2) * min(dx, dy)

# Implementación del algoritmo A*
def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    contador = 0
    lista_abierta = []
    heapq.heappush(lista_abierta, (0, contador, inicio))
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())
    lista_abierta_hash = {inicio}
    lista_cerrada = set()

    while lista_abierta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        actual = heapq.heappop(lista_abierta)[2]
        lista_abierta_hash.remove(actual)

        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            imprimir_lista_cerrada(lista_cerrada)
            return True

        for vecino in actual.vecinos:
            tentative_g_score = g_score[actual] + (1.4 if abs(vecino.fila - actual.fila) + abs(vecino.col - actual.col) == 2 else 1)  # Diagonal: costo 1.4, ortogonal: costo 1

            if tentative_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = tentative_g_score
                f_score[vecino] = tentative_g_score + heuristica(vecino.get_pos(), fin.get_pos())
                if vecino not in lista_abierta_hash:
                    contador += 1
                    heapq.heappush(lista_abierta, (f_score[vecino], contador, vecino))
                    lista_abierta_hash.add(vecino)

        dibujar()

        if actual != inicio:
            actual.hacer_cerrado()
            lista_cerrada.add(actual)

    return False

# Reconstrucción del camino encontrado
def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        if actual.color != NARANJA:
            actual.hacer_camino()
        dibujar()

# Imprimir la lista cerrada
def imprimir_lista_cerrada(lista_cerrada):
    print("Lista Cerrada:")
    print("+--------+--------+")
    print("|   Fila |   Col  |")
    print("+--------+--------+")
    for nodo in sorted(lista_cerrada, key=lambda n: (n.fila, n.col)):
        print(f"| {nodo.fila:6} | {nodo.col:6} |")
    print("+--------+--------+")

# Crear la grilla de nodos
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

# Dibujar la grilla
def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

# Dibujar todo en la ventana
def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

# Obtener la posición de click
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

# Función principal
def main(ventana, ancho):
    FILAS = 7
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)