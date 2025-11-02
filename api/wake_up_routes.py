from fastapi import APIRouter, HTTPException
from models.wake_up_models import WakeUpRequest, WakeUpResponse
from services.ai_service import generate_wake_up_response

import sys

router = APIRouter()


@router.post("/wake_up", response_model=WakeUpResponse)
async def wake_up(request: WakeUpRequest):
    try:

        raw_reply = generate_wake_up_response(request)
        plain_reply = raw_reply.replace("\n", " ").strip()
        response = WakeUpResponse(
            wake_up_response=plain_reply
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
