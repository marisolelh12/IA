from PIL import Image, ImageEnhance
import os

def augment_images(input_folder, output_folder):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Obtener lista de imágenes en la carpeta de entrada
    images = [f for f in os.listdir(input_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
    
    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        img = Image.open(img_path).convert("RGB")  # Convertir a RGB
        
        # Rotaciones
        for angle in [15, 45, 90, 180]:
            rotated = img.rotate(angle, expand=True).resize((28, 21))
            rotated.save(os.path.join(output_folder, f"{os.path.splitext(img_name)[0]}_rotated_{angle}.jpg"), "JPEG", quality=85)
        
        # Ajustes de brillo
        for factor in [0.5, 1.5, 2.0]:
            enhancer = ImageEnhance.Brightness(img)
            brightened = enhancer.enhance(factor).resize((28, 21))
            brightened.save(os.path.join(output_folder, f"{os.path.splitext(img_name)[0]}_bright_{factor}.jpg"), "JPEG", quality=85)
        
        # Nueva transformación: Flip horizontal
        flipped = img.transpose(Image.FLIP_LEFT_RIGHT).resize((28, 21))
        flipped.save(os.path.join(output_folder, f"{os.path.splitext(img_name)[0]}_flipped.jpg"), "JPEG", quality=85)

if __name__ == "__main__":
    # Carpeta de entrada y salida
    input_folder = "C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/DATASET/vocho"
    output_folder = "C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/IA/cnn/dataset/vocho"
    
    augment_images(input_folder, output_folder)
    print("Aumentación de datos completada.")
