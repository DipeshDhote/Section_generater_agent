import json
from typing import Dict, Any

from app.graph.state import WorkflowState
from app.services.llm_service import llm
from app.prompts.single_section_prompt import SINGLE_SECTION_GENERATION_PROMPT
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()


def generate_single_section(state: WorkflowState):

    try:
        section_name = state.get("current_section_name")
        chunks = state.get("retrieved_chunks", [])

        print("\n" + "=" * 80)
        print("GENERATE NODE STARTED")
        print("CURRENT SECTION:", section_name)
        print("TOTAL CHUNKS:", len(chunks))
        print("=" * 80)

        if not section_name:
            raise ValueError("current_section_name is missing")

        if not chunks:
            print("NO CHUNKS FOUND - SECTION SKIPPED")

            return {
                "current_generated_section": None,
                "current_step": "section_skipped_no_chunks",
                "status": "running",
                "error": None,
            }

        context = "\n\n".join(
            chunk.get("Text", "")
            for chunk in chunks
            if chunk.get("Text")
        )

        print("\nCONTEXT LENGTH:", len(context))

        formatted_prompt = SINGLE_SECTION_GENERATION_PROMPT.invoke({
            "section_name": section_name,
            "company_constitution": state.get("company_constitution", ""),
            "specification": state.get("specification", ""),
            "context": context,
            "validation_feedback": (
                state.get("validation_feedback")
                or "No validation feedback."
            )
        })

        print("\nLLM INVOCATION STARTED")

        response = llm.invoke(formatted_prompt)

        content = response.content.strip()

        print("\nLLM RAW RESPONSE:")
        print(content)

        if content == "SKIP_SECTION":

            print("\nLLM RETURNED SKIP_SECTION")

            return {
                "current_generated_section": None,
                "current_step": "section_skipped_by_llm",
                "status": "running",
                "error": None,
            }

        section_obj = parser.parse(content)

        print("\nPARSED SECTION OBJECT:")
        print(json.dumps(section_obj, indent=2))

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

        if set(section_obj.keys()) != required_main_keys:
            raise ValueError(
                f"Invalid main section schema: {section_obj}"
            )

        if not isinstance(section_obj["SubSections"], list):
            raise ValueError(
                "SubSections must be a list"
            )

        for subsection in section_obj["SubSections"]:

            if set(subsection.keys()) != required_sub_keys:
                raise ValueError(
                    f"Invalid subsection schema: {subsection}"
                )

        print("\nSECTION VALIDATION PASSED")
        print("=" * 80)

        return {
            "current_generated_section": section_obj,
            "current_step": "single_section_generated",
            "status": "running",
            "error": None,
        }

    except Exception as e:

        print("\nSECTION GENERATION FAILED")
        print("ERROR:", str(e))
        print("=" * 80)

        return {
            "status": "failed",
            "error": f"Single Section Generation Error: {str(e)}"
        }