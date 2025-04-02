# models/chat_models.py
from pydantic import BaseModel


class ChatRequest(BaseModel):
    target_type: str
    chat_target_id: str
    conversation_id: str
    user_input: str
    new_session: bool


class ChatResponse(BaseModel):
    chat_response: str
