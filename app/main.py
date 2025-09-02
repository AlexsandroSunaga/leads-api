import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

STORE = Path(__file__).resolve().parent.parent / "data" / "leads.jsonl"
STORE.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Marketing Leads API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class LeadRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    company: str | None = None
    message: str = Field(min_length=1, max_length=2000)
    source: str = "website"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/leads")
def create_lead(body: LeadRequest) -> dict:
    record = {
        "id": str(uuid.uuid4()),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    }
    with STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return {"id": record["id"], "status": "queued"}


@app.get("/api/v1/leads/recent")
def recent_leads(limit: int = 20) -> list[dict]:
    if limit < 1 or limit > 100:
        raise HTTPException(400, "limit must be between 1 and 100")
    if not STORE.exists():
        return []
    lines = STORE.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(line) for line in lines[-limit:]][::-1]
