"""Synthetic document inventory and extracted fields.

No real identity or financial documents are included in this repository.
"""

SAMPLE_APPLICATIONS = {
    "APP-1001": {
        "documents": ["identity_document", "salary_slip", "bank_statement"],
        "extracted_data": {
            "customer_name": "Sample Customer",
            "identity_name": "Sample Customer",
            "monthly_salary": 55000,
            "salary_slip_month": "2026-10",
            "bank_statement_months": 6,
        },
    },
    "APP-1002": {
        "documents": ["identity_document", "salary_slip"],
        "extracted_data": {
            "customer_name": "Demo Applicant",
            "identity_name": "Different Name",
            "monthly_salary": 42000,
            "salary_slip_month": "2026-10",
        },
    },
}
