# Specification File: Company Profile Section JSON Output

## 1. Objective

This Specification defines the required JSON output format for company profile section generation.

The AI agent must analyse the provided company profile information and return a valid JSON array containing only eligible company profile sections.

The Constitution File controls which sections are allowed and when a section may be generated.

This Specification controls how the output must be structured.

---

## 2. Critical Template Rule

Any sample template is only an example of JSON shape.

The AI agent must not treat example section names as fixed output.

For example, if a sample includes only:

- Company Overview
- Services
- Infrastructure

the AI agent must not limit the output to those three sections.

The AI agent must dynamically generate all eligible sections from the approved section list in the Constitution File.

---

## 3. Required Output Format

The final output must be a valid JSON array only.

The AI agent must not return:

- Markdown
- Explanation before JSON
- Explanation after JSON
- Code block wrapper
- Comments
- Invalid JSON
- Trailing commas
- Skipped sections

The output must follow this structure:

[
  {
    "Id": 1,
    "SectionName": "Approved Section Name",
    "Summary": "Tender-ready summary generated from the provided company profile information only.",
    "Purpose": "Explains why this section is useful for tender proposal generation."
  }
]

---

## 4. Field Rules

### 4.1 Id

The `Id` field must:

- Start from 1.
- Increase sequentially by 1.
- Follow the order of sections as listed in the Constitution File.
- Not skip numbers.
- Be numeric, not a string.

Example:

{
  "Id": 1
}

---

### 4.2 SectionName

The `SectionName` field must:

- Use only an approved section name from the Constitution File.
- Use the exact approved section name.
- Not use invented headings.
- Not copy arbitrary source headings unless they match an approved section.
- Not use simplified names if the Constitution uses a more specific name.

Examples:

- Use `Core Services / Offerings`, not `Services`.
- Use `Tools, Systems and Infrastructure`, not `Infrastructure`.
- Use `Information Security and Data Protection`, not `Security`.
- Use `Relevant Experience / Case Studies`, not `Projects`.

---

### 4.3 Summary

The `Summary` field must:

- Contain the generated company profile content for that section.
- Be based only on the provided company profile information.
- Be written in professional tender-ready language.
- Be concise but meaningful.
- Avoid assumptions, exaggeration, unsupported claims, and generic filler.
- Not include placeholders.
- Not state that information is missing.

The `Summary` field must not contain:

- Fake certifications
- Fake client names
- Fake financial details
- Fake years of experience
- Fake case studies
- Unsupported outcomes
- Unsupported metrics
- Unsupported technologies
- Unsupported compliance claims

---

### 4.4 Purpose

The `Purpose` field must:

- Explain the tender relevance of the section.
- Be generic but meaningful.
- Explain why the section helps in proposal generation.
- Not introduce new company facts.
- Not include unsupported claims.

Example:

{
  "Purpose": "Demonstrates the company's service capability and helps align its offerings with tender requirements."
}

---

## 5. Section Name Normalisation

The AI agent may detect synonyms or similar headings in the source content, but the final `SectionName` must use the approved Constitution section name.

| Source Text May Say | Output SectionName Must Be |
|---------------------|----------------------------|
| Services            | Core Services / Offerings  |
| Solutions           | Core Services / Offerings  |
| Products            | Products / Platforms       |
| Technology Stack    | Technical Expertise        |
| Infrastructure      | Tools, Systems and Infrastructure  |
| Clients             | Client Portfolio                   |
| Projects            | Relevant Experience / Case Studies |
| Case Work           | Relevant Experience / Case Studies |
| Security            | Information Security and Data Protection |
| Delivery Model      | Methodology / Delivery Approach  |
| Governance          | Project Management Approach      |
| Social Impact       | Social Value                     |
| Support             | Support and Maintenance Approach |
| Training            | Training and Knowledge Transfer  |

---

## 6. Dynamic Section Generation Rule

The AI agent must evaluate every approved section in the Constitution File.

The final JSON may contain any number of sections depending on the available information.

Examples:

- If only company overview information exists, return only `Company Overview`.
- If services, products, team, case studies, security, and compliance are provided, return all supported sections.
- If infrastructure information is not provided, do not return `Tools, Systems and Infrastructure`.
- If certification information is not provided, do not return `Certifications and Accreditations`.

The AI agent must not restrict output to sample template sections.

---

## 7. Section Ordering Rule

Generated sections must follow the same order as the approved section list in the Constitution File.

Do not order sections based on the source document order if it conflicts with the Constitution order.

The `Id` field must be assigned after unsupported sections are removed.

Example:

If only these sections are eligible:

- Company Overview
- Products / Platforms
- Technical Expertise

The output IDs must be:

1. Company Overview
2. Products / Platforms
3. Technical Expertise

---

## 8. Correct Output Example

This is an example of structure only.

The final output must use actual company profile information.

[
  {
    "Id": 1,
    "SectionName": "Company Overview",
    "Summary": "...",
    "Purpose": "...",
    "SubSections": [
      {
        "SubSectionId": 1,
        "SubSectionName": "Company Background",
        "Summary": "..."
      },
      {
        "SubSectionId": 2,
        "SubSectionName": "Business Focus",
        "Summary": "..."
      }
    ]
  }
]

---

## 9. Incorrect Output Pattern

The AI agent must not return a fixed object such as:

{
  "CompanyOverview": {
    "Points": []
  },
  "Services": {
    "Points": []
  },
  "Infrastructure": {
    "Points": []
  }
}

This is incorrect because:

- It fixes the output to three sections.
- It prevents dynamic section generation.
- It does not use the approved section names from the Constitution File.
- It creates empty sections, which are not allowed.
- It does not follow the required JSON array format.

---

## 10. Validation Checklist

Before returning the final JSON, the AI agent must verify:

- The output is valid JSON.
- The output is a JSON array.
- Every main section object contains exactly these keys:
  - `Id`
  - `SectionName`
  - `Summary`
  - `Purpose`
  - `SubSections`
- `SubSections` is a JSON array.
- Every subsection object contains exactly these keys:
  - `SubSectionId`
  - `SubSectionName`
  - `Summary`
- All `Id` values are sequential.
- All `SubSectionId` values are sequential within their parent section.
- Every `SectionName` is approved by the Constitution File.
- Every `Summary` is based only on provided company profile information.
- Unsupported sections are excluded.
- Empty sections are excluded.
- Empty subsections are excluded.
- No assumptions or hallucinations are included.
- No Markdown or explanatory text appears outside the JSON.

---

## 11. Final Response Rule

Return only the JSON array.

Do not include Markdown.

Do not include explanations.

Do not include skipped sections.

Do not include notes.

Do not include comments.

Do not wrap the JSON in a code block.
