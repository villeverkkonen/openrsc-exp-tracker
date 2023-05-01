from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from itertools import groupby
from operator import attrgetter
from database import crud
from database import models
from database import schemas
from database.database import SessionLocal, engine

import string
import random
import json
import httpx

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="OpenRSC overall exp tracker",
    description="Tracks players overall experience every three hours"
)
api_app = FastAPI(title="API")
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="../client/dist", html=True), name="client")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
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


@api_app.get('/hiscores')
async def get_hiscores():
    return get_hiscores()


@api_app.get('/hiscores_by_players')
async def get_hiscores_by_players(db: Session = Depends(get_db)):
    hiscores_by_players = []
    players = crud.get_players(db)
    for player in players:
        hiscores = crud.get_hiscores_by_player_id(
            db=db, player_id=player.id)

        most_efficient_day = get_most_efficient_day(hiscores)

        hiscores_by_players.append(
            {"player": player, "hiscores": hiscores, "most_efficient_day": most_efficient_day})
    return hiscores_by_players


@api_app.get('/hiscores_by_player_id')
async def get_hiscores_by_player_id(player_id: int, db: Session = Depends(get_db)):
    return crud.get_hiscores_by_player_id(db=db, player_id=player_id)


@api_app.post('/players/{player_id}/hiscores', response_model=schemas.Hiscore)
def create_hiscore(hiscore: schemas.HiscoreCreate, player_id: int, db: Session = Depends(get_db)):
    return crud.create_hiscore(db=db, hiscore=hiscore, player_id=player_id)


@api_app.post('/players', response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_name(db=db, name=player.name)
    if db_player:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_player(db=db, player=player)


@api_app.get('/players', response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    return crud.get_players(db)


@api_app.get('/players/{name}', response_model=list[schemas.Player])
def get_player_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_player_by_name(db=db, name=name)


def get_most_efficient_day(hiscores):
    max_diff = 0
    max_day = None
    daily_exp = {}

    for hiscore in hiscores:
        day = hiscore.created_at.date()

        # Update the earliest and latest new_exp for this day in the dictionary
        if day in daily_exp:
            daily_exp[day]['earliest'] = min(
                daily_exp[day]['earliest'], hiscore.new_exp)
            daily_exp[day]['latest'] = max(
                daily_exp[day]['latest'], hiscore.new_exp)
        else:
            daily_exp[day] = {'earliest': hiscore.new_exp,
                              'latest': hiscore.new_exp}

        # Calculate the difference between the earliest and latest new_exp for this day
        diff = daily_exp[day]['latest'] - daily_exp[day]['earliest']

        # Check if this day has a same or higher difference than the current maximum
        if diff >= max_diff:
            max_diff = diff
            max_day = day

    return {"day": max_day, "gained_exp": max_diff}
    # print(f"The day with the highest difference between earliest and latest new_exp is {max_day} with a difference of {max_diff}")


# Initialize database with dummy data for local testing
# TODO doesn't work yet
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
