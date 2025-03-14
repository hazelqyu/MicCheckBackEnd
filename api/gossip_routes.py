from fastapi import APIRouter, HTTPException
from models.gossip_models import GossipRequest, GossipResponse
from services.ai_service import generate_gossip_response
import logging
import sys

router = APIRouter()

gossip_logger = logging.getLogger("gossip")
gossip_logger.setLevel(logging.INFO)

if not gossip_logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    gossip_logger.addHandler(stream_handler)


@router.post("/gossip", response_model=GossipResponse)
async def gossip_interact(request: GossipRequest):
    try:
        gossip_logger.info(f"\n{request.conversation_id} \n User: {request.user_input}\n")

        raw_reply = generate_gossip_response(request)
        plain_reply = raw_reply.replace("\n", " ").strip()
        response = GossipResponse(
            audience_response=plain_reply
        )

        gossip_logger.info(f"\nAI: {response.audience_response}\n")

        return response
    except Exception as e:
        gossip_logger.error(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
