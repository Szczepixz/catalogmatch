# CatalogMatch

Supplier product matching with measured automation risk.

**Status: feasibility planning.** There is no application, audited dataset, model benchmark, test suite, or deployment yet.

CatalogMatch will map inconsistent supplier offers to exact variants in a reference catalog. It will compare inexpensive deterministic methods with retrieval and LLM approaches, automate decisions supported by evidence, and send ambiguous cases to human review.

## Problem and approach

Matching a similar description is not enough: capacity, pack size, model and other attributes may distinguish different sellable variants. The system must also recognize insufficient evidence and offers without an established catalog match.

The first stage checks data fitness and compares lexical/rule matching with a current LLM baseline over retrieved candidates. More complex models and infrastructure are conditional on measured benefit.

## Demo and evaluation

No demo or measured results are available yet. The [evaluation contract](docs/EVALUATION.md) defines the planned protocol. Future results must identify the dataset/split, model and configuration, sample sizes, automatic-match error rate, coverage, runtime/cost and limitations.

## Run locally

No executable setup commands exist yet. Once implementation starts, this section will contain commands verified in the supported environment. The [current state](docs/STATE.md) identifies the next task.

## Project context

| Document | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Persistent working rules for every chat |
| [Project brief](docs/PROJECT_BRIEF.md) | Product, scope, rationale, and roadmap |
| [Decisions](docs/DECISIONS.md) | Accepted constraints, provisional choices, and open questions |
| [Evaluation contract](docs/EVALUATION.md) | Identity semantics, datasets, baselines, metrics, and evidence |
| [Workflow](docs/WORKFLOW.md) | Planning, implementation, review, and handoffs |
| [Documentation policy](docs/DOCUMENTATION.md) | Documentation maintenance and versioning rules |
| [Current state](docs/STATE.md) | Current stage and next action |
| [Feasibility plan](docs/plans/000-feasibility.md) | Initial plan to refine before implementation |
| [Plan template](docs/plans/TEMPLATE.md) | Template for later meaningful stages |

## Intended product flow

Defined-format supplier input -> validated records -> candidate retrieval -> matching/evidence -> decision policy -> review or accepted mapping -> audit/export.

Start locally with one category and text input. Prove data fitness and useful baselines before adding the API, UI, persistence, and operational hardening.

## Development and AI assistance

AI assistance was used to prepare the initial project documentation. The intended development process also uses AI for implementation drafts, tests and review. Generated output is not evidence of correctness: accepted changes and reported results require appropriate validation. Record actual experiments and meaningful failures, and update this description as work progresses. No application code has been implemented yet.

