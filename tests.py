import requests

BASE_URL = "http://127.0.0.1:5000"

def test_agregar_usuario():
    """Prueba agregar un usuario con acento y verificar que se guarda correctamente"""
    response = requests.post(f"{BASE_URL}/usuarios", json={"nombre": "María", "edad": 25, "email": "maria@example.com"})
    assert response.status_code == 201
    assert response.json()["mensaje"] == "Usuario agregado"

def test_obtener_usuario_variaciones():
    """Prueba obtener un usuario con diferentes variaciones de acentos y mayúsculas"""
    for nombre in ["María", "Maria", "maria", "MARÍA", "MARIA"]:
        response = requests.get(f"{BASE_URL}/usuarios/{nombre}")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre_original"] == "María"
        assert data["edad"] == 25
        assert data["email"] == "maria@example.com"

def test_no_duplicar_usuario():
    """Prueba que no se permita agregar el mismo usuario dos veces"""
    response = requests.post(f"{BASE_URL}/usuarios", json={"nombre": "María", "edad": 25, "email": "maria@example.com"})
    assert response.status_code == 400
    assert response.json()["error"] == "Usuario ya existe"

def test_eliminar_usuario():
    """Prueba eliminar el usuario y verificar que ya no existe"""
    response = requests.delete(f"{BASE_URL}/usuarios/Maria")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Usuario eliminado"

    # Verificar que ya no existe
    response = requests.get(f"{BASE_URL}/usuarios/Maria")
    assert response.status_code == 404
    assert response.json()["error"] == "Usuario no encontrado"

def test_eliminar_usuario_inexistente():
    """Prueba eliminar un usuario que no existe"""
    response = requests.delete(f"{BASE_URL}/usuarios/UsuarioQueNoExiste")
    assert response.status_code == 404
    assert response.json()["error"] == "Usuario no encontrado"

def test_obtener_usuario_inexistente():
    """Prueba obtener un usuario que no existe"""
    response = requests.get(f"{BASE_URL}/usuarios/UsuarioQueNoExiste")
    assert response.status_code == 404
    assert response.json()["error"] == "Usuario no encontrado"
