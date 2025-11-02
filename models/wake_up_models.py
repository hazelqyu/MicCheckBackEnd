# models/wake_up_models.py
from pydantic import BaseModel


class WakeUpRequest(BaseModel):
    wake_up_request: str


class WakeUpResponse(BaseModel):
    wake_up_response: str
