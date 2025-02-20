# models/score_models.py
from pydantic import BaseModel


class ScoreRequest(BaseModel):
    npc_id: str
    player_id: str
    scoree: str
    rap_lyrics: str
    conversation_id: str


class ScoreResponse(BaseModel):
    scoree:str
    clarity_score: int
    story_consistency_score: int
    npc_weakness_score: int
    audience_preference_score: int
