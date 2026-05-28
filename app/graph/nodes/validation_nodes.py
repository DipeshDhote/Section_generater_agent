from typing import Dict, Any

from app.graph.state import WorkflowState


def validate_single_section(state: WorkflowState) -> Dict[str, Any]:
    try:
        section = state.get("current_generated_section")
        current_section_name = state.get("current_section_name")

        if section is None:
            return {
                "validation_status": "skip",
                "validation_feedback": None,
                "current_step": "section_validation_skipped",
                "status": "running",
                "error": None,
            }

        required_main_keys = {
            "SectionName",
            "Summary",
            "Purpose",
            "SubSections"
        }

        required_sub_keys = {
            "SubSectionId",
            "SubSectionName",
            "Summary"
        }

        if set(section.keys()) != required_main_keys:
            return {
                "validation_status": "retry",
                "validation_feedback": (
                    "Invalid schema. Main section object must contain exactly "
                    "SectionName, Summary, Purpose, and SubSections."
                ),
                "current_step": "section_validation_failed",
                "status": "running",
                "error": None,
            }

        if section["SectionName"] != current_section_name:
            return {
                "validation_status": "retry",
                "validation_feedback": (
                    f"SectionName must be exactly '{current_section_name}'."
                ),
                "current_step": "section_validation_failed",
                "status": "running",
                "error": None,
            }

        if not section["Summary"].strip():
            return {
                "validation_status": "retry",
                "validation_feedback": "Summary must not be empty.",
                "current_step": "section_validation_failed",
                "status": "running",
                "error": None,
            }

        if not section["Purpose"].strip():
            return {
                "validation_status": "retry",
                "validation_feedback": "Purpose must not be empty.",
                "current_step": "section_validation_failed",
                "status": "running",
                "error": None,
            }

        if not isinstance(section["SubSections"], list):
            return {
                "validation_status": "retry",
                "validation_feedback": "SubSections must be a JSON array.",
                "current_step": "section_validation_failed",
                "status": "running",
                "error": None,
            }

        for index, subsection in enumerate(section["SubSections"], start=1):

            if set(subsection.keys()) != required_sub_keys:
                return {
                    "validation_status": "retry",
                    "validation_feedback": (
                        "Invalid subsection schema. Each subsection must contain exactly "
                        "SubSectionId, SubSectionName, and Summary."
                    ),
                    "current_step": "section_validation_failed",
                    "status": "running",
                    "error": None,
                }

            if subsection["SubSectionId"] != index:
                return {
                    "validation_status": "retry",
                    "validation_feedback": (
                        "SubSectionId must start from 1 and increase sequentially "
                        "inside each section."
                    ),
                    "current_step": "section_validation_failed",
                    "status": "running",
                    "error": None,
                }

            if not str(subsection["SubSectionName"]).strip():
                return {
                    "validation_status": "retry",
                    "validation_feedback": "SubSectionName must not be empty.",
                    "current_step": "section_validation_failed",
                    "status": "running",
                    "error": None,
                }

            if not str(subsection["Summary"]).strip():
                return {
                    "validation_status": "retry",
                    "validation_feedback": "Subsection Summary must not be empty.",
                    "current_step": "section_validation_failed",
                    "status": "running",
                    "error": None,
                }

        return {
            "validation_status": "passed",
            "validation_feedback": None,
            "current_step": "section_validation_passed",
            "status": "running",
            "error": None,
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Section Validation Error: {str(e)}",
        }