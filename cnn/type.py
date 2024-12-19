import os
from PIL import Image
import numpy as np

def convert_images_to_uint8(input_folder, output_folder):
    """
    Convierte imágenes en una carpeta a formato RGB estándar con tipo de datos uint8.
    Guarda las imágenes convertidas en una carpeta de salida.
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recorrer todas las imágenes en la carpeta de entrada
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            
            try:
                # Abrir la imagen con Pillow
                img = Image.open(input_path).convert("RGB")  # Convertir a RGB

                # Convertir la imagen a un arreglo NumPy
                img_array = np.asarray(img, dtype=np.float32)  # Convertir a float32
                img_array = np.clip(img_array, 0, 255)  # Asegurar valores en [0, 255]
                img_array = img_array.astype(np.uint8)  # Convertir a uint8
                
                # Volver a convertir a imagen Pillow y guardar
                img_uint8 = Image.fromarray(img_array, "RGB")
                img_uint8.save(output_path)
                
                print(f"Procesada: {file_name}")
            
            except Exception as e:
                print(f"Error procesando {file_name}: {e}")

# Uso
input_folder = "dataset/vocho"
output_folder = "C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/type"

convert_images_to_uint8(input_folder, output_folder)
print("Conversión completada.")
