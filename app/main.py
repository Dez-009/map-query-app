from fastapi import FastAPI
from app.api.routes import query, agent

app = FastAPI()

app.include_router(query.router, prefix="/api")
app.include_router(agent.router, prefix="/api/agent")

@app.get("/")
def read_root():
    return {"message": "Map Query API is up!"}
