from app.graph.nodes.qdrant_nodes import get_available_sections_from_qdrant


def test_get_available_sections_from_qdrant():
    state = {
        "CompanyId": "6a13fd50ff7b9a4a1f5dfcb8"
    }

    result = get_available_sections_from_qdrant(state)

    print(result)

    assert result["status"] == "running"
    assert result["current_step"] == "available_sections_loaded"
    assert isinstance(result["section_names"], list)
    assert len(result["section_names"]) > 0