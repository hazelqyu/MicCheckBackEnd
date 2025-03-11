from fastapi import APIRouter, HTTPException
from models.score_models import ScoreRequest, ScoreResponse
from services.ai_service import generate_score_response
import json
import logging

router = APIRouter()

score_logger = logging.getLogger("score")
score_logger.setLevel(logging.INFO)

if not score_logger.handlers:
    file_handler = logging.FileHandler("logs/score_logs.txt", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    score_logger.addHandler(file_handler)


@router.post("/score", response_model=ScoreResponse)
async def get_score(request: ScoreRequest):
    try:
        score_logger.info(f"{request.scoree}'s rap:\n{request.rap_lyrics}\n")

        raw_reply = generate_score_response(request)
        clarity_score, story_consistency_score, npc_weakness_score, audience_preference_score, prediction, explanations = parse_ai_response(
            raw_reply)
        response = ScoreResponse(
            scoree=request.scoree,
            clarity_score=clarity_score,
            story_consistency_score=story_consistency_score,
            npc_weakness_score=npc_weakness_score,
            audience_preference_score=audience_preference_score,
            prediction=prediction
        )
        score_logger.info(
            f"\n{response.scoree}'s score:\nClarity Score: {clarity_score}\nStory Consistency Score:{story_consistency_score}\nNPC Weakness Score:{npc_weakness_score}\nAudience Preference Score:{audience_preference_score}\n")
        score_logger.info(explanations)
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
        npc_weakness_score = parsed_reply.get("npc_weakness_score", 0)
        audience_preference_score = parsed_reply.get("audience_preference_score", 0)
        prediction = parsed_reply.get("prediction", 0)

        explanation_1 = parsed_reply.get("explanation_1", "")
        explanation_2 = parsed_reply.get("explanation_2", "")
        explanation_3 = parsed_reply.get("explanation_3", "")
        explanation_4 = parsed_reply.get("explanation_4", "")

        prediction_reason = parsed_reply.get("prediction_reason", "")

        explanations = (f"\nExplanations:\n1. Clarity Score:{explanation_1}.\n2. Consistence Score:{explanation_2}\n3. "
                        f"Weakness Score:{explanation_3}.\n4. Audience Score: {explanation_4}.\n5. Audience Reaction "
                        f"Reason:{prediction_reason}")

        return clarity_score, story_consistency_score, npc_weakness_score, audience_preference_score, prediction, explanations
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
