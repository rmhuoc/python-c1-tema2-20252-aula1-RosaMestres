from flask import Flask

# Crea una instancia de la aplicación.
app = Flask(__name__)

# Este decorador asocia la URL raíz ('/') con la función hello_world().
@app.route('/')
def hello_world():
    # La función devuelve el texto que se mostrará en el navegador.
    return '¡Hola, desde Flask!'

# Inicia el servidor si el script se ejecuta directamente.
if __name__ == '__main__':
    app.run(debug=True)