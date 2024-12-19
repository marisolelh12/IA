import os
import numpy as np
from PIL import Image

def verify_image_shapes(input_folder, expected_shape=(128, 128, 3)):
    """
    Verifica las dimensiones y el tipo de datos de todas las imágenes en la carpeta.
    
    Parámetros:
    - input_folder: Carpeta que contiene las imágenes.
    - expected_shape: Forma esperada de las imágenes (por defecto 128x128x3).
    """
    images = []  # Lista para almacenar imágenes cargadas
    image_paths = []  # Almacena las rutas de las imágenes
    
    # Recorrer todas las imágenes en la carpeta
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(input_folder, file_name)
            try:
                # Abrir y cargar la imagen
                img = Image.open(img_path).convert("RGB")
                img_resized = img.resize((expected_shape[0], expected_shape[1]))  # Redimensionar si es necesario
                img_array = np.array(img_resized, dtype=np.uint8)  # Convertir a arreglo NumPy uint8
                
                # Agregar la imagen y su ruta
                images.append(img_array)
                image_paths.append(img_path)
            except Exception as e:
                print(f"Error procesando {img_path}: {e}")
    
    # Verificar dimensiones y tipo de datos
    print("\n--- Verificación de imágenes ---\n")
    for i, img in enumerate(images):
        print(f"Imagen {i}: {image_paths[i]}")
        print(f" -> Shape = {img.shape}, dtype = {img.dtype}")
        if img.shape != expected_shape:
            print(f" -> ⚠ Problema detectado en la imagen: {image_paths[i]}")
    print("\n--- Verificación completada ---\n")

# Uso
if __name__ == "__main__":
    input_folder = "C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/DATASET/march"  # Cambia esta ruta
    verify_image_shapes(input_folder, expected_shape=(128, 128, 3))
