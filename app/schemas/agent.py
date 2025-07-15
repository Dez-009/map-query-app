from pydantic import BaseModel

class AgentQuery(BaseModel):
    message: str
    thread_id: str | None = None  # Optional for new conversations
