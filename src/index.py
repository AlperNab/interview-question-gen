#!/usr/bin/env python3
"""
interview-question-gen — job description + CV → tailored interview question bank
Generates: behavioral, technical, situational, culture-fit questions with
evaluation rubrics, red flag probes, scorecard template
"""
import anthropic, base64, json, re, sys
from pathlib import Path

SYSTEM = """You are a talent acquisition specialist and interview design expert.
Create a comprehensive, tailored interview question bank based on the role and candidate.

Principles:
- Questions should be specific to THIS role and THIS candidate's background
- Use STAR format prompts for behavioral questions
- Technical questions should test application, not memorization
- Include probes for the specific concerns raised by the CV
- Every question should have a clear evaluation rubric

Return ONLY valid JSON — no markdown, no explanation.

{
  "role": "job title",
  "candidate_name": "string or null",
  "interview_duration_minutes": number,
  "recommended_panel": ["Hiring Manager","Technical Lead","HR","Peer"],
  "opening_question": "warm-up question to start the interview",
  "sections": [
    {
      "section": "Technical|Behavioral|Situational|Culture|CV Deep-Dive|Case Study",
      "duration_minutes": number,
      "questions": [
        {
          "id": "Q1",
          "question": "full question text",
          "follow_up_probes": ["deeper follow-up if answer is shallow"],
          "what_youre_assessing": "the specific competency or signal",
          "strong_answer_includes": ["3-4 signals of a strong answer"],
          "red_flag_signals": ["what would concern you"],
          "scoring_rubric": {
            "1": "Poor — description",
            "2": "Below expectations",
            "3": "Meets expectations",
            "4": "Exceeds expectations",
            "5": "Exceptional — description"
          },
          "weight": number_1_to_3,
          "tailored_to": "why this question fits this specific candidate/role"
        }
      ]
    }
  ],
  "cv_specific_questions": [
    {
      "topic": "specific item from CV to probe",
      "question": "tailored question",
      "what_to_clarify": "what you want to understand better",
      "green_flag": "ideal answer",
      "red_flag": "concerning answer"
    }
  ],
  "closing_questions": [
    "What questions do you have for us?",
    "What would make you choose us over other opportunities?"
  ],
  "scorecard": {
    "dimensions": [
      {
        "dimension": "competency name",
        "weight_pct": number,
        "linked_questions": ["Q1","Q2"],
        "pass_threshold": number_1_to_5
      }
    ],
    "knockout_criteria": ["deal-breaker conditions that auto-reject"],
    "minimum_overall_score": number_1_to_5
  },
  "debrief_guide": {
    "key_questions_for_panel": ["what did each panelist think of X?"],
    "consensus_check": "how to resolve disagreements",
    "timeline": "decision and feedback within X business days"
  },
  "legal_notes": ["questions to AVOID — potentially discriminatory"],
  "confidence": 0.0
}"""

def read_doc(source: str, label: str) -> list:
    path = Path(source)
    if path.exists():
        if str(source).endswith(".pdf"):
            data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
            return [
                {"type":"document","source":{"type":"base64","media_type":"application/pdf","data":data}},
                {"type":"text","text":f"[This is the {label} above]"}
            ]
        text = path.read_text(encoding="utf-8",errors="replace")[:15000]
        return [{"type":"text","text":f"{label}:\n{text}"}]
    return [{"type":"text","text":f"{label}:\n{source[:15000]}"}]

