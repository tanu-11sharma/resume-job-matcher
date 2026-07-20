from app.data import get_job, get_resume
from app.matcher import rank_jobs_for_resume, rank_resumes_for_job, score_match


def test_strong_match_scores_high():
    resume = get_resume("cand-001")  # backend/Python candidate
    job = get_job("job-101")  # Backend Engineer (Python)
    result = score_match(resume, job)

    assert result.score > 80
    assert "python" in result.matched_required
    assert "postgresql" in result.matched_required
    assert result.missing_required == []
    assert "docker" in result.matched_nice_to_have


def test_weak_match_scores_low_and_lists_missing_skills():
    resume = get_resume("cand-002")  # frontend candidate
    job = get_job("job-104")  # Senior Distributed Systems Engineer (Java/Kafka)
    result = score_match(resume, job)

    assert result.score < 40
    assert set(result.missing_required) == {"java", "kafka", "kubernetes"}
    assert result.matched_required == []


def test_rationale_mentions_candidate_name_and_role():
    resume = get_resume("cand-003")
    job = get_job("job-102")
    result = score_match(resume, job)

    assert resume["name"] in result.rationale
    assert job["title"] in result.rationale


def test_experience_below_bar_is_reflected_in_rationale():
    resume = get_resume("cand-003")  # 2 years experience
    job = get_job("job-104")  # requires 5 years
    result = score_match(resume, job)

    assert "Below the experience bar" in result.rationale


def test_rank_jobs_for_resume_orders_best_fit_first():
    resume = get_resume("cand-001")
    ranked = rank_jobs_for_resume(resume, [get_job(j) for j in ["job-101", "job-103", "job-104"]])

    scores = [r.score for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0].job_id == "job-101"


def test_rank_resumes_for_job_orders_best_fit_first():
    job = get_job("job-102")
    candidates = [get_resume(c) for c in ["cand-001", "cand-002", "cand-003", "cand-004"]]
    ranked = rank_resumes_for_job(job, candidates)

    scores = [r.score for r in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0].resume_id == "cand-003"


def test_unknown_ids_return_none():
    assert get_resume("does-not-exist") is None
    assert get_job("does-not-exist") is None
