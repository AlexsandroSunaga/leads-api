# Leads API (FastAPI)

Captures marketing contact leads from static-site forms. Leads are validated (email, name, message) and appended to a JSONL file (`data/leads.jsonl`); a recent-leads endpoint reads them back.

There are two entry points in this repo:

| Entry | Location | Contents |
|---|---|---|
| Legacy | `app.main:app` (repo root, `app/`) | health, create lead, recent leads |
| Backend (current) | `backend/` (`src.main:backend_app`) | same, plus integrations status |

## Run

Legacy entry (from the repo root):

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8030
```

Backend entry:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
mkdir data                                           # SQLite file location (./data/app.db)
PYTHONPATH=src uvicorn src.main:backend_app --reload --port 8030   # PowerShell: $env:PYTHONPATH="src"
```

Interactive docs: http://127.0.0.1:8030/docs. The Docker image is built from the repository root (`docker compose up --build`, or `docker build -f backend/Dockerfile -t leads-api .`) and serves the backend entry on port 8000. Leads are stored in the `/app/data` volume. The data directory can be overridden with the `DATA_DIR` environment variable. Leads are written to `data/leads.jsonl` at the repository root when running locally.

## Endpoints

- `GET /health`
- `POST /api/v1/leads`
- `GET /api/v1/leads/recent?limit=20` (limit 1 to 100)
- `GET /api/v1/integrations/status` (backend entry only)

## Examples

```bash
curl -X POST http://127.0.0.1:8030/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","name":"Jane Doe","company":"Acme","message":"Interested in a demo.","source":"website"}'

curl "http://127.0.0.1:8030/api/v1/leads/recent?limit=5"
```

## Tests

Covers both the legacy entry (`app.main:app`) and the backend entry (`src.main:backend_app`).

```bash
pip install -r requirements.txt -r backend/requirements.txt -r requirements-dev.txt
python -m pytest -q
```

## Author

**Alexsandro Sunaga**

## License

MIT License — see [LICENSE](LICENSE).
