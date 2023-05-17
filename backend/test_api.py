from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime, timedelta
import api

client = TestClient(api.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


@patch.object(api, "get_hiscores")
def test_get_hiscores_by_players(get_hiscores_by_players):
    get_hiscores_by_players.return_value = mock_hiscores_by_players
    response = client.get("/api/hiscores")
    assert response.status_code == 200
    assert response.json() == mock_hiscores_by_players
    get_hiscores_by_players.assert_called_once()


mock_hiscores_by_players = [
    {
        "hiscores":
            [
                {
                    "id": 1,
                    "new_exp": 2337,
                    "total_gained_exp": 1000,
                    "created_at": datetime.now(),
                    "player_id": 1
                },
                {
                    "id": 4,
                    "new_exp": 3337,
                    "total_gained_exp": 2000,
                    "created_at": datetime.now() + timedelta(days=1),
                    "player_id": 1
                }
            ],
        "player": {
            "created_at": datetime.now(),
            "id": 1,
            "name": "Elaine",
            "original_exp": 1337
        }
    },
    {
        "hiscores":
            [
                {
                    "id": 2,
                    "new_exp": 50,
                    "total_gained_exp": 50,
                    "created_at": datetime.now(),
                    "player_id": 2
                },
                {
                    "id": 5,
                    "new_exp": 350,
                    "total_gained_exp": 350,
                    "created_at": datetime.now() + timedelta(days=1),
                    "player_id": 2
                }
            ],
        "player": {
            "created_at": datetime.now(),
            "id": 2,
            "name": "Guybrush",
            "original_exp": 0
        }
    },
    {
        "hiscores":
            [
                {
                    "id": 3,
                    "new_exp": 0,
                    "total_gained_exp": 0,
                    "created_at": datetime.now(),
                    "player_id": 3
                },
                {
                    "id": 6,
                    "new_exp": 0,
                    "total_gained_exp": 0,
                    "created_at": datetime.now() + timedelta(days=1),
                    "player_id": 3
                }
            ],
        "player": {
            "created_at": datetime.now(),
            "id": 3,
            "name": "LeChuck",
            "original_exp": 0
        }
    },
]
