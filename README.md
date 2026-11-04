# CatalogMatch

Supplier product matching with measured automation risk.

**Status: data feasibility.** The offline ALASKA Monitor validator is implemented. Matching quality has yet to be evaluated.

CatalogMatch will map inconsistent supplier offers to exact variants in a reference catalog. It will compare inexpensive deterministic methods with retrieval and LLM approaches, automate decisions supported by evidence, and send ambiguous cases to human review.

## Problem and approach

Matching a similar description is not enough: capacity, pack size, model and other attributes may distinguish different sellable variants. The system must also recognize insufficient evidence and offers without an established catalog match.

The first stage checks data fitness and compares lexical/rule matching with a current LLM baseline over retrieved candidates. More complex models and infrastructure are conditional on measured benefit.

## Demo and evaluation

The audited archive yields 16,662 records and 2,246 candidate source assignments after quarantine. These assignments still need identity review. The [evaluation contract](docs/EVALUATION.md) defines the planned protocol. Future results must identify the dataset/split, model and configuration, sample sizes, automatic-match error rate, coverage, runtime/cost and limitations.

## Run locally

From the repository root, use Python 3.12 (verified with 3.12.4 on Windows). Only the standard library is required. Supply your archive path using the acquisition recipe and expected SHA-256 in the [data audit](docs/data-audit.md).

```powershell
py -3.12 -m alaska_monitor "path/to/monitor.tar.gz"
py -3.12 -m unittest discover -s tests -v
```

The CLI writes deterministic JSON to stdout. Exit 0 means structural inspection completed. Inspect the issues and quarantine sections even on success. Duplicate entries give the entity, record locator and total occurrences. Missing references are excluded from candidates. Exit 1 reports an unreadable, malformed or oversized input as a single JSON error. Redirect stdout to a private path to retain the report. The loader reads members in memory under the audit limits and preserves original attributes and ER rows for subsequent local review. Ordinary tests use synthetic archives.

To replay the [F1 diagnostic manifest](docs/data/alaska-monitor-diagnostic.json), run the first command below. For independent review, give the reviewer the second command's worksheet and local access to the referenced archive records. Keep the manifest, ER assignments and pilot judgments separate until judgments are recorded.

```powershell
py -3.12 -m diagnostic_pairs "path/to/monitor.tar.gz"
py -3.12 -m diagnostic_pairs "path/to/monitor.tar.gz" --worksheet > review.csv
```

For each pair, record each offer's eligibility under D15, then apply monitor identity policy D17 using the raw attributes. Enter `same_variant`, `different_variant` or `insufficient_evidence`, a short evidence-based rationale and reviewer origin. Preserve uncertain cases and join completed reviews by ID. See the [evaluation contract](docs/EVALUATION.md).

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

AI assistance was used to prepare the initial project documentation. The intended development process also uses AI for implementation drafts, tests and review. Generated output is not evidence of correctness: accepted changes and reported results require appropriate validation. Record actual experiments and meaningful failures, and update this description as work progresses. AI assistance also contributed to the loader and its synthetic tests.

