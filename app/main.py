"""FastAPI app exposing the resume <-> job matching agent.

Run with:
    uvicorn app.main:app --reload

Then try:
    curl http://127.0.0.1:8000/candidates/cand-001/matches
    curl http://127.0.0.1:8000/jobs/job-101/matches
    curl -X POST http://127.0.0.1:8000/match \
        -H "Content-Type: application/json" \
        -d '{"resume_id": "cand-001", "job_id": "job-101"}'
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.data import SAMPLE_JOBS, SAMPLE_RESUMES, get_job, get_resume
from app.matcher import rank_jobs_for_resume, rank_resumes_for_job, score_match

app = FastAPI(
    title="Resume-Job Matcher",
    description=(
        "Explainable candidate-to-job matching agent. Scores a candidate "
        "against a job posting and returns a plain-English 'why this fits' "
        "rationale, using sample/synthetic data only."
    ),
    version="0.1.0",
)


class MatchRequest(BaseModel):
    resume_id: str
    job_id: str


@app.get("/")
def root() -> dict:
    return {
        "service": "resume-job-matcher",
        "candidates": [r["id"] for r in SAMPLE_RESUMES],
        "jobs": [j["id"] for j in SAMPLE_JOBS],
        "docs": "/docs",
    }


@app.post("/match")
def match(request: MatchRequest) -> dict:
    resume = get_resume(request.resume_id)
    job = get_job(request.job_id)
    if resume is None:
        raise HTTPException(status_code=404, detail=f"Unknown resume_id: {request.resume_id}")
    if job is None:
        raise HTTPException(status_code=404, detail=f"Unknown job_id: {request.job_id}")
    return score_match(resume, job).to_dict()


@app.get("/candidates/{resume_id}/matches")
def candidate_matches(resume_id: str) -> dict:
    resume = get_resume(resume_id)
    if resume is None:
        raise HTTPException(status_code=404, detail=f"Unknown resume_id: {resume_id}")
    ranked = rank_jobs_for_resume(resume, SAMPLE_JOBS)
    return {"resume_id": resume_id, "ranked_jobs": [r.to_dict() for r in ranked]}


@app.get("/jobs/{job_id}/matches")
def job_matches(job_id: str) -> dict:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Unknown job_id: {job_id}")
    ranked = rank_resumes_for_job(job, SAMPLE_RESUMES)
    return {"job_id": job_id, "ranked_candidates": [r.to_dict() for r in ranked]}
