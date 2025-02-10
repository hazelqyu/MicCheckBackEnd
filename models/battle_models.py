# models/battle_models.py
from pydantic import BaseModel
from typing import List


class FillInBlankRequest(BaseModel):
    npc_id: str
    conversation_id: str
    user_input: str  # For the player's turn, the chosen word; may be empty if initiating the battle
    new_game: bool


class FillInBlankResponse(BaseModel):
    npc_full_bar: str  # The complete rap bar from the AI NPC's turn
    npc_incomplete_bar: str  # The new rap bar with a missing final word (represented as "____")
    options: List[str]  # Three candidate words provided for the blank
