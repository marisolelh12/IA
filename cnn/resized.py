import os
from PIL import Image

# Ruta al directorio de origen y destino
source_dir = 'C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/DATASET/vocho'
output_dir = 'C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/DATASET/vocho_resized'

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Recorrer los directorios y redimensionar las imágenes
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):            
            # Crear el path completo para la imagen
            img_path = os.path.join(root, file)
            
            try:
                # Leer la imagen con Pillow
                with Image.open(img_path) as img:
                    # Convertir a modo RGB si es RGBA o escala de grises
                    if img.mode != "RGB":
                        img = img.convert("RGB")

                    # Redimensionar la imagen a 128x128
                    img_resized = img.resize((21, 28))
                    
                    # Crear la estructura de directorios de salida
                    relative_path = os.path.relpath(root, source_dir)
                    output_path = os.path.join(output_dir, relative_path)
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    
                    # Guardar la imagen redimensionada en formato JPEG
                    output_file_path = os.path.join(output_path, os.path.splitext(file)[0] + ".jpg")
                    img_resized.save(output_file_path, "JPEG")

            except Exception as e:
                print(f"Error procesando la imagen {img_path}: {e}")

print(f"Todas las imágenes han sido redimensionadas y guardadas en: {output_dir}")