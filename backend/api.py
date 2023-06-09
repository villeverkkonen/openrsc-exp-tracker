from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import crud
from database import models
from database import schemas
from database.database import SessionLocal, engine
from dotenv import load_dotenv
load_dotenv()

# import string
# import random
# import json
# import httpx

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='OpenRSC overall exp tracker',
    description='Tracks players overall experience gain once a day'
)
api_app = FastAPI(title='API')
app.mount('/api', api_app)
app.mount('/', StaticFiles(directory='../client/dist', html=True), name='client')


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


@api_app.get('/players', response_model=list[schemas.Player])
async def get_players(db: Session = Depends(get_db)):
    players = crud.get_players(db)
    return players


@api_app.post('/players', response_model=schemas.Player)
async def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_name(db=db, name=player.name)
    if db_player:
        raise HTTPException(status_code=400, detail='Name already registered')
    return crud.create_player(db=db, player=player)


@api_app.get('/hiscores_by_players')
async def get_hiscores_by_players(db: Session = Depends(get_db)):
    hiscores_by_players = []
    players = crud.get_players(db)
    for player in players:
        hiscores = crud.get_hiscores_by_player_id(
            db, player_id=player.id)
        hiscores_by_players.append(
            {'player': player, 'hiscores': hiscores})

    hiscores_by_players = sorted(
        hiscores_by_players, key=lambda x: x['hiscores'][-1].total_gained_exp if x['hiscores'] else 0, reverse=True)
    return hiscores_by_players


@api_app.post('/players/{player_id}/hiscores', response_model=schemas.Hiscore)
async def create_hiscore(hiscore: schemas.HiscoreCreate, player_id: int, db: Session = Depends(get_db)):
    return crud.create_hiscore(db=db, hiscore=hiscore, player_id=player_id)


# TODO doesn't work yet
# Initialize database with dummy data for local testing
# Uncomment imports also
# def create_dummy_hiscores_by_players():
#     db: Session = Depends(get_db)

#     for _ in range(3):
#         name = ''.join(random.choices(
#             string.ascii_uppercase + string.digits, k=8))
#         original_exp = random.randint(1, 1337)
#         player = schemas.PlayerCreate(name=name, original_exp=original_exp)
#         crud.create_player(db=db, player=player)

#     players = crud.get_players(db)
#     for player in players:
#         new_exp = player.original_exp
#         for _ in range(3):
#             new_exp = random.randint(new_exp, new_exp * 2)
#             hiscore = schemas.HiscoreCreate(new_exp=new_exp)
#             crud.create_hiscore(db=db, hiscore=hiscore, player_id=player.id)


# create_dummy_hiscores_by_players()
