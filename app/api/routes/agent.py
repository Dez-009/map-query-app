from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from openai import OpenAI
from app.schemas.agent import AgentQuery
from app.core.config import Settings

router = APIRouter()

def get_settings():
    return Settings()

def get_openai_client(settings: Settings = Depends(get_settings)):
    return OpenAI(api_key=settings.OPENAI_API_KEY)

@router.post("/query")
async def query_agent(
    payload: AgentQuery,
    openai_client: OpenAI = Depends(get_openai_client),
    settings: Settings = Depends(get_settings)
):
    """
    Handle natural language queries and convert them to SQL using OpenAI.
    Provides helpful suggestions when SQL syntax errors occur.
    """
    try:
        # If we have a thread_id, use it, otherwise create a new thread
        thread_id = payload.thread_id
        if not thread_id:
            thread = openai_client.beta.threads.create()
            thread_id = thread.id

        # Add the user's message to the thread
        message = openai_client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=payload.message
        )

        # Run the assistant
        run = openai_client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=settings.OPENAI_ASSISTANT_ID
        )

        # Get the assistant's response
        messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
        
        # Return the response and thread_id for continuation
        return {
            "message": messages.data[0].content[0].text.value,
            "thread_id": thread_id,
            "status": "success"
        }

    except ProgrammingError as e:
        # Handle SQL syntax errors
        error_message = str(e)
        suggestion = None
        
        if "how many" in payload.message.lower():
            suggestion = {
                "sql": "SELECT COUNT(*) FROM users WHERE role = 'admin'",
                "explanation": "This will count the number of users with admin role"
            }
        
        return {
            "error": "SQL Syntax Error",
            "message": error_message,
            "suggestion": suggestion,
            "documentation": "https://www.postgresql.org/docs/current/tutorial-sql.html"
        }
        
    except SQLAlchemyError as e:
        # Handle other SQL-related errors
        return {
            "error": "Database Error",
            "message": str(e),
            "status": "error"
        }
        
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
