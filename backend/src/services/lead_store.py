import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field

# DATA_DIR overrides the default (<repo root>/data), e.g. /app/data in Docker.
DATA_DIR = Path(os.environ.get("DATA_DIR") or Path(__file__).resolve().parents[3] / "data")
STORE = DATA_DIR / "leads.jsonl"
STORE.parent.mkdir(parents=True, exist_ok=True)


class LeadRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    company: str | None = None
    message: str = Field(min_length=1, max_length=2000)
    source: str = "website"


def create_lead(body: LeadRequest) -> dict:
    record = {
        "id": str(uuid.uuid4()),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    }
    with STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return {"id": record["id"], "status": "queued"}


def recent_leads(limit: int = 20) -> list[dict]:
    if limit < 1 or limit > 100:
        raise HTTPException(400, "limit must be between 1 and 100")
    if not STORE.exists():
        return []
    lines = STORE.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(line) for line in lines[-limit:]][::-1]
