from app.graph.nodes.validation_nodes import validate_single_section


def test_validate_single_section_passed():
    state = {
        "current_section_name": "Product Categories",
        "current_generated_section": {
            "SectionName": "Product Categories",
            "Summary": "The company offers industrial conveyor systems.",
            "Purpose": "Shows product capability for tender use.",
            "SubSections": [
                {
                    "SubSectionId": 1,
                    "SubSectionName": "Industrial Conveyor Systems",
                    "Summary": "The company offers industrial conveyor systems."
                }
            ]
        }
    }

    result = validate_single_section(state)

    print(result)

    assert result["validation_status"] == "passed"


def test_validate_single_section_wrong_name():
    state = {
        "current_section_name": "Product Categories",
        "current_generated_section": {
            "SectionName": "Products",
            "Summary": "The company offers industrial conveyor systems.",
            "Purpose": "Shows product capability for tender use.",
            "SubSections": [
                {
                    "SubSectionId": 1,
                    "SubSectionName": "Industrial Conveyor Systems",
                    "Summary": "The company offers industrial conveyor systems."
                }
            ]
        }
    }

    result = validate_single_section(state)

    print(result)

    assert result["validation_status"] == "retry"


def test_validate_single_section_skip():
    state = {
        "current_section_name": "Product Categories",
        "current_generated_section": None
    }

    result = validate_single_section(state)

    print(result)

    assert result["validation_status"] == "skip"