import os
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# Tu lista real de GitHub (la que tiene los canales reales)
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/2026listas/refs/heads/main/full.m3u"

@app.route('/lista.m3u')
def proteger_lista():
    # Obtenemos la identificación de quién está pidiendo la lista
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Lista de palabras clave que envían TODOS los navegadores web del mundo
    palabras_navegadores = [
        'mozilla', 'chrome', 'safari', 'applewebkit', 
        'opera', 'edge', 'windows', 'android', 'iphone'
    ]
    
    # Si la petición viene sin identificación, o contiene alguna palabra de navegador: BLOQUEO
    if not user_agent or any(nav in user_agent for nav in palabras_navegadores):
        # Los mandamos a tu página web contador
        return redirect("https://appsstudios-oficial.github.io/tu-pagina-contador", code=302)

    # Si NO es un navegador (es decir, es SSIPTV, VLC, IPTV Smarters, etc.), le entregamos la lista original
    try:
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error al obtener la lista de origen", 500
            
        # Entregamos el archivo original exactamente como está en GitHub
        return Response(respuesta.text, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return "Error interno del servidor", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
