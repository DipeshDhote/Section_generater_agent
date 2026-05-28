from typing import Dict, Any

from app.graph.state import WorkflowState


def store_section_result(state: WorkflowState) -> Dict[str, Any]:
    try:
        generated_sections = state.get("generated_sections", [])
        current_section = state.get("current_generated_section")
        validation_status = state.get("validation_status")
        current_index = state.get("current_section_index", 0)

        if validation_status == "passed" and current_section:
            section_with_id = {
                "Id": len(generated_sections) + 1,
                "SectionName": current_section["SectionName"],
                "Summary": current_section["Summary"],
                "Purpose": current_section["Purpose"],
                "SubSections": current_section["SubSections"],
            }

            generated_sections.append(section_with_id)

        return {
            "generated_sections": generated_sections,
            "current_section_index": current_index + 1,
            "current_generated_section": None,
            "retrieved_chunks": [],
            "validation_status": None,
            "validation_feedback": None,
            "retry_count": 0,
            "current_step": "section_result_stored",
            "status": "running",
            "error": None,
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Store Section Result Error: {str(e)}",
        }