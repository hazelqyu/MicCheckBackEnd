from fastapi import APIRouter, HTTPException
from models.score_models import ScoreRequest, ScoreResponse
from services.ai_service import generate_score_response
import json

router = APIRouter()


@router.post("/score", response_model=ScoreResponse)
async def get_help(request: ScoreRequest):
    try:
        raw_reply = generate_score_response(request)
        npc_score, player_score, comment = parse_ai_response(raw_reply)
        return ScoreResponse(
            npc_score = npc_score,
            player_score = player_score,
            comment=comment
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def parse_ai_response(raw_reply: str):
    print(raw_reply)

    try:
        parsed_reply = json.loads(raw_reply)
    except json.JSONDecodeError as e:
        raise ValueError("AI response is not valid JSON") from e

    try:
        npc_score = parsed_reply.get("npc_score", 0)
        player_score = parsed_reply.get("player_score", 0)
        comment = parsed_reply.get("comment", "")

        if not npc_score or not player_score or not comment:
            raise ValueError("Invalid response structure or missing required fields.")
        return npc_score, player_score, comment
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
