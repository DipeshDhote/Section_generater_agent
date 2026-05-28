from app.graph.nodes.constitution_nodes import (
    rewrite_company_constitution
)

def test_rewrite_company_constitution():
    state = {
        "global_constitution": """
1. Company Overview
2. Product Categories
3. Certifications
4. Infrastructure
""",
        "section_names": [
            "Company Overview",
            "Product Categories",
            "Manufacturing Units"
        ]
    }

    result = rewrite_company_constitution(state)

    print(result["company_constitution"])

    assert result["status"] == "running"
    assert "# Company Constitution" in result["company_constitution"]
    assert "Company Overview" in result["company_constitution"]
    assert "Product Categories" in result["company_constitution"]
    assert "Manufacturing Units" in result["company_constitution"]
    assert "Skip Rule" in result["company_constitution"]