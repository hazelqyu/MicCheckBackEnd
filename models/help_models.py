# models/help_models.py
from pydantic import BaseModel
from typing import List


class HelpRequest(BaseModel):
    writing_mode: int
    npc_id: str
    user_input: str


class HelpResponse(BaseModel):
    incomplete_bar_1: str
    incomplete_bar_2: str
    incomplete_bar_3: str
    incomplete_bar_4: str
