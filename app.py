import requests
import base64
import re
from flask import Flask, Response, redirect, request

app = Flask(__name__)

# URL de tu GitHub de junio en Base64
URL_CIFRADA = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9tYWluL2p1bmlvMjAyNi5tM3U="

# Diccionario temporal en memoria para guardar los enlaces reales ocultos
MEMORIA_CANALES = {}

def procesar_y_ocultar_lista():
    """Descarga la lista original y enmascara los links reales"""
    try:
        url_real = base64.b64decode(URL_CIFRADA.encode('utf-8')).decode('utf-8')
        response = requests.get(url_real, headers={'User-Agent': 'Mozilla/5.0'})
        lineas = response.text.splitlines()
        
        nueva_lista = []
        contador = 1
        
        for linea in lineas:
            # Si la línea es un enlace (http...), lo guardamos en memoria y ponemos nuestro link falso
            if linea.strip().startswith("http"):
                enlace_real = linea.strip()
                MEMORIA_CANALES[str(contador)] = enlace_real
                
                # Construimos el enlace enmascarado apuntando a tu Render
                host = request.host_url.rstrip('/')
                nueva_lista.append(f"{host}/reproducir?id={contador}")
                contador += 1
            else:
                # Si es texto normal (#EXTINF...), lo dejamos igual
                nueva_lista.append(linea)
                
        return "\n".join(nueva_lista)
    except Exception as e:
        return f"Error al procesar: {e}"

@app.route('/lista.m3u')
def obtener_lista():
    # Entrega la lista con los enlaces ya ocultos (Cualquiera puede entrar y no verá los links originales)
    contenido_oculto = procesar_y_ocultar_lista()
    return Response(contenido_oculto, mimetype='text/plain')

@app.route('/reproducir')
def reproducir_canal():
    # Cuando la tele le da play al link falso, Render busca el verdadero en secreto y redirige el video
    id_canal = request.args.get('id')
    enlace_real = MEMORIA_CANALES.get(id_canal)
    
    if enlace_real:
        return redirect(enlace_real, code=302)
    return "Canal no encontrado", 404

if __name__ == "__main__":
    app.run()
