from PIL import Image

def remove_background(input_image_path, output_image_path):
    """Abrir la imagen de entrada"""
    img = Image.open(input_image_path).convert("RGBA")

    # Obtener los datos de la imagen
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Cambiar todos los blancos (y tonos de blanco) a transparente
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    # Actualizar los datos de la imagen
    img.putdata(new_data)

    # Guardar la imagen sin fondo
    img.save(output_image_path, "PNG")

# Ejemplo de uso
input_image_path = "C:\\Users\\es44319413t\\Downloads\\Escudo_Vectorizado.ai.png"
output_image_path = "C:\\Users\\es44319413t\\Downloads\\logoBARAJASLIMPIO.png"
remove_background(input_image_path, output_image_path)

print(f"El fondo se ha eliminado de {input_image_path} y se ha guardado en {output_image_path}.")