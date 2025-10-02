import pytest
from flask.testing import FlaskClient
from ej2d2 import create_app

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_resource_valid_id(client):
    """
    Prueba el endpoint /resource/<id> con un ID válido (positivo y ≤ 100)
    Debe devolver un código 200 y alguna información sobre el recurso
    """
    response = client.get("/resource/42")
    assert response.status_code == 200, "El código de estado debe ser 200 para un ID válido"
    assert "42" in response.get_data(as_text=True), "La respuesta debe incluir el ID solicitado"

def test_resource_negative_id(client):
    """
    Prueba el endpoint /resource/<id> con un ID negativo
    Debe abortar con código 400 (Bad Request)
    """
    response = client.get("/resource/-5")
    assert response.status_code == 400, "El código de estado debe ser 400 para un ID negativo"

def test_resource_zero_id(client):
    """
    Prueba el endpoint /resource/<id> con ID = 0
    Debe abortar con código 400 (Bad Request)
    """
    response = client.get("/resource/0")
    assert response.status_code == 400, "El código de estado debe ser 400 para ID = 0"

def test_resource_large_id(client):
    """
    Prueba el endpoint /resource/<id> con un ID > 100
    Debe abortar con código 404 (Not Found)
    """
    response = client.get("/resource/101")
    assert response.status_code == 404, "El código de estado debe ser 404 para un ID > 100"

def test_admin_no_key(client):
    """
    Prueba el endpoint /admin sin proporcionar una clave
    Debe abortar con código 401 (Unauthorized)
    """
    response = client.get("/admin")
    assert response.status_code == 401, "El código de estado debe ser 401 cuando no se proporciona la clave"

def test_admin_wrong_key(client):
    """
    Prueba el endpoint /admin con una clave incorrecta
    Debe abortar con código 403 (Forbidden)
    """
    response = client.get("/admin?key=wrong")
    assert response.status_code == 403, "El código de estado debe ser 403 cuando la clave es incorrecta"

def test_admin_correct_key(client):
    """
    Prueba el endpoint /admin con la clave correcta
    Debe devolver un código 200
    """
    response = client.get("/admin?key=secret123")
    assert response.status_code == 200, "El código de estado debe ser 200 cuando la clave es correcta"
