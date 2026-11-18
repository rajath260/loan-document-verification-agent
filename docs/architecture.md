# Architecture and interview notes

## Workflow
The graph follows a controlled sequence: ingest document inventory, load extracted fields, validate required documents and field consistency, then branch to a manual-review handoff or a review-ready summary.

## State
LoanState carries the application identifier, document list, extracted fields, missing documents, findings, route and summary. State is the workflow context shared across nodes.

## Nodes
Each node is a focused operation. Ingestion loads the document inventory. Extraction currently loads synthetic pre-extracted values. Validation applies deterministic rules. The final nodes prepare either a manual-review handoff or a review-ready summary.

## Edges and conditional routing
Normal edges connect the fixed sequence. A conditional edge after validation checks the state and selects the appropriate route. This makes the workflow explicit and testable.

## Reducers
The findings field uses operator.add. Each node can append findings while retaining earlier findings. Reducers are defined per state field. When parallel branches are added later, define reducers for any shared fields that can receive concurrent updates.

## OCR and extraction
OCR converts scanned image content into text. A document extraction model or structured LLM extraction step can map that text into a schema. Extraction and validation should remain separate: a plausible extracted value is not automatically a verified value. Preserve source references and confidence where appropriate, then apply deterministic checks.

## Hugging Face
Hugging Face offers model and dataset tooling. This project could use a sentence-transformers model for embeddings or a suitable document model for classification/extraction. Model choice depends on document type, language, deployment constraints, privacy and evaluation results.

## RAG
For internal policy Q&A, parse approved policy documents, split them into chunks, embed the chunks, store vectors in a vector index, retrieve relevant passages and pass those passages to the model with citations or source identifiers. RAG supplies contextual evidence; it does not replace policy engines or underwriting controls.

## Checkpointing and human review
A later milestone can add a LangGraph checkpointer and an interrupt before a reviewer-dependent step. A persistent thread identifier lets the application resume the same workflow after the reviewer responds. Checkpoint storage must be protected because it may contain sensitive application data.

## Banking controls
The prototype uses fictional data and does not approve or reject loans. A real deployment requires identity and access controls, encryption, auditability, data retention controls, model governance, bias and quality testing, explainability, human oversight and formal security/legal review.

## Interview explanation
"I built a document-verification workflow with LangGraph. State carries application context, nodes handle ingestion, extraction and validation, and conditional edges route incomplete or inconsistent cases to manual review. Reducers combine findings from processing steps. Hugging Face can support document models and embeddings, while RAG can retrieve relevant policy passages. The system prepares evidence for a reviewer and does not make the lending decision."
