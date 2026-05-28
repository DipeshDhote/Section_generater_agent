from typing import Optional, List
from pydantic import BaseModel


class SectionGenerateRequest(BaseModel):
    CompanyId: str
    user_id: str
    user_name: str
    max_retries: int = 2


class GeneratedSubSection(BaseModel):
    SubSectionId: int
    SubSectionName: str
    Summary: str


class GeneratedSection(BaseModel):
    Id: int
    SectionName: str
    Summary: str
    Purpose: str
    SubSections: List[GeneratedSubSection]


class SectionGenerateResponse(BaseModel):
    status: str
    company_id: str
    total_sections: int
    generated_sections: List[GeneratedSection]
    error: Optional[str] = None