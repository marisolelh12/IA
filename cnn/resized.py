import os
from PIL import Image

# Ruta al directorio de origen y destino
source_dir = 'C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/IA/cnn/dataset/sentra'
output_dir = 'C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/IA/cnn/dataset/sentra_resized'

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Recorrer los directorios y redimensionar las imágenes
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            # Crear el path completo para la imagen
            img_path = os.path.join(root, file)
            
            # Leer la imagen con Pillow
            with Image.open(img_path) as img:
                # Redimensionar la imagen a 128x128
                img_resized = img.resize((28, 21))
                
                # Crear la estructura de directorios de salida
                relative_path = os.path.relpath(root, source_dir)
                output_path = os.path.join(output_dir, relative_path)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                
                # Guardar la imagen redimensionada
                output_file_path = os.path.join(output_path, file)
                img_resized.save(output_file_path)

print(f"Todas las imágenes han sido redimensionadas y guardadas en: {output_dir}")
