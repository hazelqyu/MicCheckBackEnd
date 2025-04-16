from fastapi import APIRouter, HTTPException
from models.battle_models import BattleRequest, BattleResponse
from services.ai_service import generate_battle_response
import json
import logging
import sys

router = APIRouter()


# Create a separate logger for battle with its own handler
battle_logger = logging.getLogger("battle")
battle_logger.setLevel(logging.INFO)

# Ensure the logger does not duplicate handlers
# if not battle_logger.handlers:
#     file_handler = logging.FileHandler("logs/battle_logs.txt", encoding="utf-8")
#     file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
#     battle_logger.addHandler(file_handler)

if not battle_logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    battle_logger.addHandler(stream_handler)


@router.post("/battle", response_model=BattleResponse)
async def battle_interact(request: BattleRequest):
    try:
        battle_logger.info(f"\n{request.conversation_id}\n User: \n{request.user_input}")
        raw_reply = generate_battle_response(request)
        print(f"[FastAPI] AI Response:\n{raw_reply}")

        full_bar= parse_ai_response(raw_reply)

        response = BattleResponse(
            round=request.round,
            npc_full_bar=full_bar,
        )
        battle_logger.info(f"\nAI:\n{response.npc_full_bar}")
        return response
    except Exception as e:
        battle_logger.error(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def parse_ai_response(raw_reply: str):
    try:
        parsed_reply = json.loads(raw_reply)
    except json.JSONDecodeError as e:
        raise ValueError("AI response is not valid JSON") from e

    try:
        full_bar_1 = parsed_reply.get("npc_full_bar_1", "").strip()
        full_bar_2 = parsed_reply.get("npc_full_bar_2", "").strip()
        full_bar_3 = parsed_reply.get("npc_full_bar_3", "").strip()
        full_bar_4 = parsed_reply.get("npc_full_bar_4", "").strip()

        full_bar = f"{full_bar_1}\n{full_bar_2}\n{full_bar_3}\n{full_bar_4}"

        # Validate the response structure
        if not full_bar:
            raise ValueError("Invalid response structure or missing required fields.")

        return full_bar
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
