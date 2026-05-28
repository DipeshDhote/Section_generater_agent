from app.services.qdrant_service import QdrantService


def test_get_unique_section_names_by_company_id():
    service = QdrantService()

    result = service.get_unique_section_names_by_company_id(
        CompanyId="6a13fd50ff7b9a4a1f5dfcb8"
    )

    print(result)

    assert isinstance(result, list)
    assert len(result) > 0