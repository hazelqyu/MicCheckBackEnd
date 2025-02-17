# models/chat_models.py
from pydantic import BaseModel


class ChatRequest(BaseModel):
    npc_id: str
    conversation_id: str
    user_input: str
    new_session: bool


class ChatResponse(BaseModel):
    npc_response: str
