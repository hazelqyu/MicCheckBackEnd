# models/help_models.py
from pydantic import BaseModel
from typing import List


class HelpRequest(BaseModel):
    npc_id: str
    conversation_id: str
    user_input: str
    new_session: bool


class HelpResponse(BaseModel):
    incomplete_bars: str
    options: List[str]
