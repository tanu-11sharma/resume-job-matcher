"""Core candidate <-> job matching logic.

The matcher is deliberately dependency-light (pure standard library) so the
project runs anywhere without needing embeddings, API keys, or network
access. It combines:

  1. Skill overlap (required + nice-to-have) scored via weighted Jaccard-style
     overlap on normalized skill sets.
  2. An experience-fit adjustment based on minimum years required.

The output is a MatchResult with a numeric score (0-100) and a plain-English
"why this fits" rationale listing matched required skills, matched
nice-to-have skills, missing required skills, and the experience comparison.
This mirrors the "explainable AI matching" pattern trending in recruiting-tech
agent demos, without calling any external LLM.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from app.data import JobPosting, Resume


def _normalize(skills: list[str]) -> set[str]:
    return {s.strip().lower() for s in skills if s.strip()}


@dataclass
class MatchResult:
    resume_id: str
    job_id: str
    score: float
    matched_required: list[str] = field(default_factory=list)
    matched_nice_to_have: list[str] = field(default_factory=list)
    missing_required: list[str] = field(default_factory=list)
    years_experience: int = 0
    min_years_required: int = 0
    rationale: str = ""

    def to_dict(self) -> dict:
        return {
            "resume_id": self.resume_id,
            "job_id": self.job_id,
            "score": self.score,
            "matched_required": self.matched_required,
            "matched_nice_to_have": self.matched_nice_to_have,
            "missing_required": self.missing_required,
            "years_experience": self.years_experience,
            "min_years_required": self.min_years_required,
            "rationale": self.rationale,
        }


# Weights: required skills matter most, nice-to-have skills add a smaller
# bonus, and experience fit nudges the score up or down slightly.
REQUIRED_SKILL_WEIGHT = 70.0
NICE_TO_HAVE_WEIGHT = 20.0
EXPERIENCE_WEIGHT = 10.0


def score_match(resume: Resume, job: JobPosting) -> MatchResult:
    candidate_skills = _normalize(resume["skills"])
    required = _normalize(job["required_skills"])
    nice_to_have = _normalize(job["nice_to_have_skills"])

    matched_required = sorted(candidate_skills & required)
    missing_required = sorted(required - candidate_skills)
    matched_nice = sorted(candidate_skills & nice_to_have)

    required_ratio = (len(matched_required) / len(required)) if required else 1.0
    nice_ratio = (len(matched_nice) / len(nice_to_have)) if nice_to_have else 0.0

    years = resume["years_experience"]
    min_years = job["min_years_experience"]
    if min_years <= 0:
        experience_ratio = 1.0
    else:
        experience_ratio = min(years / min_years, 1.25) / 1.25  # cap bonus for overqualification

    score = (
        required_ratio * REQUIRED_SKILL_WEIGHT
        + nice_ratio * NICE_TO_HAVE_WEIGHT
        + experience_ratio * EXPERIENCE_WEIGHT
    )
    score = round(min(score, 100.0), 1)

    rationale = _build_rationale(
        resume=resume,
        job=job,
        matched_required=matched_required,
        matched_nice=matched_nice,
        missing_required=missing_required,
        years=years,
        min_years=min_years,
        score=score,
    )

    return MatchResult(
        resume_id=resume["id"],
        job_id=job["id"],
        score=score,
        matched_required=matched_required,
        matched_nice_to_have=matched_nice,
        missing_required=missing_required,
        years_experience=years,
        min_years_required=min_years,
        rationale=rationale,
    )


def _build_rationale(
    *,
    resume: Resume,
    job: JobPosting,
    matched_required: list[str],
    matched_nice: list[str],
    missing_required: list[str],
    years: int,
    min_years: int,
    score: float,
) -> str:
    parts: list[str] = []
    parts.append(f"{resume['name']} scores {score}/100 for the '{job['title']}' role.")

    if matched_required:
        parts.append(
            "Matches required skills: " + ", ".join(matched_required) + "."
        )
    else:
        parts.append("Matches none of the required skills.")

    if missing_required:
        parts.append("Missing required skills: " + ", ".join(missing_required) + ".")

    if matched_nice:
        parts.append("Also brings nice-to-have skills: " + ", ".join(matched_nice) + ".")

    if years >= min_years:
        parts.append(
            f"Meets the experience bar ({years} yrs vs. {min_years} yrs required)."
        )
    else:
        parts.append(
            f"Below the experience bar ({years} yrs vs. {min_years} yrs required)."
        )

    return " ".join(parts)


def rank_jobs_for_resume(resume: Resume, jobs: list[JobPosting]) -> list[MatchResult]:
    """Return jobs ranked best-fit first for a given candidate."""
    results = [score_match(resume, job) for job in jobs]
    return sorted(results, key=lambda r: r.score, reverse=True)


def rank_resumes_for_job(job: JobPosting, resumes: list[Resume]) -> list[MatchResult]:
    """Return candidates ranked best-fit first for a given job."""
    results = [score_match(resume, job) for resume in resumes]
    return sorted(results, key=lambda r: r.score, reverse=True)
