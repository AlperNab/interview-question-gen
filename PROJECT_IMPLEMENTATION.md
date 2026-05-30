# Interview Question Gen — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9127`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/interview-question-gen.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `HR / Interviewing`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Role/JD → interview kit
- Suite: `HR & Recruiting Suite`

## Deep features applied

- competency matrix
- behavioral/technical questions
- scoring rubric
- follow-ups
- anti-bias guardrails
- panel plan
- answer guide

## Customization controls

- `execution_mode` — Execution mode (select)
- `role` — role (select)
- `seniority` — seniority (select)
- `interview_round` — interview round (text)
- `skill_focus` — skill focus (text)
- `question_difficulty` — question difficulty (text)
- `company_values` — company values (text)
- `scoring_style` — scoring style (select)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `role` — Role (select) required
- `jd` — JD (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Talent Ops Workspace** pattern.

**UX workflow:** Role/person intake → scoring → workflow stage → document/interview package

**Domain components:**
- Candidate/role profile
- Scorecard grid
- Pipeline stage board
- Interview kit
- Compliance and tone panel

**Quick actions:**
- Build scorecard
- Generate interview kit
- Review compensation/doc terms
- Create follow-up actions

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
