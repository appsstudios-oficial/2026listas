@app.route('/lista.m3u')
def proteger_lista():
    # Eliminamos el bloqueo temporalmente para probar
    try:
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error al obtener la lista de origen", 500
            
        return Response(respuesta.text, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return "Error interno del servidor", 500
