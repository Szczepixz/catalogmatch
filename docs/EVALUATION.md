# Evaluation contract

This is a design constraint, not a claim that evaluation has been implemented. Refine task-specific details in the feasibility plan and record durable changes here.

## Define the target before evaluating
- Write an identity policy for the chosen category: which attributes change the exact sellable variant, which are harmless formatting differences, and which missing fields make a case unresolved.
- Reference pair labels: `same_variant`, `different_variant`, `insufficient_evidence`. Do not force ambiguous labels or drop difficult cases without reporting them.
- System actions: `auto_match` or `review_required` initially. A proposed `no_match` is distinct from insufficient evidence and requires an explicit catalog-absence protocol before automation.
- Similarity scores, schema-valid JSON, and model-written explanations are not evidence of correctness by themselves.

## Dataset requirements
Record source URL/version, acquisition date, license/terms, permitted local use and redistribution, transformation rules, hashes, category coverage, and label origin. Distinguish benchmark labels, human review, model-assisted suggestions, and generated fixtures.

Public historical data is a useful baseline but may contain label noise or model pretraining contamination. Do not claim to exclude contamination. Do not redistribute data until terms permit it. Store reproducible acquisition instructions when raw redistribution is not permitted.

Approximately 100-150 manually inspected diagnostic examples are an early feasibility target, not enough to certify high precision. Include confusing variants, missing attributes, duplicates, inconsistent formatting, and absent catalog products. Report ambiguous examples and disagreement. A second reviewer is useful; delayed self-review is not equivalent to independent annotation.

## Splits and catalog construction
- Preserve original benchmark splits and task definitions when reporting results under that benchmark's name.
- For a custom end-to-end protocol, separate train, development/calibration, and frozen test products by identity. Record the grouping method.
- A product unseen during training can still have a reference record in the searchable test catalog. State this explicitly; it differs from an absent product.
- Create absent-product cases by removing complete product identities from the reference catalog. Missing annotation is not proof of absence.
- Keep label/cluster IDs out of model features. Use reliable real identifiers as an explicit baseline only when they would be available at inference; avoid circular evaluation when those identifiers generated labels.
- Fit preprocessing and learned components using the permitted training data. Choose prompts, thresholds and hyperparameters on development data, not the test set.
- Do not claim unseen-supplier generalization without a supplier-aware split and sufficient metadata.
- Separate a curated challenge set from a representative sample. Its class balance and error rate must not be presented as expected live traffic performance.

## Baselines and experiments
1. Exact identifiers where legitimate, followed by normalization, lexical/fuzzy retrieval and attribute rules.
2. A current LLM over a bounded candidate set, with constrained output and an abstention option.
3. Embedding retrieval and/or a small learned pair scorer if initial failures justify it.
4. Selective LLM usage or LLM attribute extraction, if it addresses observed errors.

For scorer comparisons, use identical candidate sets. Measure retrieval separately and also report end-to-end performance. A benchmark giving the scorer the correct candidate by construction must be labeled as such.

Treat extraction and matching as different components: correct JSON does not establish correct attributes, and correct attributes do not guarantee a correct match. Source evidence should point to actual input text, not an invented rationale.

Only keep an added component if it improves a meaningful trade-off. No requirement to beat every approach on every metric or to fine-tune a model.

## Metrics
| Layer | Measurements |
| --- | --- |
| Retrieval | Recall@k on cases with a catalog match; candidate count and latency |
| Matching | Top-1/end-to-end correctness; pair precision/recall and relevant slices |
| Automation | Wrong automatic matches / all automatic matches; automatic coverage / all eligible requests; review rate |
| Absent products | False automatic match rate on known absent cases; separate from missing evidence |
| Confidence | Reliability/calibration analysis on held-out data if probabilities are exposed; relevance is not identity probability |
| Runtime | End-to-end p50/p95, throughput at stated load, timeouts/failures, queue time when applicable |
| Cost | Total observed cost including failed calls/retries; cost per processed and per correctly resolved offer; review time only if measured |

Always give denominators and sample sizes. Report metrics as undefined when no eligible decisions exist rather than inventing a perfect score. Use product-aware uncertainty estimates when records are correlated. A tiny zero-error sample does not establish 99% precision.

The main comparison is coverage at a specified observed error level, together with cost and runtime. Early diagnostic thresholds are provisional; freeze the release policy before final testing.

## Reproducibility
Each experiment records dataset/split hashes, catalog version, code version (commit if available), dependency/runtime versions, model/provider revision, prompts and schema, configuration/seed, candidate method/k, thresholds, raw predictions where permitted, aggregate/slice metrics, actual cost and limitations. Date provider aliases and acknowledge residual nondeterminism.

Follow the [documentation policy](DOCUMENTATION.md) for reports and artifacts. Version application inference prompts, schemas and evaluation settings; these are required product context, not private coding-chat prompts. Keep raw restricted data and account information out of public reports. Publish permitted aggregates, error analyses and acquisition/reproduction instructions. Local data access requirements must be explicit, without making the public protocol depend on private notes.

Do not use the candidate model as the sole judge of its own answers. Prefer checked labels and deterministic graders for identity tasks. Human corrections should enter a versioned future training/development release, not silently alter a frozen test.

## Software checks versus quality checks
Ordinary tests run offline with clearly labeled fixtures and mocked provider responses. Meaningful cases include variant conflicts, missing data, invalid candidate IDs, parse failures, duplicate records and bounded retries. Later add job recovery, concurrent review and artifact-version mismatch tests when those behaviors exist.

Live model evaluation is an explicit, budgeted command. CI may gate deterministic regressions and a small stable evaluation once its variability is understood. Never hide failed evaluations by lowering thresholds after seeing the test results.
