from fastapi import FastAPI
from app.core.config import get_settings
from app.api.routes import query, agent

app = FastAPI()

settings = get_settings()
print("✅ Environment Loaded:")
print(f"DB: {settings.DB_USER}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
print(f"Assistant: {settings.OPENAI_ASSISTANT_ID}")

app.include_router(query.router, prefix="/api")
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])

@app.get("/")
def read_root():
    return {"message": "Map Query API is up!"}
