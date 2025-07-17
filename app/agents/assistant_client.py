from openai import OpenAI
from app.core.config import get_settings
from time import sleep

settings = get_settings()
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=settings.OPENAI_REQUEST_TIMEOUT,
    max_retries=settings.OPENAI_MAX_RETRIES,
)


def get_sql_from_natural_language(message: str, thread_id: str | None = None) -> dict:
    try:
        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=settings.OPENAI_ASSISTANT_ID,
            instructions="""You are a SQL query assistant. Always return valid PostgreSQL queries.
            For temporal queries using intervals, always use INTERVAL syntax like "INTERVAL '1 hour'".
            Never use natural language in the response - only return the SQL query.
            The available tables are:
            - query_logs (columns: id, sql TEXT, executed_at TIMESTAMP WITH TIME ZONE)"""
        )

        timeout_counter = 0
        max_wait = settings.OPENAI_REQUEST_TIMEOUT
        while timeout_counter < max_wait:
            run_status = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                return {"error": f"OpenAI run failed with status: {run_status.status}"}
            sleep(2)  # Longer sleep to avoid too frequent polling
            timeout_counter += 2

        if timeout_counter >= max_wait:
            return {"error": "OpenAI request timed out"}

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        latest = messages.data[0].content[0].text.value

        return {"sql": latest, "thread_id": thread_id}

    except Exception as e:
        return {"error": str(e)}
