import openai
from app.core.config import get_settings

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY


def get_sql_from_natural_language(message: str, thread_id: str | None = None) -> dict:
    try:
        if not thread_id:
            thread = openai.beta.threads.create()
            thread_id = thread.id

        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=settings.OPENAI_ASSISTANT_ID,
        )

        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id, run.id)
            if run_status.status == "completed":
                break

        messages = openai.beta.threads.messages.list(thread_id)
        latest = messages.data[0].content[0].text.value

        return {"sql": latest, "thread_id": thread_id}

    except Exception as e:
        return {"error": str(e)}
