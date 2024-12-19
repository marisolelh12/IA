import os
from rembg import remove
from PIL import Image

def remove_background_batch(input_folder, output_folder):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recorrer todos los archivos de la carpeta
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Procesar solo archivos de imagen
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                # Leer la imagen y eliminar el fondo
                with open(input_path, "rb") as f:
                    input_image = f.read()
                    output_image = remove(input_image)
                
                # Guardar la imagen sin fondo
                with open(output_path, "wb") as f:
                    f.write(output_image)
                
                print(f"Procesado: {file_name}")
            except Exception as e:
                print(f"Error procesando {file_name}: {e}")

# Uso
input_folder = "C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/DATASET/aveo"
output_folder = "C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/DATASET/sFondo"
remove_background_batch(input_folder, output_folder)
print("El procesamiento de imágenes ha finalizado.")