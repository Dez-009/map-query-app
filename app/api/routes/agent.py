from fastapi import APIRouter, HTTPException
from app.schemas.agent import AgentQuery
from app.agents.assistant_client import get_sql_from_natural_language
from app.services.sql_runner import run_raw_sql

router = APIRouter()


@router.post("/query")
def query_agent(payload: AgentQuery):
    response = get_sql_from_natural_language(payload.message, payload.thread_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    sql = response.get("sql")
    thread_id = response.get("thread_id")

    result = run_raw_sql(sql)
    if result and "error" in result[0]:
        return {
            "error": result[0]["error"],
            "hint": "Please check your table name or SQL syntax.",
            "example": "SELECT COUNT(*) FROM users WHERE role = 'admin';",
            "thread_id": thread_id,
        }

    return {"result": result, "thread_id": thread_id, "sql": sql}
