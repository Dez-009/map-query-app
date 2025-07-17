"""Utilities for formatting database query results into natural language."""

from typing import List, Dict


def format_natural_language_response(original_query: str, result: List[Dict]) -> str:
    """Summarize a SQL query result into a short natural language sentence."""
    if not result:
        return "There were no results matching your request."

    if isinstance(result[0], dict) and ("count" in result[0] or "total" in result[0]):
        key = "count" if "count" in result[0] else "total"
        value = result[0][key]
        return f"There are {value} results matching your request."

    if len(result) == 1 and len(result[0]) == 1:
        only_value = list(result[0].values())[0]
        return f"The result is: {only_value}."

    preview = result[:5]
    items = [", ".join(f"{k}: {v}" for k, v in row.items()) for row in preview]
    return (
        f"There are {len(result)} results. Here is a sample: " + "; ".join(items)
    )
