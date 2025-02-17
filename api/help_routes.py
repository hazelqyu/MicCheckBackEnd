from fastapi import APIRouter, HTTPException
from models.help_models import HelpRequest, HelpResponse
from services.ai_service import generate_help_response
import json

router = APIRouter()


@router.post("/help", response_model=HelpResponse)
async def get_help(request: HelpRequest):
    try:
        raw_reply = generate_help_response(request)
        incomplete_bars, word_options = parse_ai_response(raw_reply)
        return HelpResponse(
            incomplete_bars=incomplete_bars,
            options=word_options
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
        incomplete_bar_1 = parsed_reply.get("incomplete_bar_1", "").strip()
        incomplete_bar_2 = parsed_reply.get("incomplete_bar_2", "").strip()
        incomplete_bar_3 = parsed_reply.get("incomplete_bar_3", "").strip()
        incomplete_bar_4 = parsed_reply.get("incomplete_bar_4", "").strip()
        word_options = parsed_reply.get("options", [])

        # Validate the response structure
        if not incomplete_bar_1 or not incomplete_bar_2 or not incomplete_bar_3 or not incomplete_bar_4 or not isinstance(word_options, list) or len(word_options) != 8:
            raise ValueError("Invalid response structure or missing required fields.")

        incomplete_bars = f"{incomplete_bar_1}\n{incomplete_bar_2}\n{incomplete_bar_3}\n{incomplete_bar_4}"
        return incomplete_bars, word_options
    except Exception as e:
        print(f"[FastAPI] Error parsing AI response: {e}")
        raise ValueError("Failed to process AI response")