import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # Import FastAPI app

client = TestClient(app)

@pytest.fixture
def mock_db():
    with patch("sqlite3.connect") as mock_connect:
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        yield mock_cursor

def test_transform(mock_db):
    response = client.post("/object/transform", json={"name":"Cube","position": [1, 2, 3], "rotation": [0, 0, 0], "scale": [1, 1, 1]})
    assert response.status_code == 200

def test_translation():
    response = client.post("/object/translation", json={"data": [5, 10, 15],"name":"Cube"})
    assert response.status_code == 200

def test_rotation():
    response = client.post("/object/rotation", json={"data": [5, 10, 15],"name":"Cube"})
    assert response.status_code == 200

def test_scale():
    response = client.post("/object/scale", json={"data": [5, 10, 15],"name":"Cube"})
    assert response.status_code == 200

def test_file_path():
    response = client.get("/object/file-path")
    assert response.status_code == 200
    assert "FilePath" in response.json()

def test_file_path_project():
    response = client.get("/object/file-path?projectpath=true")
    assert response.status_code == 200
    assert "FilePath" in response.json()

def test_add_item(mock_db):
    response = client.post("/object/add-item", json={"name": "Cube", "qty": 10})
    assert response.status_code == 200



def test_update_quantity(mock_db):
    response = client.put("/object/update-quantity", json={"name": "Cube", "new_qty": 20})
    assert response.status_code == 200

