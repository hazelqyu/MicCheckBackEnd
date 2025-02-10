from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse
from services.ai_service import generate_chat_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_interact(request: ChatRequest):
    try:
        raw_reply = generate_chat_response(request)
        plain_reply = raw_reply.replace("\n", " ").strip()
        return ChatResponse(
            npc_response=plain_reply
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

