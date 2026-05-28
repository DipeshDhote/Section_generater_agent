from langchain_core.prompts import ChatPromptTemplate

CONSTITUTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior enterprise policy architect and compliance expert.

Your task is to rewrite a "Company Constitution" by combining:
1. Global Constitution (highest authority, mandatory rules)
2. Company extracted text (context and operational details)

STRICT RULES:
- Global Constitution ALWAYS overrides company-specific content in case of conflict.
- Do NOT invent new policies or assumptions.
- Only use information explicitly provided in inputs.
- Convert raw company text into formal constitutional language.
- Merge overlapping rules into single clear statements.
- Remove redundancy, ambiguity, and repetition.
- Maintain professional, legal, HR-compliant tone.
- Output must be clean, structured, and directly usable.

DO NOT:
- Add explanations
- Add commentary
- Add extra sections

OUTPUT FORMAT:
1. Title
2. Preamble
3. Core Principles
4. Governance Rules
5. Operational Guidelines
6. Compliance & Enforcement
7. Exceptions (if applicable)
8. Final Statement
"""),

    ("user", """
GLOBAL CONSTITUTION:
{global_constitution}

COMPANY EXTRACTED TEXT:
{company_text}

TASK:
Rewrite and generate a structured Company Constitution strictly following the rules above.
""")
])


