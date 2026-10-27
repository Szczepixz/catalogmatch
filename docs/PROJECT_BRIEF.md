# Project brief

## Goal
Build a feasible product matching system with reproducible comparisons and explicit uncertainty. Evaluate quality, cost and operational behavior before adding complexity.

## Product problem
Supplier offers use inconsistent titles and descriptions. An operator needs to map them to exact variants in a reference catalog without silently merging different capacities, pack sizes, models, conditions, or other identity-defining attributes.

Intended user: a catalog/import operator. Actual user access, business impact, and demand have not been validated. If an operator is available, use a short interview to check identity rules and error costs. Do not invent customer validation.

Example: `Phone Y 128 GB Black` may match a differently formatted description of that variant, but not its 256 GB version. An incomplete title may provide too little evidence for either decision. These examples illustrate requirements; they are not benchmark records.

## Central engineering question
How much correct matching can be automated at a specified error tolerance, cost, and latency, while abstaining on insufficient evidence?

Product identity differs from semantic relevance. Pair classification also differs from finding a match in a catalog. Both retrieval and final decisions must be evaluated.

## Scope

### Feasibility stage
- One candidate category, chosen after inspecting available data.
- Explicit exact-variant identity policy.
- Public data/source audit and a small reviewed sample.
- Strong lexical/rule baseline and a current, well-prompted LLM baseline over candidates.
- Honest error analysis and a continue/simplify/change-domain decision.

### First complete product slice
- One documented CSV/input schema; no universal importer.
- Reference catalog and supplier offers with preserved raw inputs.
- Candidate matching and explicit review outcomes.
- Small API and review interface, persistent decisions, and export.
- Reproducible evaluation and basic deployment instructions.

### Evaluated application
- Frozen evaluation, comparisons and failure slices.
- Versioned catalog/model/prompt/policy artifacts.
- Idempotent imports and resumable batch processing where needed.
- Measured runtime/cost, bounded retries, failure recovery and basic monitoring.
- Accessible demo, concise technical write-up, known limitations and short video.

### Later options: select at most one initially
Task-specific model tuning; domain/supplier shift evaluation; active learning; or multimodal evidence. Each requires an observed limitation and a measurable hypothesis.

## Non-goals
Autonomous purchasing, ERP integration, global product clustering, arbitrary PDF/Excel ingestion, web-scale scraping, general chat, multi-agent orchestration, GPU platform engineering, and a marketplace SaaS platform are outside the initial scope.

## Architecture direction, not installed stack
Begin with a local Python experiment. Keep normalization, retrieval, scoring, policy and reporting separable. Prefer a modular monolith for the application.

FastAPI/Pydantic, PostgreSQL, scikit-learn and Sentence Transformers are candidates, not an approved dependency manifest. pgvector, queues, Redis, MLflow and ANN indexes are deferred until useful. A simple review UI is sufficient; avoid learning an unrelated frontend stack unless required.

## Planning assumptions
- CPU-first; no dedicated GPU required for the initial scope.
- One bounded category, a limited corpus and reproducible local experiments before deployment.
- Actual API/run budgets must be authorized and recorded before execution; there is no approved paid budget yet.
- The first feasibility stage is timeboxed in its plan. Later effort estimates should be revised from observed work.

## Why this direction
Exact-variant matching exposes measurable trade-offs between retrieval, decision quality, cost and review workload. It supports a complete application without requiring web-scale infrastructure. The current direction was reviewed on 2026-10-27: a current LLM baseline is required experimentally and infrastructure remains deferred. If a simpler approach wins, use it.

## Selected evidence, not proof of project performance
Sources were inspected on 2026-10-27. Verify current source terms and model details before use. No dataset was downloaded or empirically audited during that research.
- [Shopify catalog engineering](https://shopify.engineering/catalog-clustering): related precision-first catalog work. Its product-family clustering semantics are not our exact-variant policy.
- [WDC Products](https://webdatacommons.org/largescaleproductcorpus/wdc-products/): candidate benchmark with seen/unseen variants and reported label noise; fitness and licensing remain to be checked.
- [Hamel Husain and Shreya Shankar on evals](https://hamel.dev/blog/posts/evals-faq/): error analysis and task-specific criteria; practitioner guidance, not hiring guarantees.

Revisit scope when data fitness or observed behavior invalidates an assumption. Keep personal project-selection and career notes outside the shared technical documentation.
