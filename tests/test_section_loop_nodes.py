from app.graph.nodes.section_loop_nodes import (
    init_section_loop,
    get_next_section,
)


def test_init_section_loop():
    state = {
        "section_names": ["Company Overview", "Product Categories"],
        "current_section_index": 5,
        "generated_sections": [{"SectionName": "Old"}],
    }

    result = init_section_loop(state)

    assert result["current_section_index"] == 0
    assert result["generated_sections"] == []
    assert result["current_step"] == "section_loop_initialized"


def test_get_next_section():
    state = {
        "section_names": ["Company Overview", "Product Categories"],
        "current_section_index": 0,
    }

    result = get_next_section(state)

    print(result)

    assert result["current_section_name"] == "Company Overview"
    assert result["retry_count"] == 0
    assert result["current_step"] == "current_section_selected"


def test_get_next_section_when_done():
    state = {
        "section_names": ["Company Overview"],
        "current_section_index": 1,
    }

    result = get_next_section(state)

    print(result)

    assert result["current_section_name"] is None
    assert result["current_step"] == "no_more_sections"