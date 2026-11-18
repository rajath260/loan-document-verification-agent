"""State schema for the loan-document workflow."""

from operator import add
from typing import Annotated, TypedDict


class LoanState(TypedDict, total=False):
    """Shared data carried through the graph.

    findings uses a reducer so findings from multiple processing steps can
    be appended instead of replacing previous findings.
    """

    application_id: str
    documents: list[str]
    extracted_data: dict
    missing_documents: list[str]
    findings: Annotated[list[str], add]
    review_route: str
    final_summary: str
