# Genera el QR
import qrcode
from PIL import Image


qr = qrcode.QRCode(version=1, box_size=10, border=5)
data = "https://www.bau360.es/"
qr.add_data(data)
img = qr.make_image(fill_color="black", back_color="white")
img.save("PruebasQR.png")

# Abre la imagen del código QR
ruta_qr = "PruebasQR.png"
imagen_qr = Image.open(ruta_qr).convert("RGBA")

# Abre la imagen del logo a superponer
ruta_logo = "C:/Users/es44319413t/Desktop/logobau360.png"
imagen_logo = Image.open(ruta_logo).convert("RGBA")

# Calcula el nuevo tamaño del logo
nuevo_ancho = int(imagen_logo.width // 8)
nuevo_alto = int(imagen_logo.height // 8)
imagen_logo = imagen_logo.resize((nuevo_ancho, nuevo_alto))

# Calcula la posición para superponer el logo
posicion_x = (imagen_qr.width - imagen_logo.width) // 2
posicion_y = (imagen_qr.height - imagen_logo.height) // 2

# Pega el logo en la imagen del código QR
imagen_qr.paste(imagen_logo, (posicion_x, posicion_y), imagen_logo)

# Guarda el resultado como una nueva imagen
ruta_imagen_resultante = "QRLogo.png"
imagen_qr.save(ruta_imagen_resultante)

# Imprime un mensaje de éxito
print(f"El logo se ha insertado en el código QR y se ha guardado como {ruta_imagen_resultante}.")
