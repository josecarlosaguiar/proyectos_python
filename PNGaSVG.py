from PIL import Image
import svgwrite

def png_to_svg(png_path, svg_path):
    # Abre la imagen PNG
    img = Image.open(png_path)
    width, height = img.size

    # Crea un nuevo archivo SVG
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(width, height))

    # Convierte cada píxel a un rectángulo en el SVG
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if len(pixel) == 4:  # Si el píxel tiene canal alfa
                r, g, b, a = pixel
                if a > 0:  # Solo dibuja píxeles no transparentes
                    color = svgwrite.rgb(r, g, b, '%')
                    dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=color))
            else:  # Si el píxel no tiene canal alfa
                r, g, b = pixel
                color = svgwrite.rgb(r, g, b, '%')
                dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=color))

    # Guarda el archivo SVG
    dwg.save()

# Ruta del archivo PNG de entrada
input_png = r"C:\Users\es44319413t\Desktop\JaimeIV.png"

# Ruta del archivo SVG de salida
output_svg = r"C:\Users\es44319413t\Downloads\Jaime_vectorialII.svg"

# Convierte PNG a SVG
png_to_svg(input_png, output_svg)