def generate(jd_source: str, cv_source: str = "", duration: int = 60, panel_size: int = 2) -> dict:
    client = anthropic.Anthropic()

    content = read_doc(jd_source, "JOB DESCRIPTION")
    if cv_source:
        content.append({"type":"text","text":"\n---\n"})
        content.extend(read_doc(cv_source, "CANDIDATE CV"))

    content.append({"type":"text","text":f"\n\nInterview duration: {duration} minutes. Panel size: {panel_size} interviewers.\n\nGenerate a comprehensive tailored interview question bank."})

    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":content}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def to_markdown(r: dict) -> str:
    lines = [
        f"# Interview Question Bank — {r.get('role','')}",
        f"**Candidate:** {r.get('candidate_name','?')} | **Duration:** {r.get('interview_duration_minutes','?')} min",
        f"**Panel:** {', '.join(r.get('recommended_panel',[]))}",
        "",
        f"**Opening:** *{r.get('opening_question','')}*",
        "",
    ]
    for section in r.get("sections",[]):
        lines += [f"\n## {section.get('section','')} ({section.get('duration_minutes','?')} min)\n"]
        for q in section.get("questions",[]):
            lines += [
                f"### {q.get('id','')} — {q.get('what_youre_assessing','')} (weight: {q.get('weight',1)}/3)",
                "",
                f"**Q:** {q.get('question','')}",
                "",
            ]
            probes = q.get("follow_up_probes",[])
            if probes:
                lines.append("**Follow-ups:**")
                for p in probes: lines.append(f"- {p}")
                lines.append("")
            strong = q.get("strong_answer_includes",[])
            if strong:
                lines.append("**Strong answer includes:**")
                for s in strong: lines.append(f"- ✓ {s}")
                lines.append("")
            red = q.get("red_flag_signals",[])
            if red:
                lines.append("**Red flags:**")
                for rf in red: lines.append(f"- ⚠ {rf}")
                lines.append("")

    cv_qs = r.get("cv_specific_questions",[])
    if cv_qs:
        lines += ["\n## CV Deep-Dive Questions\n"]
        for q in cv_qs:
            lines += [
                f"**Topic:** {q.get('topic','')}",
                f"**Q:** {q.get('question','')}",
                f"**Clarify:** {q.get('what_to_clarify','')}",
                f"✓ Green: {q.get('green_flag','')}",
                f"⚠ Red: {q.get('red_flag','')}",
                "",
            ]

    scorecard = r.get("scorecard",{})
    if scorecard.get("dimensions"):
        lines += ["\n## Scorecard\n","| Dimension | Weight | Questions | Pass Threshold |","|-|-|-|-|"]
        for d in scorecard["dimensions"]:
            qs = ", ".join(d.get("linked_questions",[]))
            lines.append(f"| {d.get('dimension','')} | {d.get('weight_pct',0)}% | {qs} | {d.get('pass_threshold',3)}/5 |")

    legal = r.get("legal_notes",[])
    if legal:
        lines += ["\n## ⚠ Do NOT Ask\n"]
        for note in legal: lines.append(f"- {note}")

    return "\n".join(lines)

def print_questions(r: dict):
    sections = r.get("sections",[])
    total_q = sum(len(s.get("questions",[])) for s in sections) + len(r.get("cv_specific_questions",[]))

    print(f"\n{'═'*60}")
    print(f"  INTERVIEW QUESTIONS — {r.get('role','?')}")
    print(f"  {total_q} questions | {r.get('interview_duration_minutes','?')} min | Panel: {', '.join(r.get('recommended_panel',[]))}")
    print(f"{'═'*60}")
    print(f"\n  Opening: \"{r.get('opening_question','')}\"")

    for section in sections:
        qs = section.get("questions",[])
        print(f"\n{'─'*60}")
        print(f"  {section.get('section','?').upper()} — {len(qs)} questions ({section.get('duration_minutes','?')} min)")
        for q in qs:
            weight_bar = "●"*q.get("weight",1) + "○"*(3-q.get("weight",1))
            print(f"\n  [{q.get('id','')}] {weight_bar} {q.get('what_youre_assessing','')}")
            print(f"  Q: {q.get('question','')[:120]}")
            probes = q.get("follow_up_probes",[])
            if probes: print(f"     ↳ {probes[0][:80]}")
            strong = q.get("strong_answer_includes",[])
            if strong: print(f"     ✓ {strong[0]}")
            red = q.get("red_flag_signals",[])
            if red: print(f"     ⚠ {red[0]}")

    cv_qs = r.get("cv_specific_questions",[])
    if cv_qs:
        print(f"\n{'─'*60}")
        print(f"  CV DEEP-DIVE ({len(cv_qs)} questions)")
        for q in cv_qs:
            print(f"\n  Topic: {q.get('topic','')}")
            print(f"  Q: {q.get('question','')[:120]}")

    legal = r.get("legal_notes",[])
    if legal:
        print(f"\n  ⚠ DO NOT ASK: {' | '.join(legal[:3])}")

    print(f"\n  Confidence: {int(r.get('confidence',0)*100)}%")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate tailored interview questions from JD and CV")
    p.add_argument("jd", help="Job description file or text")
    p.add_argument("cv", nargs="?", default="", help="Candidate CV file (optional)")
    p.add_argument("--duration","-d",type=int,default=60,help="Interview duration minutes")
    p.add_argument("--panel",type=int,default=2,help="Number of interviewers")
    p.add_argument("--json",action="store_true")
    p.add_argument("--markdown","-m",help="Save full question bank as markdown")
    a = p.parse_args()
    r = generate(a.jd, a.cv, a.duration, a.panel)
    if a.markdown:
        Path(a.markdown).write_text(to_markdown(r),encoding="utf-8")
        print(f"Question bank saved to {a.markdown}")
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_questions(r)
