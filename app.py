import os
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# Enlace RAW de tu lista en el repositorio
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/2026listas/refs/heads/main/full.m3u"

# Diccionario interno en memoria para guardar las URLs reales temporalmente
ENLACES_OCULTOS = {}

@app.route('/lista.m3u')
def obtener_lista_ofuscada():
    global ENLACES_OCULTOS
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # BLOQUEO ESTRICTO: Solo los navegadores solicitados
    navegadores_web = ['chrome', 'firefox', 'safari', 'brave', 'opera']
    if any(nav in user_agent for nav in navegadores_web):
        return redirect("https://appsstudios-oficial.github.io/tu-pagina-contador", code=302)

    try:
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error al descargar la lista", 500
        
        lineas = respuesta.text.splitlines()
        lista_final = []
        contador_id = 1
        nuevos_enlaces = {}
        
        # Obtenemos el dominio actual de Render dinámicamente
        host_actual = request.host_url.rstrip('/')
        
        for linea in lineas:
            linea_limpia = linea.strip()
            
            if linea_limpia.startswith("http://") or linea_limpia.startswith("https://"):
                # Guardamos el enlace real asociado a un número de ID
                nuevos_enlaces[str(contador_id)] = linea_limpia
                
                # Reemplazamos por completo el enlace original por la ruta protegida de Render
                lista_final.append(f"{host_actual}/video/{contador_id}")
                contador_id += 1
            else:
                lista_final.append(linea)
                
        # Actualizamos la base de datos temporal en memoria
        ENLACES_OCULTOS = nuevos_enlaces
        
        contenido_m3u = "\n".join(lista_final)
        return Response(contenido_m3u, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return "Error interno", 500

@app.route('/video/<id_video>')
def redireccionar_video(id_video):
    # Cuando la app de IPTV pide un canal, buscamos secretamente el enlace real
    url_real = ENLACES_OCULTOS.get(str(id_video))
    
    if url_real:
        # Redireccionamos al flujo original de manera transparente
        return redirect(url_real, code=302)
    else:
        return "Canal no encontrado o lista desactualizada", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
