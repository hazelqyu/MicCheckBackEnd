from fastapi import APIRouter, HTTPException
from models.detect_models import DetectRequest, DetectResponse, HighlightRange
from services.ai_service import generate_detect_response
import json
import logging
import sys

router = APIRouter()

detect_logger = logging.getLogger("detect")
detect_logger.setLevel(logging.INFO)

if not detect_logger.handlers:
    file_handler = logging.FileHandler("logs/detect_logs.txt", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    detect_logger.addHandler(file_handler)


@router.post("/detect", response_model=DetectResponse)
async def weakness_detect(request: DetectRequest):
    try:
        detect_logger.info(f"message:\n{request.input_text}")

        raw_reply = generate_detect_response(request)
        detected, highlights, summaries, categories, indices = parse_ai_response(raw_reply)

        highlight_ranges = []
        for phrase in highlights:
            start = request.input_text.find(phrase)
            if start != -1:
                end = start + len(phrase)
                highlight_ranges.append(HighlightRange(start=start, end=end))
            else:
                detect_logger.warning(f"Phrase '{phrase}' not found in input text")

        response = DetectResponse(
            detected=detected,
            highlights=highlights,
            highlight_indices=highlight_ranges,
            summaries=summaries,
            categories=categories,
            indices=indices
        )

        detect_logger.info(
            f"Detected: {response.detected}\n"
            f"Highlights: {response.highlights}\n"
            f"Summaries: {response.summaries}\n"
            f"Categories: {response.categories}"
            f"Indices: {response.indices}")

        return response

    except Exception as e:
        detect_logger.error(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def parse_ai_response(raw_reply: str):
    try:
        parsed_reply = json.loads(raw_reply)
    except json.JSONDecodeError as e:
        raise ValueError("AI response is not valid JSON") from e

    try:
        detected = parsed_reply.get("detected", True)
        highlights = parsed_reply.get("highlights", [])
        summaries = parsed_reply.get("summaries", [])
        categories = parsed_reply.get("categories", [])
        indices = parsed_reply.get("indices", [])

        if detected:
            if not highlights or not summaries or not categories or not indices:
                raise ValueError("Invalid response structure or missing required fields in the AI detect response.")

        return detected, highlights, summaries, categories, indices

    except Exception as e:
        print(f"[FastAPI] Error parsing detect AI response: {e}")
        raise ValueError("Failed to process AI response")
