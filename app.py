import os
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# Tu lista real de GitHub (la que tiene los canales reales)
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/2026listas/refs/heads/main/full.m3u"

@app.route('/lista.m3u')
def proteger_lista():
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Si la petición no tiene identificación, la bloqueamos por seguridad
    if not user_agent:
        return redirect("https://appsstudios-oficial.github.io/tu-pagina-contador", code=302)

    # Bloqueamos estrictamente las firmas que usan los navegadores de PC y Celulares
    # Esto no afecta a los servidores de SSIPTV ni a reproductores puros
    bloqueo_navegadores = [
        'chrome/', 'firefox/', 'safari/', 'edge/', 'opera/', 'edg/',
        'window snt', 'macintosh', 'linux x86_64'
    ]
    
    # Si detectamos que es un usuario en un navegador web, lo mandamos al contador
    if any(nav in user_agent for nav in bloqueo_navegadores):
        return redirect("https://appsstudios-oficial.github.io/tu-pagina-contador", code=302)

    # Si pasa el filtro (SSIPTV, VLC, etc.), le entregamos la lista limpia
    try:
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error al obtener la lista de origen", 500
            
        return Response(respuesta.text, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return "Error interno del servidor", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
