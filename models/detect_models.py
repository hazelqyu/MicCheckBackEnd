# models/detect_models.py
from pydantic import BaseModel
from typing import List, Tuple


class HighlightRange(BaseModel):
    start: int
    end: int


class DetectRequest(BaseModel):
    npc_id: str
    input_text: str


class DetectResponse(BaseModel):
    detected: bool
    highlights: List[str]
    summaries: List[str]
    highlight_indices: List[HighlightRange]
    indices: List[int]
