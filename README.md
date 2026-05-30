# Interview Question Gen

This folder has been upgraded into a **standalone real GUI project**.

Run the project GUI:

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default local URL: `http://127.0.0.1:9127`

This project includes its own FastAPI backend, browser GUI, provider settings, local/cloud LLM routing, encrypted API-key storage, file uploads, job history, exports, and a project-specific plugin configuration.

See `PROJECT_IMPLEMENTATION.md` and `project_config.json` for the applied project-specific features and customization controls.

---

## Original README

# interview-question-gen

> **Job description + CV → complete tailored interview question bank.** Behavioral, technical, situational questions with evaluation rubrics, scorecard, red flag probes, legal notes. Exports to Markdown.

[![PyPI](https://img.shields.io/pypi/v/interview-question-gen?style=flat)](https://pypi.org/project/interview-question-gen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install interview-question-gen

# From JD only
python -m interview_question_gen job_description.txt --markdown questions.md

# With candidate CV for tailored questions
python -m interview_question_gen job_description.txt candidate_cv.pdf --markdown questions.md

# 90-minute panel of 3
python -m interview_question_gen jd.txt cv.pdf --duration 90 --panel 3
```

## What's generated

- **Tailored questions** — specific to this role AND this candidate's background
- **5-point rubric** per question — exactly what poor vs exceptional looks like
- **Follow-up probes** — for when the first answer is shallow
- **CV deep-dive** — questions targeting specific items on the CV to verify
- **Weighted scorecard** — dimensions, weights, pass thresholds
- **Knockout criteria** — automatic rejections
- **Legal notes** — questions to avoid (discriminatory)
- **Debrief guide** — how to run the post-interview panel discussion

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
