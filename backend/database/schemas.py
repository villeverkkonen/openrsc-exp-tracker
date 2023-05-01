from datetime import datetime
from pydantic import BaseModel


class HiscoreBase(BaseModel):
    new_exp: int
    created_at: datetime = datetime.now()


class HiscoreCreate(HiscoreBase):
    pass


class Hiscore(HiscoreBase):
    id: int
    player_id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    name: str
    original_exp: int


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    created_at: datetime = datetime.now()
    hiscores: list[Hiscore] = []

    class Config:
        orm_mode = True
