from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.sql_runner import run_raw_sql

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_runner(payload: QueryRequest) -> QueryResponse:
    """Execute raw SQL provided in the request body."""

    result = run_raw_sql(payload.sql)
    if result and isinstance(result, list) and "error" in result[0]:
        raise HTTPException(status_code=400, detail=result[0]["error"])
    return QueryResponse(result=result)
