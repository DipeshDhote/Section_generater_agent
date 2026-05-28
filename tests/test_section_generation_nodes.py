from app.graph.nodes.section_generation_nodes import generate_single_section


def test_generate_single_section():
    state = {
        "current_section_name": "Product Categories",
        "company_constitution": """
### Section: Product Categories

Purpose:
This section should outline the primary product categories offered by the company.

Generation Rule:
Generate this section ONLY using Qdrant chunks where section_name equals "Product Categories".

Skip Rule:
Skip this section if insufficient evidence exists.
""",
        "specification": """
Return only one JSON object with exactly:
SectionName, Summary, Purpose, SubSections.

SubSections must be a JSON array.

Each SubSections object must contain exactly:
SubSectionId, SubSectionName, Summary.
""",
        "retrieved_chunks": [
            {
                "Text": "Industrial conveyor systems - CNC machinery components - Hydraulic and pneumatic equipment - Smart robotic assembly systems - Industrial automation controllers - Heavy-duty steel fabrication components - Precision engineering parts - Warehouse automation systems"
            }
        ],
        "validation_feedback": None,
    }

    result = generate_single_section(state)

    print(result)

    assert result["status"] == "running"
    assert result["current_step"] == "single_section_generated"

    section = result["current_generated_section"]

    assert section["SectionName"] == "Product Categories"
    assert "Summary" in section
    assert "Purpose" in section
    assert "SubSections" in section
    assert isinstance(section["SubSections"], list)

    for subsection in section["SubSections"]:
        assert "SubSectionId" in subsection
        assert "SubSectionName" in subsection
        assert "Summary" in subsection