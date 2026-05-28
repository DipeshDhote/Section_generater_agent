from typing import Dict, Any

from app.graph.state import WorkflowState
from app.services.qdrant_service import QdrantService


qdrant_service = QdrantService()


def get_available_sections_from_qdrant(state: WorkflowState) -> Dict[str, Any]:

    try:
        CompanyId = state.get("CompanyId")

        if not CompanyId:
            raise ValueError("CompanyId is missing")

        section_names = qdrant_service.get_unique_section_names_by_company_id(
            CompanyId=CompanyId
        )

        if not section_names:
            raise ValueError(
                f"No sections found in Qdrant for CompanyId: {CompanyId}"
            )

        return {
            "section_names": section_names,
            "current_section_index": 0,
            "current_section_name": None,
            "current_step": "available_sections_loaded",
            "status": "running",
            "error": None
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Get Available Sections Error: {str(e)}"
        }


# def get_chunks_by_current_section(state: WorkflowState) -> Dict[str, Any]:

#     try:
#         CompanyId = state.get("CompanyId")
#         current_section_name = state.get("current_section_name")

#         if not CompanyId:
#             raise ValueError("CompanyId is missing")

#         if not current_section_name:
#             raise ValueError("current_section_name is missing")

#         chunks = qdrant_service.get_chunks_by_company_id_and_section_name(
#             CompanyId=CompanyId,
#             RelatedSection=current_section_name
#         )

#         return {
#             "retrieved_chunks": chunks,
#             "current_step": "section_chunks_loaded",
#             "status": "running",
#             "error": None
#         }

#     except Exception as e:
#         return {
#             "status": "failed",
#             "error": f"Get Section Chunks Error: {str(e)}"
#         }



def get_chunks_by_current_section(state: WorkflowState) -> Dict[str, Any]:

    try:
        CompanyId = state.get("CompanyId")
        current_section_name = state.get("current_section_name")

        # print("\n" + "=" * 80)
        # print("RETRIEVAL NODE STARTED")
        # print("COMPANY ID:", CompanyId)
        # print("CURRENT SECTION:", current_section_name)
        # print("=" * 80)

        if not CompanyId:
            raise ValueError("CompanyId is missing")

        if not current_section_name:
            raise ValueError("current_section_name is missing")

        chunks = qdrant_service.get_chunks_by_company_id_and_section_name(
            CompanyId=CompanyId,
            RelatedSection=current_section_name
        )

        print("TOTAL CHUNKS FOUND:", len(chunks))

        # if chunks:
        #     print("FIRST CHUNK RELATED SECTION:", chunks[0].get("RelatedSection"))
        #     print("FIRST CHUNK TEXT SAMPLE:", chunks[0].get("Text", "")[:300])

        # print("=" * 80)

        return {
            "retrieved_chunks": chunks,
            "current_step": "section_chunks_loaded",
            "status": "running",
            "error": None
        }

    except Exception as e:

        # print("\nRETRIEVAL NODE FAILED")
        # print("ERROR:", str(e))
        # print("=" * 80)

        return {
            "status": "failed",
            "error": f"Get Section Chunks Error: {str(e)}"
        }