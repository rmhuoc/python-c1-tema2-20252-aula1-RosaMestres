"""
Enunciado:
Desarrolla una aplicación web con Flask que explore los diferentes tipos MIME (Multipurpose Internet Mail Extensions)
y cómo enviar diversos formatos de contenido en respuestas HTTP. Esta aplicación te permitirá entender
cómo configurar correctamente los encabezados Content-Type para diferentes tipos de datos.

Los tipos MIME son fundamentales en el desarrollo web ya que indican al cliente (navegador, aplicación, etc.)
cómo interpretar y mostrar los datos enviados por el servidor. Una API bien diseñada debe utilizar
los tipos MIME apropiados para cada tipo de contenido.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /text`: Devuelve un texto plano con el tipo MIME `text/plain`.
   - Ejemplo de uso: Enviar mensajes simples o logs sin formato.

2. `GET /html`: Devuelve un fragmento HTML con el tipo MIME `text/html`.
   - Ejemplo de uso: Enviar contenido que debe ser renderizado como una página web.

3. `GET /json`: Devuelve un objeto JSON con el tipo MIME `application/json`.
   - Ejemplo de uso: Intercambio de datos estructurados entre cliente y servidor en APIs RESTful.

4. `GET /xml`: Devuelve un documento XML con el tipo MIME `application/xml`.
   - Ejemplo de uso: APIs SOAP, configuraciones o intercambio de datos estructurados en formato XML.

5. `GET /image`: Devuelve una imagen con el tipo MIME `image/png`.
   - Ejemplo de uso: Servir imágenes directamente desde la API.

6. `GET /binary`: Devuelve datos binarios con el tipo MIME `application/octet-stream`.
   - Ejemplo de uso: Descargar archivos como PDFs, archivos comprimidos o cualquier contenido binario genérico.

Tu tarea es completar la implementación de la función create_app() y de los endpoints solicitados,
asegurándote de utilizar el tipo MIME correcto en cada caso y generar el contenido adecuado.

Esta actividad te enseñará cómo configurar correctamente los tipos de contenido en respuestas HTTP,
una habilidad esencial para el desarrollo de APIs y servicios web que manejan diferentes formatos de datos.
"""

from flask import Flask, jsonify, Response, send_file, make_response
import os
import io
import base64

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/text', methods=['GET'])
    def get_text():
        """
        Devuelve un texto plano con el tipo MIME `text/plain`
        """
        # Implementa este endpoint para devolver el contenido solicitado
        resp = Response("Este es un texto plano")
        resp.headers["Content-Type"] = "text/plain"
        return resp

    @app.route('/html', methods=['GET'])
    def get_html():
        """
        Devuelve un fragmento HTML con el tipo MIME `text/html`
        """
        # Implementa este endpoint para devolver el contenido solicitado
        resp = Response("<h1>Este es un fragmento HTML</h1>")
        resp.headers["Content-Type"] = "text/html"
        return resp

    @app.route('/json', methods=['GET'])
    def get_json():
        """
        Devuelve un objeto JSON con el tipo MIME `application/json`
        """
        # Implementa este endpoint para devolver el contenido solicitado
        return jsonify({"mensaje": "Este es un objeto JSON"})

    @app.route('/xml', methods=['GET'])
    def get_xml():
        """
        Devuelve un documento XML con el tipo MIME `application/xml`
        """
        # Implementa este endpoint para devolver el contenido solicitado
        resp = Response ("<mensaje>Este es un documento XML</mensaje>")
        resp.headers["Content-Type"] = "application/xml"
        return resp

    @app.route('/image', methods=['GET'])
    def get_image():
        """
        Devuelve una imagen con el tipo MIME `image/png`
        """
        # Implementa este endpoint para devolver el contenido solicitado
        # Sugerencia: Puedes usar send_file para enviar una imagen
        png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
            "ASsJTYQAAAAASUVORK5CYII="
        )
        png_bytes = base64.b64decode(png_b64)
        img_io = io.BytesIO(png_bytes)
        img_io.seek(0)
        return send_file(
            img_io,
            mimetype="image/png",
            as_attachment=False,
            download_name="pixel.png"
        )

    @app.route('/binary', methods=['GET'])
    def get_binary():
        """
        Devuelve datos binarios genéricos con el tipo MIME `application/octet-stream`
        Para este ejemplo, puedes crear unos bytes aleatorios o un archivo binario simple
        """
        # Implementa este endpoint para devolver el contenido solicitado
        # Sugerencia: Puedes usar os.urandom() para generar datos aleatorios
        data = os.urandom(64)
        resp = make_response(data)
        resp.headers["Content-Type"] = "application/octet-stream"
        resp.headers["Content-Disposition"] = 'attachment; filename="random.bin"'
        return resp

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
