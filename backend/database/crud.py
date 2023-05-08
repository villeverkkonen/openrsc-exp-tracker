from sqlalchemy.orm import Session
from sqlalchemy import asc
from datetime import datetime
from . import models
from . import schemas


def get_players(db: Session):
    return db.query(models.Player).all()


def get_player_by_name(db: Session, name: str):
    return db.query(models.Player).filter(models.Player.name == name).first()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(
        name=player.name,
        original_exp=player.original_exp,
        created_at=datetime.now()
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_hiscores_by_player_id(db: Session, player_id: int):
    return db.query(models.Hiscore).filter(models.Hiscore.player_id == player_id).order_by(asc(models.Hiscore.created_at)).all()


def create_hiscore(db: Session, hiscore: schemas.HiscoreCreate, player_id: int):
    db_hiscore = models.Hiscore(
        **hiscore.dict(),
        player_id=player_id
    )
    db.add(db_hiscore)
    db.commit()
    db.refresh(db_hiscore)
    return db_hiscore
