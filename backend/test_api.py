from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from database import crud, models
import api
import pytest


client = TestClient(api.app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_players(monkeypatch):
    def mock_get_players(payload):
        return mock_players

    monkeypatch.setattr(crud, 'get_players', mock_get_players)

    response = client.get('/api/players')
    players = response.json()

    assert response.status_code == 200
    assert len(players) == len(mock_players)
    assert players[0]['name'] == mock_players[0].name
    assert players[1]['name'] == mock_players[1].name
    assert players[2]['name'] == mock_players[2].name


@pytest.mark.asyncio
async def test_create_player(monkeypatch):
    datetime_now = datetime.now()

    def mock_get_player_by_name(db, name):
        return None

    monkeypatch.setattr(crud, 'get_player_by_name', mock_get_player_by_name)

    def mock_create_player(db, player):
        created_player = models.Player(
            id=1,
            name=player.name,
            original_exp=player.original_exp,
            created_at=datetime_now
        )
        return created_player

    monkeypatch.setattr(crud, 'create_player', mock_create_player)

    player_data = {
        'name': 'Test Player',
        'original_exp': 1000
    }
    response = client.post('/api/players', json=player_data)

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'name': 'Test Player',
        'original_exp': 1000,
        'created_at': datetime_now.strftime('%Y-%m-%dT%H:%M:%S.%f'),
        'hiscores': []
    }


@pytest.mark.asyncio
async def test_create_player_duplicate_name(monkeypatch):
    def mock_get_player_by_name(db, name):
        return models.Player(
            created_at=datetime.now(),
            id=3,
            name='LeChuck',
            original_exp=0
        )

    monkeypatch.setattr(crud, 'get_player_by_name', mock_get_player_by_name)

    player_data = {
        'name': 'LeChuck',
        'original_exp': 1000
    }
    response = client.post('/api/players', json=player_data)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_hiscores_by_players(monkeypatch):
    def mock_get_players(payload):
        return mock_players

    monkeypatch.setattr(crud, 'get_players', mock_get_players)

    def mock_get_hiscores_by_player_id(payload, player_id):
        if player_id == 1:
            return mock_hiscores_for_elaine
        if player_id == 2:
            return mock_hiscores_for_guybrush
        if player_id == 3:
            return mock_hiscores_for_lechuck

    monkeypatch.setattr(crud, 'get_hiscores_by_player_id',
                        mock_get_hiscores_by_player_id)

    response = client.get('/api/hiscores_by_players')
    hiscores_by_players = response.json()

    assert response.status_code == 200
    assert len(hiscores_by_players) == len(mock_hiscores_by_players)

    # response list should be sorted correctly
    assert hiscores_by_players[0]['player']['name'] == mock_hiscores_by_players[0]['player']['name']
    assert hiscores_by_players[1]['player']['name'] == mock_hiscores_by_players[1]['player']['name']
    assert hiscores_by_players[2]['player']['name'] == mock_hiscores_by_players[2]['player']['name']

    # hiscores lists should be correct length
    assert len(hiscores_by_players[0]['hiscores']) == len(
        mock_hiscores_by_players[0]['hiscores'])
    assert len(hiscores_by_players[1]['hiscores']) == len(
        mock_hiscores_by_players[1]['hiscores'])
    assert len(hiscores_by_players[2]['hiscores']) == len(
        mock_hiscores_by_players[2]['hiscores'])


@pytest.mark.asyncio
async def test_create_hiscore(monkeypatch):
    datetime_now = datetime.now()

    def mock_create_hiscore(db, hiscore, player_id):
        created_hiscore = models.Hiscore(
            id=1,
            new_exp=hiscore.new_exp,
            total_gained_exp=hiscore.total_gained_exp,
            created_at=datetime_now,
            player_id=player_id
        )
        return created_hiscore

    monkeypatch.setattr(crud, 'create_hiscore', mock_create_hiscore)

    hiscore_data = {
        'new_exp': 100,
        'total_gained_exp': 500
    }
    player_id = 1
    response = client.post(
        f'/api/players/{player_id}/hiscores', json=hiscore_data)

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'new_exp': 100,
        'total_gained_exp': 500,
        'created_at': datetime_now.strftime('%Y-%m-%dT%H:%M:%S.%f'),
        'player_id': 1
    }


mock_players = [
    models.Player(
        created_at=datetime.now(),
        id=3,
        name='LeChuck',
        original_exp=0
    ),
    models.Player(
        created_at=datetime.now(),
        id=1,
        name='Elaine',
        original_exp=1337
    ),
    models.Player(
        created_at=datetime.now(),
        id=2,
        name='Guybrush',
        original_exp=0
    )
]


mock_hiscores_for_elaine = [
    models.Hiscore(
        id=1,
        new_exp=2337,
        total_gained_exp=1000,
        created_at=datetime.now(),
        player_id=1
    ),
    models.Hiscore(
        id=4,
        new_exp=3337,
        total_gained_exp=2000,
        created_at=datetime.now() + timedelta(days=1),
        player_id=1
    )
]


mock_hiscores_for_guybrush = [
    models.Hiscore(
        id=2,
        new_exp=50,
        total_gained_exp=50,
        created_at=datetime.now(),
        player_id=2
    ),
    models.Hiscore(
        id=5,
        new_exp=350,
        total_gained_exp=350,
        created_at=datetime.now() + timedelta(days=1),
        player_id=2
    )
]


mock_hiscores_for_lechuck = [
    models.Hiscore(
        id=3,
        new_exp=0,
        total_gained_exp=0,
        created_at=datetime.now(),
        player_id=3
    ),
    models.Hiscore(
        id=6,
        new_exp=0,
        total_gained_exp=0,
        created_at=datetime.now() + timedelta(days=1),
        player_id=3
    )
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
