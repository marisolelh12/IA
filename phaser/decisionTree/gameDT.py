import pygame
import random
import numpy as np
import csv
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Generacion de datos de entrenamiento para el modelo DT
def generate_game_data(n_samples=1000):
    np.random.seed(42)
    distances = np.random.uniform(0, 100, n_samples)  # Distancia de la bala
    speeds = np.random.uniform(1, 20, n_samples)      # Velocidad de la bala
    labels = (distances / speeds < 5).astype(int)     # Saltar si se cumple la condicion
    data = np.column_stack((distances, speeds))
    return data, labels

# Entrenamiento del modelo con el csv
def train_model_from_csv(csv_file, arch_modelo):
    data = pd.read_csv(csv_file)
    X = data[['distance', 'speed']].values
    y = data['jump'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Modelo entrenado con accuracy: {accuracy * 100:.2f}%")
    with open(arch_modelo, 'wb') as file:
        pickle.dump(model, file)
    return model

# Configuracion del juego
pygame.init()

w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego con Árboles de Decisión")

# Cargar assets
fondo_img = pygame.image.load('assets/game/fondo2.png')
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]
bala_img = pygame.image.load('assets/sprites/purple_ball.png')

fondo_img = pygame.transform.scale(fondo_img, (w, h))
jugador_frames = [pygame.transform.scale(img, (40, 50)) for img in jugador_frames]
bala_img = pygame.transform.scale(bala_img, (30, 30))

# Crear el rectángulo del jugador y de la bala
jugador_rect = pygame.Rect(50, h - 100, 32, 48)
bala_rect = pygame.Rect(w - 50, h - 90, 16, 16)
bala_speed = random.randint(4, 10)

reloj = pygame.time.Clock()
correr = True
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Dataset
datos_entrenamiento = []
dataset = "game_datos_entrenamiento.csv"
arch_modelo = "trained_decision_tree.pkl"

# Revisar si hay modelo
try:
    with open(arch_modelo, 'rb') as file:
        dt_classifier = pickle.load(file)
    print("Modelo cargado.")
except FileNotFoundError:
    print("No se encontro un modelo.")
    dt_classifier = None

# Guardar dataset en csv
def guardar_datos(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["distance", "speed", "jump"])
        writer.writerows(data)

# Function to append dataset to a CSV file without overwriting
def append_data_to_csv(data, filename):
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Only write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(["distance", "speed", "jump"])
            writer.writerows(data)
    except FileNotFoundError:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["distance", "speed", "jump"])
            writer.writerows(data)

# Function to display menu and select mode
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    manual_text = font.render("Presiona 'M' para Manual", True, (255, 255, 255))
    auto_text = font.render("Presiona 'A' para Automático", True, (255, 255, 255))
    quit_text = font.render("Presiona 'Q' para Salir", True, (255, 255, 255))

    pantalla.blit(manual_text, (w // 2 - manual_text.get_width() // 2, h // 2 - 60))
    pantalla.blit(auto_text, (w // 2 - auto_text.get_width() // 2, h // 2))
    pantalla.blit(quit_text, (w // 2 - quit_text.get_width() // 2, h // 2 + 60))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return False  # Manual mode
                elif event.key == pygame.K_a:
                    return True  # Automatic mode
                elif event.key == pygame.K_q:
                    print("Juego terminado. Gracias por jugar.")
                    pygame.quit()
                    exit()

# Display menu and select mode
auto_mode = mostrar_menu()

#Loop
while correr:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
        if not auto_mode and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and en_suelo:
                salto = True
                en_suelo = False

    # Actualizar posicion de la bala
    bala_rect.x -= bala_speed
    if bala_rect.x < 0:
        bala_rect.x = w - 50
        bala_speed = random.randint(3, 10)

    if auto_mode and dt_classifier and bala_rect.x > 0 and en_suelo:
        distance_to_bala = abs(jugador_rect.x - bala_rect.x)
        prediction = dt_classifier.predict([[distance_to_bala, bala_speed]])
        if prediction[0] == 1:
            salto = True
            en_suelo = False

    if salto:
        jugador_rect.y -= salto_altura
        salto_altura -= gravedad
        if jugador_rect.y >= h - 100:
            jugador_rect.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

    if not auto_mode:
        jump_label = 1 if salto else 0
        distance_to_bala = abs(jugador_rect.x - bala_rect.x)
        datos_entrenamiento.append([distance_to_bala, bala_speed, jump_label])

    # Colision
    if jugador_rect.colliderect(bala_rect):
        print("Colisión detectada!")
        correr = False

    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar todo
    pantalla.blit(fondo_img, (0, 0))
    pantalla.blit(jugador_frames[current_frame], (jugador_rect.x, jugador_rect.y))
    pantalla.blit(bala_img, (bala_rect.x, bala_rect.y))

    # Actualizar la pantalla
    pygame.display.flip()
    reloj.tick(30)  # Limitar el juego a 30 FPS

# Save or append the dataset to CSV when the game ends
if not auto_mode:
    append_data_to_csv(datos_entrenamiento, dataset)
    print(f"Dataset appended to {dataset}")
else:
    print("Automatic mode: No data saved to CSV.")

# Train the model after the game ends
if not auto_mode:
    train_model_from_csv(dataset, arch_modelo)

pygame.quit()