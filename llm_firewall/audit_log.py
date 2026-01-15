import json
import time
from typing import Dict, Any

DEFAULT_LOG_PATH = ".firewall_logs.jsonl"

def write_event(event: Dict[str, Any], path: str = DEFAULT_LOG_PATH) -> None:
    event = dict(event)
    event["ts"] = int(time.time())
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
