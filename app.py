import requests
import base64
from flask import Flask, Response, redirect, request

app = Flask(__name__)

URL_CIFRADA = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9tYWluL2p1bmlvMjAyNi5tM3U="
MEMORIA_CANALES = {}

def procesar_y_ocultar_lista():
    try:
        url_real = base64.b64decode(URL_CIFRADA.encode('utf-8')).decode('utf-8')
        response = requests.get(url_real, headers={'User-Agent': 'Mozilla/5.0'})
        lineas = response.text.splitlines()
        
        nueva_lista = []
        contador = 1
        
        for linea in lineas:
            if linea.strip().startswith("http"):
                enlace_real = linea.strip()
                MEMORIA_CANALES[str(contador)] = enlace_real
                host = request.host_url.rstrip('/')
                # Le dejamos los links limpios a la tele
                nueva_lista.append(f"{host}/reproducir?id={contador}")
                contador += 1
            else:
                nueva_lista.append(linea)
                
        return "\n".join(nueva_lista)
    except Exception as e:
        return f"Error: {e}"

@app.route('/lista.m3u')
def obtener_lista():
    return Response(procesar_y_ocultar_lista(), mimetype='text/plain')

@app.route('/reproducir')
def reproducir_canal():
    # FILTRO ANTI-CHUSMAS: Revisamos quién le dio al botón de Play
    user_agent = request.headers.get('User-Agent', '').lower()
    navegadores_web = ['chrome', 'edge', 'firefox', 'opera', 'safari']
    
    # Si intentan reproducir el link suelto desde un navegador web común, se lo bloqueamos
    if any(nav in user_agent for nav in navegadores_web):
        return "<h1>Acceso Denegado</h1>No podés reproducir enlaces sueltos desde el navegador.", 403

    id_canal = request.args.get('id')
    enlace_real = MEMORIA_CANALES.get(id_canal)
    
    if enlace_real:
        return redirect(enlace_real, code=302)
    return "Canal no encontrado", 404

if __name__ == "__main__":
    app.run()
