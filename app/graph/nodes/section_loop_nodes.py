from typing import Dict, Any

from app.graph.state import WorkflowState


def init_section_loop(state: WorkflowState) -> Dict[str, Any]:
    return {
        "current_section_index": 0,
        "current_section_name": None,
        "generated_sections": [],
        "current_step": "section_loop_initialized",
        "status": "running",
        "error": None,
    }


def get_next_section(state: WorkflowState) -> Dict[str, Any]:
    try:
        section_names = state.get("section_names", [])
        current_index = state.get("current_section_index", 0)

        if current_index >= len(section_names):
            return {
                "current_section_name": None,
                "current_step": "no_more_sections",
                "status": "running",
                "error": None,
            }

        return {
            "current_section_name": section_names[current_index],
            "retrieved_chunks": [],
            "current_generated_section": None,
            "validation_status": None,
            "validation_feedback": None,
            "retry_count": 0,
            "current_step": "current_section_selected",
            "status": "running",
            "error": None,
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Get Next Section Error: {str(e)}",
        }