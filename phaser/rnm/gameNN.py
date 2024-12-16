import pygame
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generacion de datos de entrenamiento para el modelo NN
def generate_game_data(n_samples=1000):
    distances = np.random.uniform(0, 100, n_samples)
    speeds = np.random.uniform(1, 20, n_samples)
    labels = (distances / speeds < 5).astype(int)
    data = np.column_stack((distances, speeds))
    return data, labels

def train_neural_network_from_data(training_data):
    if len(training_data) == 0:
        print("Error: No hat datos de entrenamiento disponibles.")
        return None

    data = np.array([[entry['distance'], entry['speed'], entry['jump']] for entry in training_data])
    X = data[:, :2]
    y = data[:, 2] 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        Dense(4, input_dim=2, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print("Entrenamiento de la red neuronal...")
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Modelo entrenado con precisión de: {accuracy * 100:.2f}%")

    return model

# Configuracion del juego
pygame.init()

w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego con Redes Neuronales")

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
jugador_rect = pygame.Rect(50, h - 100, 40, 50)
bala_rect = pygame.Rect(w - 100, h - 80, 30, 30)
bala_speed = random.randint(4, 10)

reloj = pygame.time.Clock()
correr = True
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables para la animación del jugador
current_frame = 0
frame_count = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen

# Datos de entrenamiento
training_data = []
nn_model = None

# Menu
def mostrar_menu():
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

auto_mode = mostrar_menu()

# Loop
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
        bala_speed = random.randint(4, 10)

    if auto_mode:
        if nn_model is None:
            print("Error: No hay ningún modelo entrenado disponible.")
            auto_mode = mostrar_menu()
            continue

        if bala_rect.x > 0 and en_suelo:
            distance_to_ball = abs(jugador_rect.x - bala_rect.x)
            prediction = nn_model.predict(np.array([[distance_to_ball, bala_speed]]), verbose=0)
            print(f"Predicción de distance={distance_to_ball}, ={bala_speed}: {prediction[0][0]:.2f}")
            if prediction[0][0] >= 0.5:
                print("Salto!")
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
        distance_to_ball = abs(jugador_rect.x - bala_rect.x)
        training_data.append({
            'distance': distance_to_ball,
            'speed': bala_speed,
            'jump': jump_label
        })

    # Colision
    if jugador_rect.colliderect(bala_rect):
        print("Colisión detectada!")

        if not auto_mode and len(training_data) > 0:
            print(f"Datos de formación recopilados: {len(training_data)} samples. Entrenando modelo...")
            nn_model = train_neural_network_from_data(training_data)
            if nn_model is not None:
                print("Modelo entrenado con éxito.")
            else:
                print("Falló el entrenamiento del modelo.")

        auto_mode = mostrar_menu()
        bala_rect.x = w - 50
        bala_speed = random.randint(4, 10)
        jugador_rect.y = h - 100
        salto = False
        en_suelo = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            print("Reiniciando juego...")
            bala_rect.x = w - 50
            bala_speed = random.randint(4, 10)
            jugador_rect.y = h - 100
            salto = False
            en_suelo = True
            break
        else:
            continue
            break

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
    reloj.tick(30)   # Limitar el juego a 30 FPS

if not auto_mode:
    print("Datos de entrenamiento recopilados. Entrenando modelo...")
    print(f"Recolectadas {len(training_data)} samples de datos de entrenamiento.")
    for i, data_point in enumerate(training_data[:10]):
        print(f"Sample {i + 1}: Distance={data_point['distance']}, Speed={data_point['speed']}, Jump={data_point['jump']}")
    nn_model = train_neural_network_from_data(training_data)
    if nn_model is not None:
        print("Modelo entrenado y listo para predicciones.")
else:
    print("Auto mode: No se han recogido datos de entrenamiento. Juego en modo Manual.")

pygame.quit()