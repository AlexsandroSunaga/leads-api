# Leads API (FastAPI)

Captures marketing contact leads from static-site forms. Leads are validated (email, name, message) and appended to a JSONL file (`data/leads.jsonl`); a recent-leads endpoint reads them back.

The API lives in `backend/` (`src.main:backend_app`).

## Tech stack

| Area | Technologies |
|------|--------------|
| Backend | `Python`, `FastAPI`, `Pydantic Settings`, `email-validator`, `Uvicorn` |
| Database | `SQLAlchemy (async)`, `SQLite (aiosqlite)` |
| Auth | `JWT (python-jose)`, `passlib` |
| DevOps and tooling | `Docker`, `Docker Compose`, `pytest`, `mypy` |

## Run

Run the API:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
mkdir data                                           # SQLite file location (./data/app.db)
PYTHONPATH=src uvicorn src.main:backend_app --reload --port 8030   # PowerShell: $env:PYTHONPATH="src"
```

Interactive docs: http://127.0.0.1:8030/docs. The Docker image is built from the repository root (`docker compose up --build`, or `docker build -f backend/Dockerfile -t leads-api .`) and serves the API on port 8000. Leads are stored in the `/app/data` volume. The data directory can be overridden with the `DATA_DIR` environment variable. Leads are written to `data/leads.jsonl` at the repository root when running locally.

## Endpoints

- `GET /health`
- `POST /api/v1/leads`
- `GET /api/v1/leads/recent?limit=20` (limit 1 to 100)
- `GET /api/v1/integrations/status`

## Examples

```bash
curl -X POST http://127.0.0.1:8030/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","name":"Jane Doe","company":"Acme","message":"Interested in a demo.","source":"website"}'

curl "http://127.0.0.1:8030/api/v1/leads/recent?limit=5"
```

## Tests

Tests use FastAPI's TestClient against `src.main:backend_app`.

```bash
pip install -r backend/requirements.txt -r requirements-dev.txt
python -m pytest -q
```

## Author

**Alexsandro Sunaga**

## License

MIT License — see [LICENSE](LICENSE).
