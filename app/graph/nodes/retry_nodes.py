from typing import Dict, Any

from app.graph.state import WorkflowState


def increment_retry_count(state: WorkflowState) -> Dict[str, Any]:
    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "current_step": "retry_count_incremented",
        "status": "running",
        "error": None,
    }