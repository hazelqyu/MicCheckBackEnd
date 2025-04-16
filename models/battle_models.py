# models/battle_models.py
from pydantic import BaseModel
from typing import List


class BattleRequest(BaseModel):
    round: int
    npc_id: str
    conversation_id: str
    user_input: str
    new_game: bool


class BattleResponse(BaseModel):
    round: int
    npc_full_bar: str
