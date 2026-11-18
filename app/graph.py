"""LangGraph workflow for a fictional document verification process."""

from langgraph.graph import END, START, StateGraph

from app.mock_documents import SAMPLE_APPLICATIONS
from app.state import LoanState

REQUIRED_DOCUMENTS = {"identity_document", "salary_slip", "bank_statement"}


def ingest_documents(state: LoanState) -> dict:
    """Load a synthetic application's document inventory."""
    application_id = state["application_id"]
    application = SAMPLE_APPLICATIONS.get(application_id)
    if application is None:
        return {
            "documents": [],
            "extracted_data": {},
            "findings": ["Application was not found in the synthetic dataset."],
        }
    return {
        "documents": application["documents"],
        "extracted_data": application["extracted_data"],
        "findings": ["Loaded synthetic document inventory."],
    }


def extract_fields(state: LoanState) -> dict:
    """In this milestone, use pre-extracted synthetic fields.

    A later milestone will replace this node with OCR plus structured
    extraction. Keep extraction separate from validation.
    """
    data = state.get("extracted_data", {})
    if not data:
        return {"findings": ["No extracted fields are available."]}
    return {"findings": ["Loaded synthetic extracted fields for validation."]}


def validate_application(state: LoanState) -> dict:
    """Apply deterministic completeness and consistency checks."""
    documents = set(state.get("documents", []))
    missing = sorted(REQUIRED_DOCUMENTS - documents)
    data = state.get("extracted_data", {})
    findings = []

    if missing:
        findings.append("Missing required documents: " + ", ".join(missing))

    customer_name = data.get("customer_name")
    identity_name = data.get("identity_name")
    if customer_name and identity_name and customer_name.casefold() != identity_name.casefold():
        findings.append("Name mismatch between application and identity document.")

    if not data.get("monthly_salary"):
        findings.append("Monthly salary field is missing.")

    if not data.get("salary_slip_month"):
        findings.append("Salary slip period is missing.")

    if not data.get("bank_statement_months"):
        findings.append("Bank statement period could not be confirmed.")

    if not findings:
        findings.append("Required demo fields are present and passed basic consistency checks.")

    return {
        "missing_documents": missing,
        "findings": findings,
    }


def route_for_review(state: LoanState) -> str:
    """Route incomplete or inconsistent applications to manual review."""
    findings = state.get("findings", [])
    has_mismatch = any("mismatch" in item.lower() for item in findings)
    has_missing = bool(state.get("missing_documents")) or any(
        "missing" in item.lower() or "could not be confirmed" in item.lower()
        for item in findings
    )
    return "manual_review" if has_mismatch or has_missing else "review_ready"


def manual_review(state: LoanState) -> dict:
    """Prepare a human-review handoff; this node does not decide the loan."""
    summary = (
        f"Application {state['application_id']} requires manual document review. "
        "Findings: " + " ".join(state.get("findings", []))
    )
    return {"review_route": "MANUAL_REVIEW", "final_summary": summary}


def review_ready(state: LoanState) -> dict:
    """Prepare a summary for an authorized reviewer, not an approval."""
    summary = (
        f"Application {state['application_id']} passed the basic demo checks. "
        "This is not a loan approval or credit decision. An authorized reviewer "
        "must complete the applicable bank process."
    )
    return {"review_route": "REVIEW_READY", "final_summary": summary}


def build_graph():
    """Build and compile the document verification StateGraph."""
    builder = StateGraph(LoanState)
    builder.add_node("ingest_documents", ingest_documents)
    builder.add_node("extract_fields", extract_fields)
    builder.add_node("validate_application", validate_application)
    builder.add_node("manual_review", manual_review)
    builder.add_node("review_ready", review_ready)

    builder.add_edge(START, "ingest_documents")
    builder.add_edge("ingest_documents", "extract_fields")
    builder.add_edge("extract_fields", "validate_application")
    builder.add_conditional_edges(
        "validate_application",
        route_for_review,
        {
            "manual_review": "manual_review",
            "review_ready": "review_ready",
        },
    )
    builder.add_edge("manual_review", END)
    builder.add_edge("review_ready", END)
    return builder.compile()
