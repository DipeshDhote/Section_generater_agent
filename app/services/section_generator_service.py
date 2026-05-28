from typing import Dict, Any, Optional

from app.graph.workflow import graph


class SectionGeneratorService:

    def generate_sections(self,CompanyId: str, user_id: str, user_name: str,global_constitution: str,specification: Optional[str] = None,max_retries: int = 2) -> Dict[str, Any]:

        initial_state = {
            "CompanyId": CompanyId,
            "user_id": user_id,
            "user_name": user_name,

            "global_constitution": global_constitution,
            "company_constitution": None,
            "specification": specification,

            "section_names": [],
            "current_section_index": 0,
            "current_section_name": None,

            "retrieved_chunks": [],
            "current_generated_section": None,
            "generated_sections": [],
  
            "validation_status": None,
            "validation_feedback": None,
            "retry_count": 0,
            "max_retries": max_retries,

            "current_step": "started",
            "status": "running",
            "error": None,
        }

        return graph.invoke(initial_state)