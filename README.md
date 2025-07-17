# Map Query App

Map Query App is a powerful property management system with an AI-powered query interface. Built with **FastAPI**, **Docker**, and integrated with **OpenAI**, it provides both property management capabilities and an intuitive natural language interface for database queries.

> 🏢 **Are you a property management professional?**  
> Check out our [user-friendly overview](docs/about.md) to see how Map Query App can give you deeper insights into your property portfolio.

## Features

### Property Management
- Complete property and unit tracking
- Resident management with contact information
- Payment processing and history
- Maintenance and repair request handling
- Pet and vehicle registration
- Comprehensive data model for property operations

### AI-Powered Query Interface
- Natural language to SQL translation via OpenAI integration (`/api/agent/query`)
- Direct SQL execution via the `/api/query` endpoint
- Intelligent query validation and error handling
- Query logging and history tracking
- Thread-based conversation history with OpenAI Assistant

### Technical Features
- Containerized development environment with Docker Compose
- Database migrations managed by Alembic
- Comprehensive test coverage
- Automated data seeding for development

## Project Structure

```
app/
├── api/         # FastAPI route handlers
│   └── routes/  # API endpoints for query and agent interfaces
├── core/        # Settings and configuration
├── models/      # SQLAlchemy models
│   ├── property.py    # Property management
│   ├── unit.py       # Unit details
│   ├── resident.py   # Resident information
│   ├── payment.py    # Payment processing
│   ├── repair.py     # Maintenance requests
│   ├── pet.py        # Pet registration
│   └── vehicle.py    # Vehicle management
├── schemas/     # Pydantic models
│   ├── property.py   # Property DTOs
│   ├── unit.py      # Unit DTOs
│   ├── resident.py  # Resident DTOs
│   ├── payment.py   # Payment DTOs
│   ├── repair.py    # Repair DTOs
│   ├── pet.py       # Pet DTOs
│   └── vehicle.py   # Vehicle DTOs
├── services/    # Business logic
├── agents/      # OpenAI integration
├── main.py      # Application entrypoint
migrations/      # Database migrations
scripts/         # Utility scripts
└── tests/       # Unit and integration tests
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd map-query-app
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to add:
   - Your OpenAI API key
   - OpenAI Assistant ID (or use the default)
   - Database credentials (or use defaults)

3. **Start the application**
   ```bash
   # Build and start all services
   docker compose up --build

   # In another terminal, run migrations
   docker compose exec web alembic upgrade head

   # Seed demo data (recommended for testing)
   docker compose exec web python -m scripts.seed_demo_data

   # Seed query history (optional)
   docker compose exec web python -m scripts.seed_data
   ```

4. **Test the API**
   The API will be available at `http://localhost:8000`. Try it out:
   ```bash
   # Natural language queries
   curl -X POST http://localhost:8000/api/agent/query \
     -H "Content-Type: application/json" \
     -d '{"message": "Show me all vacant units"}'

   curl -X POST http://localhost:8000/api/agent/query \
     -H "Content-Type: application/json" \
     -d '{"message": "List residents with overdue payments"}'

   # Direct SQL query
   curl -X POST http://localhost:8000/api/query \
     -H "Content-Type: application/json" \
     -d '{"sql": "SELECT p.name, u.unit_number, r.first_name, r.last_name FROM properties p JOIN units u ON p.id = u.property_id LEFT JOIN residents r ON u.id = r.unit_id;"}'
   ```

## Development and Testing

### Running Tests

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**
   ```bash
   # Run all tests
   PYTHONPATH=. pytest

   # Run with coverage
   PYTHONPATH=. pytest --cov=app

   # Run specific test file
   PYTHONPATH=. pytest tests/test_sql_runner.py
   ```

Tests require a PostgreSQL instance. When using Docker Compose, PostgreSQL is exposed on port `5432`.

### Development

- API documentation available at `http://localhost:8000/docs`
- OpenAPI spec at `http://localhost:8000/openapi.json`
- Database migrations in `migrations/versions/`
- Sample data seeding via `scripts/seed_data.py`

## API Reference

See [docs/api.md](docs/api.md) for detailed endpoint documentation.

## License

This project is licensed under the MIT License.
