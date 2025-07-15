from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Request body for executing raw SQL queries."""

    sql: str


class QueryResponse(BaseModel):
    """Response containing query execution results."""

    result: list[dict]
