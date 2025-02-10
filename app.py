# app.py
from fastapi import FastAPI
from api.chat_routes import router as chat_router
from api.battle_routes import router as battle_router


app = FastAPI(title="Rap Battle Game Backend API")

# Include chat and battle endpoints.
app.include_router(chat_router)
app.include_router(battle_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
