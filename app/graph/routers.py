from app.graph.state import WorkflowState


def validation_router(state: WorkflowState) -> str:
    validation_status = state.get("validation_status")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    if validation_status == "passed":
        return "store"

    if validation_status == "skip":
        return "store"

    if validation_status == "retry" and retry_count < max_retries:
        return "retry"

    return "store"


def has_more_sections_router(state: WorkflowState) -> str:
    current_index = state.get("current_section_index", 0)
    section_names = state.get("section_names", [])

    if current_index < len(section_names):
        return "continue"

    return "end"