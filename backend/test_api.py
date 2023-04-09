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
        'playerName': 'Lord Jolt',
        'oldExp': 50,
        'newExp': 300,
        'gainedExp': 250
    },
    {
        'playerName': 'Purilainen',
        'oldExp': 100,
        'newExp': 200,
        'gainedExp': 100
    },
    {
        'playerName': 'LeChuck',
        'oldExp': 200,
        'newExp': 250,
        'gainedExp': 50
    }
]
