from fastapi import FastAPI

from app.api.routes import query

app = FastAPI()

app.include_router(query.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Map Query API is up!"}
