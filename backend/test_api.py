from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from database import crud
import api
import pytest


client = TestClient(api.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_hiscores_by_players(monkeypatch):
    @pytest.mark.asyncio
    async def mock_get_players(payload):
        return mock_players

    monkeypatch.setattr(crud, "get_players", mock_get_players)

    @pytest.mark.asyncio
    async def mock_get_hiscores_by_player_id(payload, player_id):
        if player_id == 1:
            return mock_hiscores_for_elaine
        if player_id == 2:
            return mock_hiscores_for_guybrush
        if player_id == 3:
            return mock_hiscores_for_lechuck

    monkeypatch.setattr(crud, "get_hiscores_by_player_id",
                        mock_get_hiscores_by_player_id)

    response = client.get("/api/hiscores_by_players")
    assert response.status_code == 200
    # response list should be sorted correctly
    assert response.json()[
        0]['player']['name'] == mock_hiscores_by_players[0]['player']['name']
    assert response.json()[
        1]['player']['name'] == mock_hiscores_by_players[1]['player']['name']
    assert response.json()[
        2]['player']['name'] == mock_hiscores_by_players[2]['player']['name']


mock_players = [
    {
        "created_at": datetime.now(),
        "id": 3,
        "name": "LeChuck",
        "original_exp": 0
    },
    {
        "created_at": datetime.now(),
        "id": 1,
        "name": "Elaine",
        "original_exp": 1337
    },
    {
        "created_at": datetime.now(),
        "id": 2,
        "name": "Guybrush",
        "original_exp": 0
    }
]


mock_hiscores_for_elaine = [
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
]

mock_hiscores_for_guybrush = [
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
]

mock_hiscores_for_lechuck = [
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
]

mock_hiscores_by_players = [
    {

        "player": {
            "created_at": datetime.now(),
            "id": 1,
            "name": "Elaine",
            "original_exp": 1337
        },
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
        ]
    },
    {
        "player": {
            "created_at": datetime.now(),
            "id": 2,
            "name": "Guybrush",
            "original_exp": 0
        },
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
        ]
    },
    {
        "player": {
            "created_at": datetime.now(),
            "id": 3,
            "name": "LeChuck",
            "original_exp": 0
        },
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
        ]
    },
]
