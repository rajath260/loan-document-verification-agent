"""Tests for the first document-verification milestone."""

from app.graph import build_graph


def run_application(application_id: str) -> dict:
    return build_graph().invoke({"application_id": application_id, "findings": []})


def test_complete_application_is_routed_for_review_ready_summary():
    result = run_application("APP-1001")
    assert result["review_route"] == "REVIEW_READY"
    assert "not a loan approval" in result["final_summary"]


def test_incomplete_or_inconsistent_application_goes_to_manual_review():
    result = run_application("APP-1002")
    assert result["review_route"] == "MANUAL_REVIEW"
    assert result["missing_documents"]
    assert any("mismatch" in item.lower() for item in result["findings"])


def test_unknown_application_is_not_silently_approved():
    result = run_application("UNKNOWN")
    assert result["review_route"] == "MANUAL_REVIEW"
