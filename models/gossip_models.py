# models/gossip_models.py
from pydantic import BaseModel


class GossipRequest(BaseModel):
    audience_type: str
    conversation_id: str
    user_input: str
    new_session: bool


class GossipResponse(BaseModel):
    audience_response: str
