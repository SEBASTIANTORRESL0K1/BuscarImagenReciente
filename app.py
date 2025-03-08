import os
import glob
from datetime import datetime
from flask import Flask, render_template, jsonify, send_file

app = Flask(__name__)

# Carpeta que deseas monitorear
CARPETA_IMAGENES = 'C:/Users/sseba/Pictures/Screenshots'

def obtener_imagen_mas_reciente(carpeta_imagenes):
    """
    Obtiene la imagen más reciente en una carpeta de imágenes que fue modificada en la fecha actual.
    Args:
        carpeta_imagenes (str): La ruta de la carpeta que contiene las imágenes.
    Returns:
        str: La ruta de la imagen más reciente modificada en la fecha actual. 
             Si no hay imágenes modificadas en la fecha actual, retorna None.
    """
    # Obtener la lista de archivos en la carpeta de imágenes
    lista_imagenes = glob.glob(os.path.join(carpeta_imagenes, '*'))
    
    # Filtrar solo los archivos que son imágenes
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obtener_imagen_reciente')
def obtener_imagen_reciente_ruta():
    imagen = obtener_imagen_mas_reciente(CARPETA_IMAGENES)
    if imagen:
        timestamp = os.path.getmtime(imagen)
        fecha = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        nombre_archivo = os.path.basename(imagen)
        return jsonify({
            'existe': True,
            'nombre': nombre_archivo,
            'ruta': f'/imagen/{nombre_archivo}',
            'fecha': fecha
        })
    else:
        return jsonify({
            'existe': False,
            'mensaje': 'No se encontraron imágenes en la carpeta para la fecha actual.'
        })

@app.route('/imagen/<nombre_archivo>')
def servir_imagen(nombre_archivo):
    # Construir la ruta completa a la imagen
    ruta_imagen = os.path.join(CARPETA_IMAGENES, nombre_archivo)
    # Verificar que el archivo existe y está dentro de la carpeta permitida
    if os.path.exists(ruta_imagen) and os.path.dirname(os.path.abspath(ruta_imagen)) == os.path.abspath(CARPETA_IMAGENES):
        return send_file(ruta_imagen)
    else:
        return "Imagen no encontrada", 404

if __name__ == '__main__':
    # Crear directorio templates si no existe
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Crear el archivo index.html en el directorio templates
    index_html_path = os.path.join(templates_dir, 'index.html')
    
    # Solo crear el archivo si no existe
    if not os.path.exists(index_html_path):
        with open(index_html_path, 'w', encoding='utf-8') as f:
            f.write("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Imágenes Recientes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        #imagen-contenedor {
            margin-top: 20px;
        }
        #imagen-reciente {
            max-width: 100%;
            border: 1px solid #ddd;
        }
        #info {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Monitor de Imágenes Recientes</h1>
    
    <div id="info">
        <p>Carpeta monitoreada: <span id="carpeta-path"></span></p>
        <p>Última actualización: <span id="ultima-actualizacion">-</span></p>
    </div>
    
    <div id="status">Buscando imágenes recientes...</div>
    
    <div id="imagen-contenedor">
        <img id="imagen-reciente" style="display: none;" alt="Imagen más reciente">
    </div>
    
    <script>
        // Establecer la ruta de la carpeta monitoreada
        document.getElementById('carpeta-path').textContent = 'C:/Users/sseba/OneDrive/Imagenes';
        
        // Función para actualizar la imagen
        function actualizarImagen() {
            fetch('/obtener_imagen_reciente')
                .then(response => response.json())
                .then(data => {
                    const horaActual = new Date().toLocaleTimeString();
                    document.getElementById('ultima-actualizacion').textContent = horaActual;
                    
                    if (data.existe) {
                        document.getElementById('status').textContent = `Imagen encontrada: ${data.nombre} (${data.fecha})`;
                        const imagen = document.getElementById('imagen-reciente');
                        // Añadir timestamp para evitar caché
                        imagen.src = `${data.ruta}?t=${new Date().getTime()}`;
                        imagen.style.display = 'block';
                    } else {
                        document.getElementById('status').textContent = data.mensaje;
                        document.getElementById('imagen-reciente').style.display = 'none';
                    }
                })
                .catch(error => {
                    document.getElementById('status').innerHTML = `<span class="error">Error al obtener la imagen: ${error}</span>`;
                });
        }
        
        // Actualizar al cargar la página
        actualizarImagen();
        
        // Actualizar cada minuto
        setInterval(actualizarImagen, 60000);
    </script>
</body>
</html>
            """)
    
    print(f"Servidor iniciado. Carpeta monitoreada: {CARPETA_IMAGENES}")
    print(f"La carpeta templates está en: {templates_dir}")
    print(f"El archivo index.html está en: {index_html_path}")
    print("Accede a http://localhost:5001 en tu navegador")
    
    # Iniciar el servidor
    app.run(debug=True, host='0.0.0.0', port=5001)