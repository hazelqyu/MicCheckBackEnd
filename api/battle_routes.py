from fastapi import APIRouter, HTTPException
from models.battle_models import FillInBlankRequest, FillInBlankResponse
from services.ai_service import generate_fill_in_blank_response
import json

router = APIRouter()


@router.post("/battle/fill_in_blank", response_model=FillInBlankResponse)
async def fill_in_blank_interact(request: FillInBlankRequest):
    try:
        raw_reply = generate_fill_in_blank_response(request)
        print(f"[FastAPI] AI Response:\n{raw_reply}")

        full_bar, incomplete_bar, word_options = parse_ai_response(raw_reply)

        return FillInBlankResponse(
            npc_full_bar=full_bar,
            npc_incomplete_bar=incomplete_bar,
            options=word_options
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def parse_ai_response(raw_reply: str):
    try:
        parsed_reply = json.loads(raw_reply)
    except json.JSONDecodeError as e:
        raise ValueError("AI response is not valid JSON") from e

    try:
        # Extract required fields from the JSON response
        full_bar = parsed_reply.get("npc_full_bar", "").strip()
        incomplete_bar = parsed_reply.get("npc_incomplete_bar", "").strip()
        word_options = parsed_reply.get("options", [])

        # Validate the response structure
        if not full_bar or not incomplete_bar or not isinstance(word_options, list) or len(word_options) != 3:
            raise ValueError("Invalid response structure or missing required fields.")

        return full_bar, incomplete_bar, word_options
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")
