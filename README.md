# Loan Document Verification Agent

An educational banking workflow that demonstrates how LangGraph can coordinate document intake, extraction, validation, exception routing and human review.

The prototype uses fictional application data. It does not make credit decisions, approve loans, verify real identity documents or connect to a bank.

## Learning objectives
- Model a multi-step business process as a LangGraph StateGraph.
- Design state schemas and field-level reducers.
- Build nodes and normal/conditional edges.
- Understand document ingestion, OCR, extraction and validation boundaries.
- Understand where Hugging Face models and embeddings can be introduced.
- Understand RAG, checkpointers, interrupts and human-in-the-loop review.
- Explain why AI findings must not become automatic lending decisions.

## Architecture — first milestone
Application input -> document inventory -> mock extraction -> validation -> conditional route.
If required fields are missing or inconsistent, route to manual review. Otherwise, route to a review-ready summary. The workflow only produces a verification summary; an authorized person remains responsible for any lending decision.

## Repository layout
- app/state.py: workflow state and reducer
- app/mock_documents.py: fictional document payloads
- app/graph.py: LangGraph nodes and routing
- app/main.py: sample applications
- tests/test_workflow.py: basic workflow tests
- docs/architecture.md: design and interview notes

## Setup
Python 3.11+ recommended.

Windows PowerShell:
    py -3.11 -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt

macOS/Linux:
    python3.11 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Run:
    python -m app.main

Test:
    python -m pytest

## Concepts demonstrated
| Concept | Meaning | Example |
|---|---|---|
| State | Shared workflow data | application id, extracted fields, flags |
| Node | One processing step | extract or validate |
| Edge | Fixed transition | extraction to validation |
| Conditional edge | Branching based on state | complete vs manual review |
| Reducer | Merges updates for a state key | append validation findings |
| Checkpointer | Persists graph state at checkpoints | resume an interrupted review |
| Human-in-the-loop | Pauses for authorized input | reviewer examines discrepancies |

## Where Hugging Face fits
A later milestone can use a Hugging Face model or library for document classification, token classification or embeddings. OCR can be performed by a dedicated OCR engine; a language model should not be assumed to reliably read every scanned document. Extracted fields should be validated against deterministic rules and source evidence.

## Where RAG fits
If internal policy documents are added, a RAG pipeline can:
1. Parse and chunk approved policy documents.
2. Generate embeddings with a sentence-transformers model.
3. Store vectors in a vector index such as FAISS.
4. Retrieve relevant policy passages for a question.
5. Pass the retrieved passages, with source references, to the model.

RAG retrieves supporting text; it does not prove that a customer is eligible or replace policy controls.

## Responsible banking design
Use synthetic data only. A production system requires lawful purpose, consent where applicable, access controls, encryption, audit trails, data retention rules, model risk management, bias testing, explainability, human oversight and security review. Do not infer protected or sensitive attributes. Do not let an LLM make the final credit decision.

## Learning milestones
1. Build the deterministic workflow and understand state/nodes/edges/reducers.
2. Add document parsing and OCR on synthetic sample documents.
3. Add structured extraction and schema validation.
4. Add Hugging Face embeddings and a small RAG policy corpus.
5. Add LangGraph checkpointing and interrupt/resume for human review.
6. Add tests, tracing and interview-ready architecture documentation.

## Interview summary
"I modelled a loan-document verification process as a LangGraph workflow. The state carries application and extraction data, nodes perform ingestion and validation, and conditional edges route exceptions to manual review. Reducers merge findings from document-processing branches. Hugging Face can provide extraction or embedding models, while RAG can retrieve relevant policy passages. The prototype supports document review only; it does not make a lending decision."
