from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime, timezone
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME  # noqa: E402


def validate_config() -> None:
    if "<username>" in MONGODB_URI or "<cluster>" in MONGODB_URI:
        raise SystemExit(
            "Edit config.py and set MONGODB_URI before running the demo scripts."
        )


def get_collection():
    validate_config()
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")
    return client, client[DATABASE_NAME][COLLECTION_NAME]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
