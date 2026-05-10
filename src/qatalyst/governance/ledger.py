import json
import time


class CognitiveLedger:
    """Immutable record of system state transitions."""

    def __init__(self, path="cognitive_ledger.jsonl"):
        self.path = path

    def record(self, entry: dict):
        entry["timestamp"] = time.time()
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
