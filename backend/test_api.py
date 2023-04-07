from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_get_hiscores():
    response = client.get("/api/hiscores")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

mock_hiscores = [
    {
        'playerName': 'Purilainen',
        'oldExp': 100.0,
        'newExp': 200.0,
        'gainedExp': 100.0
    },
    {
        'playerName': 'LeChuck',
        'oldExp': 200.0,
        'newExp': 250.0,
        'gainedExp': 50.0
    },
    {
        'playerName': 'Lord Jolt',
        'oldExp': 50.0,
        'newExp': 300.0,
        'gainedExp': 250.0
    }
]