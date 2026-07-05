import os
import re
from urllib.parse import urlparse
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# Enlace RAW de tu lista en el nuevo repositorio
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/2026listas/refs/heads/main/full.m3u"

def ip_a_decimal(ip):
    """Transforma una IP como 181.224.255.210 en un número entero gigante"""
    try:
        octetos = list(map(int, ip.split('.')))
        return (octetos[0] << 24) + (octetos[1] << 16) + (octetos[2] << 8) + octetos[3]
    except:
        return None

def ofuscar_url(url):
    """Busca si el enlace usa IP y la transforma para ofuscarla"""
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        
        if host and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
            ip_decimal = ip_a_decimal(host)
            if ip_decimal:
                nuevo_netloc = f"{ip_decimal}"
                if parsed.port:
                    nuevo_netloc += f":{parsed.port}"
                nuevo_url = parsed._replace(netloc=nuevo_netloc).geturl()
                return nuevo_url
        return url
    except:
        return url

@app.route('/lista.m3u')
def obtener_lista_ofuscada():
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # BLOQUEO ESTRICTO: Solo los navegadores solicitados
    navegadores_web = ['chrome', 'firefox', 'safari', 'brave', 'opera']
    
    # Si el User-Agent contiene alguna de estas palabras, se lo redirige
    if any(nav in user_agent for nav in navegadores_web):
        return redirect("https://appsstudios-oficial.github.io/tu-pagina-contador", code=302)

    try:
        # Para cualquier otra aplicación (apps de IPTV, VLC, etc.), la lista pasa limpio
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error", 500
        
        lineas = respuesta.text.splitlines()
        lista_final = []
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if linea_limpia.startswith("http://") or linea_limpia.startswith("https://"):
                linea_ofuscada = ofuscar_url(linea_limpia)
                lista_final.append(linea_ofuscada)
            else:
                lista_final.append(linea)
                
        contenido_m3u = "\n".join(lista_final)
        return Response(contenido_m3u, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return "Error interno", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
