from fastapi import APIRouter, HTTPException
from app.schemas.agent import AgentQuery
from app.agents.assistant_client import get_sql_from_natural_language
from app.services.sql_runner import run_raw_sql

router = APIRouter()


@router.post("/query")
def query_agent(payload: AgentQuery):
    if not callable(get_sql_from_natural_language):
        raise HTTPException(status_code=500, detail="Agent function reference is invalid.")

    response = get_sql_from_natural_language(payload.message, payload.thread_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    sql = response.get("sql")
    thread_id = response.get("thread_id")

    # Try to extract just the SQL if the assistant included any explanation
    if sql.upper().startswith("SELECT"):
        sql = sql.strip()
    else:
        # Find the first SELECT statement
        import re
        match = re.search(r"SELECT\s+.*?;", sql, re.IGNORECASE | re.DOTALL)
        if match:
            sql = match.group(0).strip()
        else:
            return {
                "error": "No valid SQL query found in response",
                "hint": "The assistant response didn't contain a valid SELECT statement",
                "response": sql,
                "thread_id": thread_id,
            }

    result = run_raw_sql(sql)
    if result and isinstance(result, list) and result and "error" in result[0]:
        return {
            "error": result[0]["error"],
            "hint": "Please check your SQL syntax",
            "sql": sql,
            "thread_id": thread_id,
        }

    return {"result": result, "thread_id": thread_id, "sql": sql}
