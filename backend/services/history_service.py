import json
from pathlib import Path

LOG_PATH = Path("backend/data/query_log.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_interaction(entry: dict):
    """Append a single query/response record to query_log.json."""
    logs = []
    if LOG_PATH.exists():
        try:
            logs = json.load(open(LOG_PATH))
        except Exception:
            logs = []
    logs.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
