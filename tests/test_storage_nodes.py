from app.graph.nodes.storage_nodes import store_section_result


def test_store_section_result_passed():
    state = {
        "generated_sections": [],
        "current_generated_section": {
            "SectionName": "Product Categories",
            "Summary": "The company offers industrial machinery products.",
            "Purpose": "Shows product capability for tenders.",
            "SubSections": [
                {
                    "SubSectionId": 1,
                    "SubSectionName": "Industrial Machinery",
                    "Summary": "Includes conveyor systems and automation products."
                }
            ]
        },
        "validation_status": "passed",
        "current_section_index": 0,
    }

    result = store_section_result(state)

    print(result)

    assert len(result["generated_sections"]) == 1
    assert result["generated_sections"][0]["Id"] == 1
    assert "SubSections" in result["generated_sections"][0]
    assert len(result["generated_sections"][0]["SubSections"]) == 1
    assert result["current_section_index"] == 1


def test_store_section_result_skip():
    state = {
        "generated_sections": [],
        "current_generated_section": None,
        "validation_status": "skip",
        "current_section_index": 0,
    }

    result = store_section_result(state)

    print(result)

    assert len(result["generated_sections"]) == 0
    assert result["current_section_index"] == 1