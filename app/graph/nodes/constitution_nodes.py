from typing import Dict, Any

from app.graph.state import WorkflowState
from app.services.llm_service import llm
from app.prompts.constitution_rewrite_prompt import CONSTITUTION_REWRITE_PROMPT
from app.services.mongo_service import ConfigDocumentService


service = ConfigDocumentService()


def rewrite_company_constitution(state: WorkflowState) -> Dict[str, Any]:

    try:
        CompanyId = state.get("CompanyId")
        user_name = state.get("user_name")
        global_constitution = state.get("global_constitution")
        section_names = state.get("section_names")

        if not CompanyId:
            raise ValueError("CompanyId is missing")

        if not user_name:
            raise ValueError("user_name is missing")

        if not global_constitution:
            raise ValueError("global_constitution is missing")

        if not section_names:
            raise ValueError("section_names is empty")

        user_prompt = "\n".join(
            f"- {section}"
            for section in section_names
        )

        formatted_prompt = CONSTITUTION_REWRITE_PROMPT.invoke({
            "global_constitution": global_constitution,
            "section_names": user_prompt
        })

        response = llm.invoke(formatted_prompt)

        company_constitution = response.content.strip()

        constitution_id = service.save_rewritten_constitution(
            CompanyId=CompanyId,
            constitution=company_constitution,
            user_prompt=formatted_prompt.to_string(),
            created_by=user_name
        )

        return {
            "constitution_id": constitution_id,
            "company_constitution": company_constitution,
            "current_step": "company_constitution_generated_and_stored",
            "status": "running",
            "error": None
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": f"Constitution Rewrite Error: {str(e)}"
        }