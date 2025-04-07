from fastapi import APIRouter, HTTPException
from models.score_models import ScoreRequest, ScoreResponse
from services.ai_service import generate_score_response
import json
import logging
import sys

router = APIRouter()

score_logger = logging.getLogger("score")
score_logger.setLevel(logging.INFO)

# if not score_logger.handlers:
#     file_handler = logging.FileHandler("logs/score_logs.txt", encoding="utf-8")
#     file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
#     score_logger.addHandler(file_handler)

if not score_logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    score_logger.addHandler(stream_handler)


@router.post("/score", response_model=ScoreResponse)
async def get_score(request: ScoreRequest):
    try:
        score_logger.info(f"{request.scoree}'s rap:\n{request.rap_lyrics}\n")

        raw_reply = generate_score_response(request)
        clarity_score, story_consistency_score, cleverness_score, npc_weakness_score, rhyming_ability_score, audience_preference_score, comment = parse_ai_response(raw_reply)
        response = ScoreResponse(
            scoree=request.scoree,
            clarity_score=clarity_score,
            story_consistency_score=story_consistency_score,
            cleverness_score=cleverness_score,
            npc_weakness_score=npc_weakness_score,
            rhyming_ability_score=rhyming_ability_score,
            audience_preference_score=audience_preference_score,
            comment=comment
        )
        score_logger.info(
            f"\n{response.scoree}'s score:\nClarity Score: {clarity_score}\nStory Consistency Score:{story_consistency_score}\nCleverness Score:{cleverness_score}\nNPC Weakness Score:{npc_weakness_score}\nRhyming Ability Score:{rhyming_ability_score}, Audience Preference Score:{audience_preference_score}\n")
        score_logger.info(comment)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def parse_ai_response(raw_reply: str):
    try:
        parsed_reply = json.loads(raw_reply)
    except json.JSONDecodeError as e:
        raise ValueError("AI response is not valid JSON") from e

    try:
        clarity_score = parsed_reply.get("clarity_score", 0)
        story_consistency_score = parsed_reply.get("story_consistency_score", 0)
        cleverness_score = parsed_reply.get("cleverness_score", 0)
        npc_weakness_score = parsed_reply.get("npc_weakness_score", 0)
        rhyming_ability_score = parsed_reply.get("rhyming_ability_score", 0)
        audience_preference_score = parsed_reply.get("audience_preference_score", 0)
        comment = parsed_reply.get("comment", 0)

        return clarity_score, story_consistency_score, cleverness_score, npc_weakness_score, rhyming_ability_score, audience_preference_score, comment
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
