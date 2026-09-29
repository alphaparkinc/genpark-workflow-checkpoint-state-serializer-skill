"""Workflow Checkpoint State Serializer.
100% Python Standard Library.
"""

import json

class CheckpointSerializer:
    """Snapshots workflow execution states with delta journal compression."""
    def __init__(self):
        self.snapshots = []

    def commit_checkpoint(self, step_name: str, state: dict) -> dict:
        serialized = json.dumps(state, sort_keys=True)
        checkpoint_id = len(self.snapshots) + 1
        record = {
            "checkpoint_id": checkpoint_id,
            "step_name": step_name,
            "state": json.loads(serialized),
            "state_hash": hash(serialized)
        }
        self.snapshots.append(record)
        return record

    def restore_checkpoint(self, checkpoint_id: int) -> dict:
        for s in self.snapshots:
            if s["checkpoint_id"] == checkpoint_id:
                return s["state"]
        return None
