import os
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# Enlace RAW de tu lista en el repositorio
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/2026listas/refs/heads/main/full.m3u"

@app.route('/lista.m3u')
def obtener_lista_protegida():
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Tu bloqueo original para navegadores web
    navegadores_web = ['chrome', 'firefox', 'safari', 'brave', 'opera']
    if any(nav in user_agent for nav in navegadores_web):
        return redirect("https://appsstudios-oficial.github.io/tu-pagina-contador", code=302)

    try:
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error al descargar la lista", 500
        
        # Entregamos el archivo M3U original, con sus enlaces reales intactos
        return Response(respuesta.text, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return "Error interno", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
