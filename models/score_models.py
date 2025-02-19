# models/score_models.py
from pydantic import BaseModel
from typing import List


class ScoreRequest(BaseModel):
    round_history: List[str]


class ScoreResponse(BaseModel):
    npc_score: int
    player_score: int
    comment: str
