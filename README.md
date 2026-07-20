# Resume-Job Matcher

An explainable candidate-to-job matching agent. Given a candidate's resume
and a job posting, it produces a numeric fit score **and** a plain-English
"why this fits" rationale: which required skills matched, which are missing,
which nice-to-have skills the candidate brings, and how their experience
compares to the role's requirement.

## Why this is relevant

Recruiting and talent-matching is one of the most common applied-AI patterns
showing up right now — "agent reads a resume, agent reads a job description,
agent tells you if it's a fit and why." This project builds a minimal,
fully-working version of that pattern:

- **No black box.** The score is a transparent, weighted combination of
  required-skill overlap, nice-to-have overlap, and experience fit — every
  number in the output can be traced back to a specific rule.
- **No external dependencies required to run the core logic.** The matching
  engine (`app/matcher.py`) is pure Python standard library, so it runs
  anywhere with zero API keys, embeddings, or network calls.
- **A small FastAPI layer on top** demonstrates how this kind of logic gets
  exposed as a service in a real agentic pipeline (e.g. a tool an LLM agent
  could call via MCP or function-calling).

## What's inside

- `app/data.py` — synthetic sample resumes and job postings (all fabricated
  for this demo; no real people or companies).
- `app/matcher.py` — the scoring + rationale engine.
- `app/main.py` — FastAPI app exposing `/match`, `/candidates/{id}/matches`,
  and `/jobs/{id}/matches`.
- `tests/test_matcher.py` — unit tests covering strong matches, weak matches,
  missing-skill reporting, experience-gap reporting, and ranking.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Then, in another terminal:

```bash
# Score one candidate against one job
curl -X POST http://127.0.0.1:8000/match \
  -H "Content-Type: application/json" \
  -d '{"resume_id": "cand-001", "job_id": "job-101"}'

# Rank all sample jobs for a given candidate
curl http://127.0.0.1:8000/candidates/cand-001/matches

# Rank all sample candidates for a given job
curl http://127.0.0.1:8000/jobs/job-101/matches
```

Example response from `/match`:

```json
{
  "resume_id": "cand-001",
  "job_id": "job-101",
  "score": 100.0,
  "matched_required": ["postgresql", "python", "rest apis"],
  "matched_nice_to_have": ["aws", "docker", "fastapi"],
  "missing_required": [],
  "years_experience": 4,
  "min_years_required": 3,
  "rationale": "Asha Rao scores 100.0/100 for the 'Backend Engineer (Python)' role. Matches required skills: postgresql, python, rest apis. Also brings nice-to-have skills: aws, docker, fastapi. Meets the experience bar (4 yrs vs. 3 yrs required)."
}
```

(This is the actual output produced by running the example above — verified, not fabricated.)

You can also explore the API interactively at `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest -v
```

## Disclaimer

This is a demo project using entirely synthetic data for illustration. It is
not a production hiring tool, is not validated for fairness or bias, and
should not be used to make real hiring or employment decisions.
