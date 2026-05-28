from langchain_core.prompts import ChatPromptTemplate


CONSTITUTION_REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Company Constitution Planning Agent.

OBJECTIVE:
Create a company-specific constitution using:
1. Global Constitution
2. Available section names discovered from Qdrant metadata

The generated constitution will later be used for:
- section-wise Qdrant retrieval
- section generation
- validation
- skip logic

SECTION SELECTION RULES:

1. If a section exists in BOTH:
   - Global Constitution
   - Available Section Names

   Then:
   - Include it as a Standard Section.

2. If a section exists in:
   - Available Section Names
   BUT NOT in Global Constitution

   Then:
   - Include it as a Discovered Section.

3. If a section exists in:
   - Global Constitution
   BUT NOT in Available Section Names

   Then:
   - Do NOT include it.

STRICT RULES:

- Do not invent sections.
- Do not hallucinate sections.
- Every included section MUST exist in Available Section Names.
- Preserve Global Constitution order for Standard Sections.
- Add Discovered Sections after Standard Sections.
- Return markdown only.
- Do not return JSON.
- Do not add explanations outside the constitution.
- Do not include commentary.
- Do not include metadata.
- Do not generate empty sections.

MANDATORY SECTION STRUCTURE:

Every section MUST contain EXACTLY:

1. Purpose
2. Generation Rule
3. Skip Rule

OUTPUT FORMAT:

# Company Constitution

## Standard Sections

### Section: <Section Name>

Purpose:
Explain what this section should contain.

Generation Rule:
Generate this section ONLY using Qdrant chunks
where section_name equals "<Section Name>".

Skip Rule:
Skip this section if insufficient evidence exists.

---

## Discovered Sections

### Section: <Section Name>

Purpose:
Explain what this discovered section should contain
based on its section name.

Generation Rule:
Generate this section ONLY using Qdrant chunks
where section_name equals "<Section Name>".

Skip Rule:
Skip this section if insufficient evidence exists.
"""
    ),
    (
        "user",
        """
GLOBAL CONSTITUTION:
{global_constitution}

AVAILABLE SECTION NAMES:
{section_names}

Create the company-specific constitution.
"""
    )
])