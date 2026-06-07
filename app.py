import requests
import base64
from flask import Flask, Response, request

app = Flask(__name__)

URL_CIFRADA = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9tYWluL2p1bmlvMjAyNi5tM3U="
CLAVE_ACCESO = "MiTele2026"

@app.route('/lista.m3u')
def obtener_lista():
    # 1. Validar clave secreta
    clave_recibida = request.args.get('clave')
    if clave_recibida != CLAVE_ACCESO:
        return "No encontrado", 404

    # 2. Leer la firma de la aplicación
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Lista de apps e intermediarios de TV permitidos (Sumamos ss-iptv y los servidores que usa)
    permitidos = [
        'vlc', 'iptv', 'smarters', 'xciptv', 'ott', 'player', 
        'smarttv', 'tivi', 'mxplayer', 'core', 'lavf', 'http-client',
        'ss-iptv', 'ssiptv', 'webkit', 'url', 'fetch', 'go-http-client'
    ]
    
    navegadores_web = ['chrome', 'edge', 'firefox', 'opera']

    # Si es una de las apps permitidas (incluyendo los motores de SS IPTV), pasa directo
    es_reproductor = any(rep in user_agent for rep in permitidos)
    
    # Bloqueo estricto solo si es un navegador de PC real y no está en los permitidos
    es_navegador_puro = any(nav in user_agent for nav in navegadores_web) and not es_reproductor

    if es_navegador_puro:
        return "<h1>404 Not Found</h1>The server can not find the requested page.", 404

    try:
        url_real = base64.b64decode(URL_CIFRADA.encode('utf-8')).decode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_real, headers=headers)
        
        return Response(response.text, mimetype='text/plain')
    except Exception as e:
        return "Error interno", 500

if __name__ == "__main__":
    app.run()
