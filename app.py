import os
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# Tu lista real de GitHub (la que tiene los canales reales)
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/2026listas/refs/heads/main/full.m3u"

@app.route('/lista.m3u')
def proteger_lista():
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
