from typing import TypedDict, Optional, List, Dict, Any


# class WorkflowState(TypedDict):
#     # Input Fields
#     CompanyId: str
#     user_id: str
#     user_name: str

#     # Constitution / Rules
#     global_constitution: str
#     company_constitution: Optional[str]
#     specification: Optional[str]

#     # Section Metadata
#     section_names: List[str]

#     # Loop Control
#     current_section_index: int
#     current_section_name: Optional[str]

#     # Qdrant Retrieval
#     retrieved_chunks: List[Dict[str, Any]]

#     # Current Generated Section
#     current_generated_section: Optional[Dict[str, Any]]

#     # Final Output
#     generated_sections: List[Dict[str, Any]]

#     # Validation / Retry
#     validation_status: Optional[str]
#     validation_feedback: Optional[str]
#     retry_count: int
#     max_retries: int

#     # Workflow Metadata
#     current_step: Optional[str]
#     status: Optional[str]
#     error: Optional[str]




class SubSection(TypedDict):
    SubSectionId: int
    SubSectionName: str
    Summary: str


class Section(TypedDict):
    SectionName: str
    Summary: str
    Purpose: str
    SubSections: List[SubSection]


class WorkflowState(TypedDict):
    # Input Fields
    CompanyId: str
    user_id: str
    user_name: str

    # Constitution / Rules
    global_constitution: str
    company_constitution: Optional[str]
    specification: Optional[str]

    # Section Metadata
    section_names: List[str]

    # Loop Control
    current_section_index: int
    current_section_name: Optional[str]

    # Qdrant Retrieval
    retrieved_chunks: List[Dict[str, Any]]

    # Current Generated Section
    current_generated_section: Optional[Section]

    # Final Output
    generated_sections: List[Section]

    # Validation / Retry
    validation_status: Optional[str]
    validation_feedback: Optional[str]
    retry_count: int
    max_retries: int

    # Workflow Metadata
    current_step: Optional[str]
    status: Optional[str]
    error: Optional[str]