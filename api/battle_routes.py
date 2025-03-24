from fastapi import APIRouter, HTTPException
from models.battle_models import FillInBlankRequest, FillInBlankResponse
from services.ai_service import generate_fill_in_blank_response
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


@router.post("/battle/fill_in_blank", response_model=FillInBlankResponse)
async def fill_in_blank_interact(request: FillInBlankRequest):
    try:
        battle_logger.info(f"\n{request.conversation_id}\n User: \n{request.user_input}")
        raw_reply = generate_fill_in_blank_response(request)
        print(f"[FastAPI] AI Response:\n{raw_reply}")

        full_bar, incomplete_bar, word_options = parse_ai_response(raw_reply)

        response = FillInBlankResponse(
            round=request.round,
            npc_full_bar=full_bar,
            npc_incomplete_bar=incomplete_bar,
            options=word_options
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
        incomplete_bar = parsed_reply.get("npc_incomplete_bar", "").strip()
        word_options = parsed_reply.get("options", [])

        # Validate the response structure
        if not full_bar or not incomplete_bar or not isinstance(word_options, list) or len(word_options) != 3:
            raise ValueError("Invalid response structure or missing required fields.")

        return full_bar, incomplete_bar, word_options
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
