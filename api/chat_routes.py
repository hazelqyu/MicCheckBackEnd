from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse
from services.ai_service import generate_chat_response
import logging
import sys

router = APIRouter()

chat_logger = logging.getLogger("chat")
chat_logger.setLevel(logging.INFO)

# if not chat_logger.handlers:
#     file_handler = logging.FileHandler("logs/chat_logs.txt", encoding="utf-8")
#     file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
#     chat_logger.addHandler(file_handler)

if not chat_logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    chat_logger.addHandler(stream_handler)


@router.post("/chat", response_model=ChatResponse)
async def chat_interact(request: ChatRequest):
    try:
        chat_logger.info(f"\n{request.conversation_id} \n User: {request.user_input}\n")

        raw_reply = generate_chat_response(request)
        plain_reply = raw_reply.replace("\n", " ").strip()
        response = ChatResponse(
            chat_response=plain_reply
        )

        chat_logger.info(f"\nAI: {response.chat_response}\n")

        return response
    except Exception as e:
        chat_logger.error(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
