from app import app

def test_home():
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json["status"] == "running"

def test_health_check():
    cliente = app.test_client()
    for _ in range(5):
        respuesta = cliente.get("/health")
        assert respuesta.status_code == 200

def test_buscar_rechaza_id_no_numerico():
    cliente = app.test_client()
    respuesta = cliente.get("/buscar?id=1%20OR%201=1")
    assert respuesta.status_code == 400
