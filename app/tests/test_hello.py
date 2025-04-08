from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello():
    response = client.get('/v1/')
    assert response.status_code == 200
    assert len(response.json()) > 0