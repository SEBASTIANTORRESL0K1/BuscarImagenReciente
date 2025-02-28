import os
import glob
from datetime import datetime

def obtener_imagen_mas_reciente(carpeta_imagenes):
    # Obtener la lista de archivos en la carpeta de imágenes
    lista_imagenes = glob.glob(os.path.join(carpeta_imagenes, '*'))
    
    # Filtrar solo los archivos que son imágenes (puedes agregar más extensiones si es necesario)
    lista_imagenes = [imagen for imagen in lista_imagenes if imagen.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()
    
    # Filtrar las imágenes que fueron modificadas en la fecha actual
    lista_imagenes = [imagen for imagen in lista_imagenes if datetime.fromtimestamp(os.path.getmtime(imagen)).date() == fecha_actual]
    
    # Verificar si hay imágenes en la carpeta
    if not lista_imagenes:
        return None
    
    # Obtener la imagen más reciente
    imagen_mas_reciente = max(lista_imagenes, key=os.path.getmtime)
    
    return imagen_mas_reciente

# Ejemplo de uso
carpeta_imagenes = 'C:/Users/sseba/OneDrive/Escritorio/4I/SERVICIO SOCIAL/PYTHON/imagenes'
imagen_reciente = obtener_imagen_mas_reciente(carpeta_imagenes)
if imagen_reciente:
    print(f'La imagen más reciente es: {imagen_reciente}')
else:
    print('No se encontraron imágenes en la carpeta.')