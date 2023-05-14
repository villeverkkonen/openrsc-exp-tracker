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

    def __repr__(self):
        return "<Player(id='{}', name='{}', original_exp={}, created_at={})>"\
            .format(self.id, self.name, self.original_exp, self.created_at)


class Hiscore(Base):
    __tablename__ = "hiscores"

    id = Column(Integer, primary_key=True, index=True)
    new_exp = Column(Integer)
    total_gained_exp = Column(Integer)
    created_at = Column(DateTime)
    player_id = Column(Integer, ForeignKey("players.id"))

    player = relationship("Player", back_populates="hiscores")

    def __repr__(self):
        return "<Hiscore(id='{}', new_exp='{}', total_gained_exp={}, created_at={}), player_id={})>"\
            .format(self.id, self.new_exp, self.total_gained_exp, self.created_at, self.player_id)
