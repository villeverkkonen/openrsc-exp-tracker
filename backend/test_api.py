from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from database import crud
from database import models
import api
import asyncio
import pytest


# @pytest.fixture
# def app():
#     import api
#     return api


# @pytest.fixture
# def client(app):
#     return TestClient(app)


client = TestClient(api.app)


# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_hiscores_by_players(monkeypatch):
    @pytest.mark.asyncio
    async def mock_get_players(payload):
        return mock_players

    monkeypatch.setattr(crud, "get_players", mock_get_players)

    @pytest.mark.asyncio
    async def mock_get_hiscores_by_player_id(payload):
        return mock_hiscores_by_player_id

    monkeypatch.setattr(crud, "get_hiscores_by_player_id",
                        mock_get_hiscores_by_player_id)
    # mock_func = MagicMock(return_value=mock_hiscores_by_players)
    # mocker.patch("api.get_hiscores_by_players", new=mock_func)
    response = await client.get("/api/hiscores_by_players")
    assert response.status_code == 200
    assert response.json() == mock_hiscores_by_players
    # m.assert_called_once()


# @pytest.object(api, "get_hiscores_by_players")
# def test_get_hiscores_by_players(get_hiscores_by_players):
#     get_hiscores_by_players.return_value = mock_hiscores_by_players
#     response = client.get("/api/hiscores_by_players")
#     assert response.status_code == 200
#     assert response.json() == mock_hiscores_by_players
#     get_hiscores_by_players.assert_called_once()


mock_players = [
    models.Player(
        id=2,
        created_at=datetime.now(),
        name="Guybrush",
        original_exp=0
    )
]


lol = [
    {
        "player": {
            "created_at": datetime.now(),
            "id": 2,
            "name": "Guybrush",
            "original_exp": 0
        }
    },
    # {
    #     "player": {
    #         "created_at": datetime.now(),
    #         "id": 1,
    #         "name": "Elaine",
    #         "original_exp": 1337
    #     }
    # },
    # {
    #     "player": {
    #         "created_at": datetime.now(),
    #         "id": 3,
    #         "name": "LeChuck",
    #         "original_exp": 0
    #     }
    # }
]


mock_hiscores_by_players = [
    # {

    #     "player": {
    #         "created_at": datetime.now(),
    #         "id": 1,
    #         "name": "Elaine",
    #         "original_exp": 1337
    #     },
    #     "hiscores":
    #         [
    #             {
    #                 "id": 1,
    #                 "new_exp": 2337,
    #                 "total_gained_exp": 1000,
    #                 "created_at": datetime.now(),
    #                 "player_id": 1
    #             },
    #             {
    #                 "id": 4,
    #                 "new_exp": 3337,
    #                 "total_gained_exp": 2000,
    #                 "created_at": datetime.now() + timedelta(days=1),
    #                 "player_id": 1
    #             }
    #          ]
    # },
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
    # {

    #     "player": {
    #         "created_at": datetime.now(),
    #         "id": 3,
    #         "name": "LeChuck",
    #         "original_exp": 0
    #     },
    #     "hiscores":
    #         [
    #             {
    #                 "id": 3,
    #                 "new_exp": 0,
    #                 "total_gained_exp": 0,
    #                 "created_at": datetime.now(),
    #                 "player_id": 3
    #             },
    #             {
    #                 "id": 6,
    #                 "new_exp": 0,
    #                 "total_gained_exp": 0,
    #                 "created_at": datetime.now() + timedelta(days=1),
    #                 "player_id": 3
    #             }
    #           ]
    # },
]

mock_hiscores_by_player_id = [
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
]
