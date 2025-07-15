Perfect move, Dez — creating an agents.md file and clear Codex custom instructions is how we get it to act like a smart teammate, not just a code generator.

Let’s do this in two parts:

⸻

📄 Part 1: agents.md — Codex Task Understanding Doc

This file explains to Codex:
	•	What the app is
	•	What type of tasks it will receive
	•	What the expected structure/output should be

Here’s a ready-to-use version you can paste in agents.md:

# agents.md

## 🔧 Project: Map Query App

This app is a **modular monolith API** built with **FastAPI + PostgreSQL + Docker**.

It allows users to:
- Run raw SQL queries via a `/query` endpoint
- Receive formatted results (JSON or natural language)
- Later: use OpenAI agents to translate natural language into SQL

The system will support:
- PostgreSQL (raw SQL, no ORM yet)
- Alembic for migrations
- Docker containers
- OpenAI agents for intelligent routing and query generation

---

## 🧱 Structure

app/
├── core/          # Settings and config
├── db/            # DB connectors and raw SQL logic
├── services/      # Business logic
├── schemas/       # Pydantic models
├── api/           # FastAPI route handlers
├── agents/        # Agent-related tools (OpenAI later)
├── main.py        # App entrypoint
tests/             # Unit tests

---

## 🧠 Codex Task Format

Codex will receive tasks like:

> **Task 002 – Add Docker + PostgreSQL via docker-compose.yml**

And should respond with a full-code block that includes:
- File paths
- Clear section titles
- One-click copyable code
- ✅ Checkbox bullets for task tracking

---

## 📦 Example (One-Shot)

```txt
Task 004 – Implement Raw SQL Execution Service

Goal: Create a service in `app/services/sql_runner.py` to run raw SQL queries against PostgreSQL.

✅ Create `sql_runner.py` with `run_raw_sql(query: str) -> list[dict]`
✅ Use `psycopg2` to connect using environment variables
✅ Handle errors with safe rollback and return error info

```python
# app/services/sql_runner.py
import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

def run_raw_sql(query: str) -> list[dict]:
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if conn:
            conn.close()


⸻

✅ Style Guide
	•	Clean modular monolith structure
	•	Write production-ready, readable code
	•	Minimal boilerplate — clear & functional logic

---

## ⚙️ Part 2: Codex Custom Instructions

You can paste this into your Codex “custom instructions” field to guide it:

You are contributing to a modular monolith app called map-query-app. Your job is to complete backend tasks using FastAPI, PostgreSQL, and Docker. Each task should:
	1.	Start with a brief goal statement.
	2.	Use ✅ checklists for each step.
	3.	Output a single copyable code block that includes all files.
	4.	Follow the folder structure defined in agents.md.
	5.	Use raw SQL for now (no ORM yet).
	6.	Support future integration with OpenAI agents.

Example task format and output are defined in agents.md.

---

