# FastAPI Calculator

Simple, reliable calculator API and UI built with FastAPI with **PostgreSQL database integration**. Supports addition, subtraction, multiplication, and division with calculation history, SQLAlchemy ORM, comprehensive testing, and Docker deployment.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-✨-teal)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![Pytest](https://img.shields.io/badge/tests-pytest-green)
![Playwright](https://img.shields.io/badge/E2E-Playwright-8A2BE2)
![CI](https://github.com/Vishesh0-7/Calculator_FastAPI/actions/workflows/ci.yml/badge.svg?branch=main)

**Docker Hub:** [vishy211/is601_mod11](https://hub.docker.com/r/vishy211/is601_mod11)


## Features

- **FastAPI service** with RESTful endpoints for calculations
- **PostgreSQL database** integration with SQLAlchemy ORM
- **Calculation history** - all operations stored in database with CRUD operations
- **Factory design pattern** for arithmetic operations (Add, Sub, Multiply, Divide)
- **Pydantic V2 schemas** with validation (division by zero prevention, type checking)
- **Static HTML UI** at `/` that saves calculations to database
- **Auto-generated API docs** at `/docs` (Swagger) and `/redoc`
- **Docker & Docker Compose** setup with PostgreSQL and pgAdmin
- **Comprehensive testing**: 51 tests (19 unit, 17 integration, 2 E2E, 13 legacy)
- **GitHub Actions CI/CD** with PostgreSQL service running tests on every push/PR
- **Docker Hub deployment** - Pull and run with one command


## Quickstart

Prerequisites:
- Python 3.8+
- pip

Clone and set up:

```bash
git clone https://github.com/Vishesh0-7/Calculator_FastAPI.git
cd calculator--FastApi

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies and browsers for Playwright
pip install -r requirements.txt
playwright install
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Open in your browser:
- UI: http://127.0.0.1:8000/
- Docs (Swagger): http://127.0.0.1:8000/docs
- Docs (ReDoc): http://127.0.0.1:8000/redoc


## API Reference

### Health & Legacy Endpoints

- **GET** `/health` - Health check
  - Response: `{ "status": "ok" }`

- **GET** `/add?a=<float>&b=<float>` - Simple addition (no database)
- **GET** `/sub?a=<float>&b=<float>` - Simple subtraction (no database)
- **GET** `/mul?a=<float>&b=<float>` - Simple multiplication (no database)
- **GET** `/div?a=<float>&b=<float>` - Simple division (no database)
- **GET** `/calc?op=<add|sub|mul|div>&a=<float>&b=<float>` - Generic calculation (no database)

### Database-Backed Calculation Endpoints

- **POST** `/calculations/` - Create and store a calculation
  - Body: `{ "a": float, "b": float, "type": "Add|Sub|Multiply|Divide" }`
  - Query: `?user_id=<int>` (optional)
  - Response: `{ "id": int, "a": float, "b": float, "type": string, "result": float, "user_id": int|null }`
  - Status: `201 Created` or `400 Bad Request`

- **GET** `/calculations/` - List all calculations
  - Query: `?skip=0&limit=100`
  - Response: Array of calculation objects

- **GET** `/calculations/{id}` - Get specific calculation
  - Response: Calculation object or `404 Not Found`

- **GET** `/users/{user_id}/calculations/` - Get calculations for a user
  - Query: `?skip=0&limit=100`
  - Response: Array of calculation objects

### Examples

```bash
# Legacy endpoints (no database)
curl "http://localhost:8000/add?a=3&b=2"
curl "http://localhost:8000/calc?op=mul&a=4&b=2.5"

# Database-backed endpoints
# Create calculation
curl -X POST "http://localhost:8000/calculations/" \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5, "type": "Add"}'

# List all calculations
curl "http://localhost:8000/calculations/"

# Get specific calculation
curl "http://localhost:8000/calculations/1"
```

For interactive API documentation, visit: http://localhost:8000/docs


## Project Structure

```
calculator--FastApi/
├── app/
│   ├── main.py              # FastAPI app, routes, database-backed endpoints
│   ├── models.py            # SQLAlchemy ORM models (User, Calculation)
│   ├── schemas.py           # Pydantic V2 schemas with validation
│   ├── factory.py           # Factory pattern for operations (Add, Sub, Multiply, Divide)
│   ├── crud.py              # Database CRUD operations
│   ├── database.py          # SQLAlchemy database configuration
│   ├── operations.py        # Legacy calculator operations
│   └── static/
│       └── index.html       # UI that saves calculations to database
├── tests/
│   ├── test_unit.py         # Unit tests (factory, schema validation) - 19 tests
│   ├── test_integration.py  # Integration tests (database CRUD) - 17 tests
│   ├── unit/                # Legacy unit tests
│   ├── integration/         # Legacy API endpoint tests
│   └── e2e/                 # Playwright E2E tests
├── Dockerfile               # Multi-stage build (development & production)
├── docker-compose.yml       # Local development with PostgreSQL + pgAdmin
├── docker-compose.prod.yml  # Production deployment configuration
├── .dockerignore            # Docker build exclusions
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
├── REFLECTION.md            # Development reflection and challenges
├── DOCKER_GUIDE.md          # Comprehensive Docker documentation
├── MODULE_11_IMPLEMENTATION.md  # Module 11 feature details
├── COMPLIANCE_VERIFICATION.md   # Requirements verification
└── .github/workflows/ci.yml # CI/CD with PostgreSQL service
```


## Testing

### Run Tests Locally

**Prerequisites:**
```bash
# Activate virtual environment
source venv/bin/activate  # or .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for E2E tests)
playwright install
```

**Run all tests:**
```bash
pytest -v
```

**Run specific test suites:**
```bash
# Unit tests (19 tests - factory pattern, schema validation)
pytest tests/test_unit.py -v

# Integration tests (17 tests - database CRUD operations)
pytest tests/test_integration.py -v

# Legacy unit tests (operations)
pytest tests/unit/test_operations.py -v

# Legacy integration tests (API endpoints)
pytest tests/integration/test_api.py -v

# E2E tests with Playwright (requires browser installation)
pytest tests/e2e/test_e2e_playwright.py -v
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run Tests in Docker

**With PostgreSQL:**
```bash
# Run all tests against PostgreSQL in Docker
docker-compose --profile test run --rm test

# Run specific tests
docker-compose --profile test run --rm test pytest tests/test_unit.py -v
```

### Test Summary

| Test Suite | Count | Description |
|------------|-------|-------------|
| **Unit Tests** | 19 | Factory operations, schema validation, division by zero |
| **Integration Tests** | 17 | Database CRUD, PostgreSQL integration, relationships |
| **Legacy Unit** | 6 | Basic arithmetic operations |
| **Legacy Integration** | 7 | HTTP API endpoint tests |
| **E2E Tests** | 2 | Playwright browser automation |
| **Total** | **51 tests** | Comprehensive coverage |


## Docker Deployment

### Docker Hub

Pre-built image available on Docker Hub:

**Pull and run:**
```bash
docker pull vishy211/is601_mod11:latest
docker run -d -p 8000:8000 vishy211/is601_mod11:latest
```

**Docker Hub Repository:** https://hub.docker.com/r/vishy211/is601_mod11

### Local Docker Setup

**Quick start with Docker Compose:**
```bash
# Start all services (app + PostgreSQL + pgAdmin)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

**Access the application:**
- **App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (login: admin@calculator.com / admin)

**Run tests in Docker:**
```bash
docker-compose --profile test run --rm test
```

### Manual Docker Build

```bash
# Build the image
docker build -t calculator-api:latest .

# Run with SQLite (development)
docker run -d -p 8000:8000 calculator-api:latest

# Run with PostgreSQL (production)
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  calculator-api:latest
```

For detailed Docker instructions, see [`DOCKER_GUIDE.md`](DOCKER_GUIDE.md).

---

## Continuous Integration (CI)

GitHub Actions runs on pushes/PRs to `main`:
- **PostgreSQL 15 service container** for realistic testing
- Install dependencies and Playwright browsers
- Run unit tests (factory pattern, schema validation)
- Run integration tests against PostgreSQL
- Run E2E tests with Playwright
- Automated testing ensures code quality before merge

**Workflow file:** `.github/workflows/ci.yml`

**Status:** ![CI](https://github.com/Vishesh0-7/Calculator_FastAPI/actions/workflows/ci.yml/badge.svg?branch=main)


## Development notes

- Logging is configured in `app/main.py`; adjust level/format as needed.
- Static assets are served from `app/static` at `/static` (UI uses `/` route for convenience).
- The operations are implemented in `app/operations.py` with simple, typed functions.


## Documentation

- **[REFLECTION.md](REFLECTION.md)** - Development experiences, challenges, and key learnings
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Comprehensive Docker deployment guide
- **[MODULE_11_IMPLEMENTATION.md](MODULE_11_IMPLEMENTATION.md)** - Module 11 feature details
- **[COMPLIANCE_VERIFICATION.md](COMPLIANCE_VERIFICATION.md)** - Requirements verification checklist

---

## Quick Links

- **GitHub Repository**: https://github.com/Vishesh0-7/Calculator_FastAPI
- **Docker Hub Image**: https://hub.docker.com/r/vishy211/is601_mod11
- **API Documentation**: http://localhost:8000/docs (when running)
- **CI/CD Pipeline**: https://github.com/Vishesh0-7/Calculator_FastAPI/actions

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **FastAPI** for the excellent web framework
- **SQLAlchemy** for powerful ORM capabilities
- **PostgreSQL** for reliable database management
- **Pydantic** for data validation
- **Docker** for containerization
- **Playwright** for browser automation
- **pytest** for comprehensive testing framework

---

## Author

**Vishesh**  
IS601 - Module 11  
November 2025

