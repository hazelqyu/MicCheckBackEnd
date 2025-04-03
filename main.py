# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rap Battle Game Backend API")

# Allow requests from anywhere (or just from your Itch.io game URL)
origins = [
    "https://hazelqyu.itch.io",  # Your game
    "http://localhost:8000",     # If you test locally
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <- Allow all origins (any domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Rap Battle Game API is running!"}


from api.chat_routes import router as chat_router
from api.battle_routes import router as battle_router
from api.help_routes import router as help_router
from api.score_routes import router as score_router
from api.detect_routes import router as detect_router

# Include chat and battle endpoints.
app.include_router(chat_router)
app.include_router(battle_router)
app.include_router(help_router)
app.include_router(score_router)
app.include_router(detect_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
