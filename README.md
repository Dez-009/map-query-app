# Map Query App

Map Query App is a modular monolith API that allows users to execute raw SQL against a PostgreSQL database through a simple HTTP interface. It is built with **FastAPI**, **Docker**, and **Alembic** for migrations. Future versions will integrate OpenAI agents for natural language to SQL translation.

## Features

- Run raw SQL queries via the `/api/query` endpoint.
- Receive results in JSON format or error details when queries fail.
- Containerized development environment with Docker Compose.
- Database migrations managed by Alembic.
- Designed to support future OpenAI agent orchestration in `app/agents`.

## Project Structure

```
app/
├── api/       # FastAPI route handlers
├── core/      # Settings and configuration
├── db/        # Database models and connectors
├── schemas/   # Pydantic models
├── services/  # Business logic
├── agents/    # Placeholder for future OpenAI agents
├── main.py    # Application entrypoint
migrations/    # Alembic migration scripts
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd map-query-app
   ```
2. **Create the `.env` file** (already provided) with database settings.
3. **Start the stack** using Docker Compose:
   ```bash
   docker compose up --build
   ```
4. **Run database migrations** in another terminal:
   ```bash
   docker compose exec web alembic upgrade head
   ```
5. Access the API at `http://localhost:8000`.

## Running Tests

Install dependencies and run `pytest`:

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

A local PostgreSQL instance is required for tests. When using Docker Compose, the provided configuration exposes Postgres on port `5432`.

## API Reference

See [docs/api.md](docs/api.md) for detailed endpoint documentation.

## License

This project is licensed under the MIT License.
