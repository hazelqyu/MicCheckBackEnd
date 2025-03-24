# main.py
from fastapi import FastAPI

app = FastAPI(title="Rap Battle Game Backend API")


@app.get("/")
async def root():
    return {"message": "Rap Battle Game API is running!"}


from api.chat_routes import router as chat_router
from api.battle_routes import router as battle_router
from api.help_routes import router as help_router
from api.score_routes import router as score_router
from api.gossip_routes import router as gossip_router
from api.detect_routes import router as detect_router

# Include chat and battle endpoints.
app.include_router(chat_router)
app.include_router(battle_router)
app.include_router(help_router)
app.include_router(score_router)
app.include_router(gossip_router)
app.include_router(detect_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
