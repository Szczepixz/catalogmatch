# CatalogMatch

Supplier product matching with measured automation risk.

**Status: data feasibility.** The offline ALASKA Monitor validator, diagnostic annotation ledger and bounded development identity proposal are implemented. Matching quality has yet to be evaluated.

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

### Replay the F1 annotation ledger

The ledger verifies the archive, replays diagnostic selection and the masked-review ID mapping, preserves observations, and applies the [versioned adjudications](docs/data/alaska-monitor-adjudications.json). Supply the two preserved private review CSVs and mapping explicitly:

```powershell
py -3.12 -m annotation_ledger "path/to/monitor.tar.gz" "path/to/first-review.csv" "path/to/second-review.csv" "path/to/private-key.csv" > "path/to/ledger.json"
```

Use an existing output directory and a new output path, never an input CSV. Exit 0 emits one complete deterministic JSON ledger; exit 1 emits one JSON error without a partial ledger. Inspect exit status before consuming a redirected file. All processing is offline; nothing is uploaded. No personal notes or private default paths are loaded.

Both review CSVs have the exact header `id,eligibility_left,eligibility_right,judgment,rationale,reviewer_origin`; the key has `id,original_id,first_judgment`. This release imports the preserved AI reviews only: origin `AI`, eligibility `eligible`, and the three D17 judgment values. It is not a general annotation importer. The configuration pins the archive and private CSV hashes to exact bytes. Public JSON hashes normalize CRLF to LF so Git checkout line endings do not change provenance; substantive changes still fail verification. A fresh clone can run synthetic tests but needs the original private CSVs to reproduce these annotations.

The ledger retains 120 oriented pairs, 149 observation events and 15 adjudication events; effective counts are **18 same / 45 different / 57 insufficient**. Original rationale text stays in the input CSVs and is referenced by SHA-256 of its decoded UTF-8 text. Output includes categorical observations, sanitized adjudication reasons, evidence field names, provenance hashes, source structure, exposure/hold blocks and identity warnings, but no raw offer attributes or reviewer prose. An unknown historical event date is `null`; plan revision order determines supersession. The pinned ID mapping binds assessments to the original side orientation; it cannot independently establish how reviewers interpreted their inputs or their isolation.

All 11 held groups remain separate from pair judgments. D013 is still a positive pair in held group 075, and D066/D068 are disconnected positive pairs in group 122. Conservative blocks join shared memberships and exact duplicate JSON objects among assigned records; they do not establish semantic aliases or validated identities. The output is a provisional AI-assisted diagnostic artifact, not a catalog, final split or gold set. Treat its locators and annotations according to the [publication policy](docs/DOCUMENTATION.md) before sharing.

### Validate the bounded F1-I development proposal

The [development manifest](docs/data/alaska-monitor-development.json) records an explicit AI-assisted membership review of the 34 endpoints of 17 non-held positive pairs. It proposes **15 identities, 15 original-record references and 17 cross-source queries**. D066/D068 share a reviewed identity based on record evidence, separately from their leakage block. D013 remains held; D019 is deferred because an offer contains unexplained FH/FWH identifier disagreement. Original pair labels remain unchanged. This is development material, not human gold, a final split or archive-wide alias certification.

```powershell
py -3.12 -m development_identities "path/to/monitor.tar.gz" "path/to/first-review.csv" "path/to/second-review.csv" "path/to/private-key.csv"
py -3.12 -m unittest discover -s tests -v
```

The CLI rebuilds F1-L from the original hash-pinned inputs on every run; it never trusts a saved ledger. It checks the manifest's provenance, explicit endpoints/source memberships, evidence fields and canonical object hashes, holds, internal nonpositive edges, scoped alias-review coverage, duplicates, and reference/query selection. `--manifest "path/to/proposal.json"` selects an explicit alternative. Exit 0 emits a compact validation report and normalized manifest SHA-256; exit 1 emits a single error without a partial report or raw records. Semantic findings are preserved annotations, not generated or proved by this validator. A fresh clone can run synthetic checks but requires the original private inputs to reproduce the real-data validation.

Reference selection uses the owner-approved `capacity-information-hash-v2` rule: maximize nonduplicate cross-host query capacity, then maximize the number of reviewed information categories, then choose the lowest SHA-256 of UTF-8 `f1-catalog-v1|reference|locator`, then locator. Exact duplicates use canonical JSON objects (sorted keys, compact separators, ASCII escaping, UTF-8); choose the lowest eligible query locator per identical payload and retain every member in the audit. Reference/query entries contain locators, not raw descriptions; load the selected original record locally without merging descriptions. No exact duplicates occur in this bounded pool. A review trigger flags at least three common non-title fields with at least 90% identical values; its five findings are explicitly reviewed, not automatically collapsed. D112 retains one correlated cross-source query with 38 matching specification fields. Four other template-overlap pairs have different model identities. Different hostnames are not proof of independent suppliers.

The owner confirmed membership within the 15 displayed sections and reported no noticed aliases between them. This separate event is bound to the [preserved revision-20 snapshot](docs/data/alaska-monitor-development-v1.json); no per-field rationale or approval of individual references was supplied. The original AI annotations remain intact. `human_verified: false` means full independent verification is not claimed; the scoped human assessment is recorded in `owner_review`. Completeness annotations remain AI-assisted, with one point per explicit usable category and field locators, without rewarding repetition. See the [reference rule](docs/EVALUATION.md#development-reference-selection).

All 11 holds, D099 and other unresolved judgments remain unchanged. Independent test checking, broader alias coverage and protocol agreement remain separate work; no F2, final-test reservation or absence experiment has been run. See [revision 20](docs/plans/000-feasibility.md#bounded-f1-i-development-identities-revision-20-2026-11-13) for scope and validation evidence.

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

AI assistance was used to prepare the initial project documentation. The intended development process also uses AI for implementation drafts, tests and review. Generated output is not evidence of correctness: accepted changes and reported results require appropriate validation. Record actual experiments and meaningful failures, and update this description as work progresses. AI assistance also contributed to the loader, annotation ledger, bounded identity review/validator and their synthetic tests.

