from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    original_exp = Column(Integer)
    created_at = Column(DateTime)

    hiscores = relationship("Hiscore", back_populates="player")


class Hiscore(Base):
    __tablename__ = "hiscores"

    id = Column(Integer, primary_key=True, index=True)
    new_exp = Column(Integer)
    created_at = Column(DateTime)
    player_id = Column(Integer, ForeignKey("players.id"))

    player = relationship("Player", back_populates="hiscores")
