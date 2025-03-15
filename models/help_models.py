# models/help_models.py
from pydantic import BaseModel
from typing import List


class HelpRequest(BaseModel):
    npc_id: str
    conversation_id: str
    user_input: str
    new_session: bool


class HelpResponse(BaseModel):
    incomplete_bar_1: str
    incomplete_bar_2: str
    incomplete_bar_3: str
    incomplete_bar_4: str
    options: List[str]
