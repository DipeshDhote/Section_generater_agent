from app.graph.nodes.qdrant_nodes import get_chunks_by_current_section


def test_get_chunks_by_current_section():
    state = {
        "CompanyId": "6a13fd50ff7b9a4a1f5dfcb8",
        "current_section_name": "Company Overview"
    }

    result = get_chunks_by_current_section(state)

    print(result)

    assert result["status"] == "running"
    assert result["current_step"] == "section_chunks_loaded"
    assert isinstance(result["retrieved_chunks"], list)
    assert len(result["retrieved_chunks"]) > 0