# Monitor de Imágenes Recientes

Este proyecto es una aplicación Flask que monitorea una carpeta específica en busca de la imagen más reciente modificada en la fecha actual y la muestra en una página web.

## Requisitos

- Python 3.x
- Flask

## Instalación

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Navega al directorio del proyecto.

```bash
cd /ruta/al/directorio/del/proyecto
```

3. Instala las dependencias necesarias.

```bash
pip install flask
```

## Configuración

1. Asegúrate de que la carpeta que deseas monitorear está configurada correctamente en el archivo `app.py`. Por defecto, está configurada para monitorear `/ruta/a/la/carpeta/monitoreada`.

```python
# ...existing code...
CARPETA_IMAGENES = '/ruta/a/la/carpeta/monitoreada'
# ...existing code...
```

## Ejecución

1. Ejecuta el archivo `app.py` para iniciar el servidor Flask.

```bash
python app.py
```

2. Abre tu navegador web y navega a `http://localhost:5000`.

## Uso

- La página principal mostrará la imagen más reciente modificada en la fecha actual en la carpeta monitoreada.
- La página se actualizará automáticamente cada minuto para mostrar la imagen más reciente.

## Notas

- Si la carpeta `templates` no existe, se creará automáticamente.
- Si el archivo `index.html` no existe en la carpeta `templates`, se creará automáticamente con el contenido necesario.
