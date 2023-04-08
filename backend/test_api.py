from fastapi.testclient import TestClient
from unittest.mock import patch
import api

client = TestClient(api.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


@patch.object(api, "get_hiscores")
def test_get_hiscores(get_hiscores):
    get_hiscores.return_value = mock_hiscores
    response = client.get("/api/hiscores")
    assert response.status_code == 200
    assert response.json() == mock_hiscores
    get_hiscores.assert_called_once()


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
