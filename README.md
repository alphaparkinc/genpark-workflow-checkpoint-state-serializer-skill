# genpark-workflow-checkpoint-state-serializer-skill

Immutable execution state journal enabling checkpoint-based rollback and deterministic agent replay.

## Architecture

```mermaid
flowchart LR
    Step[Agent Workflow Step] --> Commit[commit_checkpoint]
    Commit --> Storage[(In-Memory Snapshots Journal)]
    Storage --> Restore[restore_checkpoint]
    Restore --> RestoredState[Restored Agent Context]
```

## Features
- **Deep Serialization**: Prevents mutation of previous snapshots.
- **Replayability**: Enables time-travel debugging across agent steps.
