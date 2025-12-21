"""
Enunciado:
Desarrolla una aplicación web con Flask que demuestre diferentes formas de acceder a la
información enviada en las solicitudes HTTP. Esta aplicación te permitirá entender cómo
procesar diferentes tipos de datos proporcionados por los clientes.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /headers`: Devuelve los encabezados (headers) de la solicitud en formato JSON.
   - Muestra información como User-Agent, Accept-Language, etc.

2. `GET /browser`: Analiza el encabezado User-Agent y devuelve información sobre:
   - El navegador que está usando el cliente
   - El sistema operativo
   - Si es un dispositivo móvil o no

3. `POST /echo`: Acepta cualquier tipo de datos y devuelve exactamente los mismos datos
   en la misma forma que fueron enviados. Debe manejar:
   - JSON
   - Datos de formulario (form data)
   - Texto plano

4. `POST /validate-id`: Valida un documento de identidad según estas reglas:
   - Debe recibir un JSON con un campo "id_number"
   - El ID debe tener exactamente 9 caracteres
   - Los primeros 8 caracteres deben ser dígitos
   - El último carácter debe ser una letra
   - Devuelve JSON indicando si es válido o no

Esta actividad te enseñará cómo acceder y manipular datos de las solicitudes HTTP,
una habilidad fundamental para crear APIs robustas y aplicaciones web interactivas.
"""

from flask import Flask, jsonify, request, Response
import re

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/headers', methods=['GET'])
    def get_headers():
        """
        Devuelve los encabezados (headers) de la solicitud en formato JSON.
        Convierte el objeto headers de la solicitud en un diccionario.
        """
        # Implementa este endpoint:
        # 1. Accede a los encabezados de la solicitud usando request.headers
        # 2. Convierte los encabezados a un formato adecuado para JSON
        # 3. Devuelve los encabezados como respuesta JSON

        headers_dict = dict(request.headers)
        return jsonify(headers_dict),200



    @app.route('/browser', methods=['GET'])
    def get_browser_info():
        """
        Analiza el encabezado User-Agent y devuelve información sobre el navegador,
        sistema operativo y si es un dispositivo móvil.
        """
        # Implementa este endpoint:
        # 1. Obtén el encabezado User-Agent de request.headers
        # 2. Analiza la cadena para detectar:
        #    - El nombre del navegador (Chrome, Firefox, Safari, etc.)
        #    - El sistema operativo (Windows, macOS, Android, iOS, etc.)
        #    - Si es un dispositivo móvil (detecta cadenas como "Mobile", "Android", "iPhone")
        # 3. Devuelve la información como respuesta JSON
        ua = request.headers.get("User-Agent","")

        ua_lower = ua.lower()

        if "edg" in ua_lower:
            browser = "Edge"
        elif "chrome" in ua_lower and "safari" in ua_lower:
            browser = "Chrome"
        elif "firefox" in ua_lower:
            browser = "Firefox"
        elif "safari" in ua_lower and "chrome" not in ua_lower:
            browser = "Safari"
        else:
            browser = "Unknown"
            

        if "iphone" in ua_lower or "ipad" in ua_lower or "ios" in ua_lower:
            os_name = "iOS"
        elif "android" in ua_lower:
            os_name = "Android"
        elif "windows" in ua_lower:
            os_name = "Windows"
        elif "mac os x" in ua_lower or "macintosh" in ua_lower:
            os_name = "macOS"
        elif "linux" in ua_lower:
            os_name = "Linux"
        else:
            os_name = "Unknown"

        
        is_mobile = any(token in ua_lower for token in  ["mobile","android","iPhone","ipad"])

        return jsonify({
            "user_agent": ua,
            "browser": browser,
            "os": os_name,
            "is_mobile": is_mobile
        }),200


    @app.route('/echo', methods=['POST'])
    def echo():
        """
        Devuelve exactamente los mismos datos que recibe.
        Debe detectar el tipo de contenido y procesarlo adecuadamente.
        """
        # Implementa este endpoint:
        # 1. Detecta el tipo de contenido de la solicitud con request.content_type
        # 2. Según el tipo de contenido, extrae los datos:
        #    - Para JSON: usa request.get_json()
        #    - Para form data: usa request.form
        #    - Para texto plano: usa request.data
        # 3. Devuelve los mismos datos con el mismo tipo de contenido
        mimetype = request.mimetype or ""

        if mimetype == "application/json":
            data = request.get_json(silent=True)
            if data is None:
                return Response(request.get_data(),mimetype="application/json")
            return jsonify(data),200
        
        if mimetype in ("application/x-www-form-urlencoded", "multipart/form-data"):
            form_dict = request.form.to_dict(flat=True)
            return jsonify(form_dict),200
        
        raw = request.get_data()
        return Response(raw,mimetype=mimetype if mimetype else "text/plain"),200


    @app.route('/validate-id', methods=['POST'])
    def validate_id():
        """
        Valida un documento de identidad según reglas específicas:
        - Debe tener exactamente 9 caracteres
        - Los primeros 8 caracteres deben ser dígitos
        - El último carácter debe ser una letra
        """
        # Implementa este endpoint:
        # 1. Obtén el campo "id_number" del JSON enviado
        # 2. Valida que cumpla con las reglas especificadas
        # 3. Devuelve un JSON con el resultado de la validación
        data = request.get_json(silent=True)
        if not isinstance(data,dict) or "id_number" not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Falta el campo 'id_number' en el JSON",
                "valid": False
            }),400
        id_number = str(data.get("id_number",""))

        pattern = r"^\d{8}[A-Za-z]$"
        is_valid = re.fullmatch(pattern,id_number) is not None

        return jsonify({
            "id_number": id_number,
            "valid": is_valid
        }),200
        

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
