"""Synthetic sample data: candidate resumes and job postings.

All data here is fabricated for demo purposes only — no real people or
companies. This lets the whole project run end-to-end with zero external
API keys or network calls.
"""
from __future__ import annotations

from typing import TypedDict


class Resume(TypedDict):
    id: str
    name: str
    skills: list[str]
    years_experience: int
    summary: str


class JobPosting(TypedDict):
    id: str
    title: str
    required_skills: list[str]
    nice_to_have_skills: list[str]
    min_years_experience: int
    description: str


SAMPLE_RESUMES: list[Resume] = [
    {
        "id": "cand-001",
        "name": "Asha Rao",
        "skills": ["python", "fastapi", "postgresql", "docker", "aws", "rest apis"],
        "years_experience": 4,
        "summary": (
            "Backend engineer who has spent the last four years building "
            "REST APIs and data pipelines in Python, deploying on AWS with "
            "Docker, and tuning PostgreSQL for high write throughput."
        ),
    },
    {
        "id": "cand-002",
        "name": "Marcus Lee",
        "skills": ["javascript", "react", "typescript", "node.js", "graphql", "css"],
        "years_experience": 3,
        "summary": (
            "Frontend-leaning full-stack developer focused on React and "
            "TypeScript, with three years building customer-facing "
            "dashboards and GraphQL APIs."
        ),
    },
    {
        "id": "cand-003",
        "name": "Priya Nair",
        "skills": ["python", "pytorch", "nlp", "langchain", "vector databases", "docker"],
        "years_experience": 2,
        "summary": (
            "Machine learning engineer with two years of experience building "
            "NLP pipelines and retrieval-augmented generation systems using "
            "PyTorch, LangChain, and vector databases."
        ),
    },
    {
        "id": "cand-004",
        "name": "David Kim",
        "skills": ["java", "spring boot", "kafka", "kubernetes", "aws", "microservices"],
        "years_experience": 6,
        "summary": (
            "Senior backend engineer with six years designing distributed "
            "microservices in Java/Spring Boot, running on Kubernetes with "
            "Kafka for event streaming."
        ),
    },
]

SAMPLE_JOBS: list[JobPosting] = [
    {
        "id": "job-101",
        "title": "Backend Engineer (Python)",
        "required_skills": ["python", "rest apis", "postgresql"],
        "nice_to_have_skills": ["docker", "aws", "fastapi"],
        "min_years_experience": 3,
        "description": (
            "We're looking for a backend engineer to build and scale REST "
            "APIs in Python, backed by PostgreSQL, deployed on AWS."
        ),
    },
    {
        "id": "job-102",
        "title": "ML Engineer, Applied NLP",
        "required_skills": ["python", "nlp", "pytorch"],
        "nice_to_have_skills": ["langchain", "vector databases", "docker"],
        "min_years_experience": 1,
        "description": (
            "Join our applied AI team building retrieval-augmented "
            "generation systems and NLP pipelines with PyTorch."
        ),
    },
    {
        "id": "job-103",
        "title": "Frontend Engineer (React)",
        "required_skills": ["javascript", "react", "css"],
        "nice_to_have_skills": ["typescript", "graphql"],
        "min_years_experience": 2,
        "description": (
            "Build customer-facing dashboards in React and TypeScript, "
            "working closely with design and product."
        ),
    },
    {
        "id": "job-104",
        "title": "Senior Distributed Systems Engineer",
        "required_skills": ["java", "kafka", "kubernetes"],
        "nice_to_have_skills": ["spring boot", "aws", "microservices"],
        "min_years_experience": 5,
        "description": (
            "Own core distributed infrastructure services handling "
            "event streaming and microservice orchestration at scale."
        ),
    },
]


def get_resume(resume_id: str) -> Resume | None:
    return next((r for r in SAMPLE_RESUMES if r["id"] == resume_id), None)


def get_job(job_id: str) -> JobPosting | None:
    return next((j for j in SAMPLE_JOBS if j["id"] == job_id), None)
