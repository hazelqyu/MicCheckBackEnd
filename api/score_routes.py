from fastapi import APIRouter, HTTPException
from models.score_models import ScoreRequest, ScoreResponse
from services.ai_service import generate_score_response
import json

router = APIRouter()


@router.post("/score", response_model=ScoreResponse)
async def get_score(request: ScoreRequest):
    try:
        raw_reply = generate_score_response(request)
        clarity_score, story_consistency_score, npc_weakness_score, audience_preference_score = parse_ai_response(
            raw_reply)
        return ScoreResponse(
            scoree=request.scoree,
            clarity_score=clarity_score,
            story_consistency_score=story_consistency_score,
            npc_weakness_score=npc_weakness_score,
            audience_preference_score=audience_preference_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def parse_ai_response(raw_reply: str):
    print(raw_reply)

    try:
        parsed_reply = json.loads(raw_reply)
        print(parsed_reply)
    except json.JSONDecodeError as e:
        raise ValueError("AI response is not valid JSON") from e

    try:
        clarity_score = parsed_reply.get("clarity_score", 0)
        story_consistency_score = parsed_reply.get("story_consistency_score", 0)
        npc_weakness_score = parsed_reply.get("npc_weakness_score", 0)
        audience_preference_score = parsed_reply.get("audience_preference_score", 0)

        return clarity_score, story_consistency_score, npc_weakness_score, audience_preference_score
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
