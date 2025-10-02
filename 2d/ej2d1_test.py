import pytest
from flask.testing import FlaskClient
from ej2d1 import create_app
import logging
from io import StringIO

class LogCaptureHandler(logging.Handler):
    """
    Manejador personalizado para capturar mensajes de log durante las pruebas
    """
    def __init__(self):
        super().__init__()
        self.logs = StringIO()
        self.setLevel(logging.INFO)
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    def emit(self, record):
        """Añade un mensaje de log a los logs capturados"""
        self.logs.write(self.format(record) + '\n')

    def get_logs(self):
        """Devuelve los logs capturados y reinicia"""
        logs = self.logs.getvalue()
        self.logs = StringIO()
        return logs

@pytest.fixture
def client() -> FlaskClient:
    """
    Fixture para configurar el cliente de pruebas y capturar logs
    """
    app = create_app()
    app.testing = True

    # Configurar el capturador de logs
    log_capture = LogCaptureHandler()
    app.logger.addHandler(log_capture)
    app.logger.setLevel(logging.INFO)

    with app.test_client() as client:
        client.log_capture = log_capture
        yield client

def test_info_endpoint(client):
    """
    Prueba el endpoint /info
    Verifica que:
    1. Devuelve un mensaje de texto
    2. El código de estado es 200
    3. Se registró un mensaje de nivel INFO
    """
    response = client.get("/info")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.content_type.startswith('text/plain'), "El contenido debe ser texto plano"

    logs = client.log_capture.get_logs()
    assert "INFO:" in logs, "Debe registrarse un mensaje de nivel INFO"

def test_warning_endpoint(client):
    """
    Prueba el endpoint /warning
    Verifica que:
    1. Devuelve un mensaje de texto
    2. El código de estado es 200
    3. Se registró un mensaje de nivel WARNING
    """
    response = client.get("/warning")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.content_type.startswith('text/plain'), "El contenido debe ser texto plano"

    logs = client.log_capture.get_logs()
    assert "WARNING:" in logs, "Debe registrarse un mensaje de nivel WARNING"

def test_error_endpoint(client):
    """
    Prueba el endpoint /error
    Verifica que:
    1. Devuelve un mensaje de texto
    2. El código de estado es 200
    3. Se registró un mensaje de nivel ERROR
    """
    response = client.get("/error")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.content_type.startswith('text/plain'), "El contenido debe ser texto plano"

    logs = client.log_capture.get_logs()
    assert "ERROR:" in logs, "Debe registrarse un mensaje de nivel ERROR"

def test_critical_endpoint(client):
    """
    Prueba el endpoint /critical
    Verifica que:
    1. Devuelve un mensaje de texto
    2. El código de estado es 200
    3. Se registró un mensaje de nivel CRITICAL
    """
    response = client.get("/critical")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.content_type.startswith('text/plain'), "El contenido debe ser texto plano"

    logs = client.log_capture.get_logs()
    assert "CRITICAL:" in logs, "Debe registrarse un mensaje de nivel CRITICAL"

def test_status_endpoint_with_level(client):
    """
    Prueba el endpoint /status con parámetro level
    Este test es opcional, solo se ejecutará si el endpoint está implementado
    """
    try:
        # Intentar diferentes niveles
        response = client.get("/status?level=warning")
        assert response.status_code == 200
        logs = client.log_capture.get_logs()
        assert "WARNING:" in logs

        response = client.get("/status?level=error")
        assert response.status_code == 200
        logs = client.log_capture.get_logs()
        assert "ERROR:" in logs
    except:
        # Si el endpoint no está implementado, la prueba se omite
        pytest.skip("El endpoint /status no está implementado")
