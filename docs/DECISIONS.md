# Decision register

Updated: 2026-10-27. `Accepted` describes project direction, not permission to install dependencies or spend money. Update a row when evidence changes it; do not silently rewrite history. Add a short dated note for consequential revisions.

| ID | Status | Decision | Reason / reopening condition |
| --- | --- | --- | --- |
| D01 | Accepted | Build CatalogMatch around exact-variant matching to an existing catalog | Explicit correctness criteria; revisit if ground truth is infeasible or product requirements change |
| D02 | Accepted | Start with a 20-30 hour feasibility stage | Avoid building infrastructure around unsuitable data |
| D03 | Accepted | One category and one input contract first | Category is open; no universal import or cross-category claims |
| D04 | Accepted | Compare a strong lexical/rule baseline and a current LLM baseline | New models can invalidate unnecessary custom complexity |
| D05 | Accepted | Retrieval quality and decision quality are separate | Same candidate pool for scorer comparisons; also evaluate end to end |
| D06 | Accepted | Human review is a first-class outcome | No forced match on insufficient evidence |
| D07 | Accepted | Product-disjoint custom evaluation and separate threshold selection | Avoid leakage; preserve original protocols when reporting public benchmarks |
| D08 | Accepted | CPU-first, local experiment before modular application | No GPU purchase or distributed infrastructure assumed |
| D09 | Accepted | Short planning -> implementation -> evidence-based review cycles | Different chats use repository files as the handoff; no hidden chat context |
| D10 | Accepted | Current LLM experiment mandatory; deployment conditional | Model integration must have measured value; a negative result is publishable |
| D11 | Provisional | FastAPI/Pydantic and PostgreSQL for the application | Confirm when the application phase is ready; not required for initial data audit |
| D12 | Deferred | Queues, Redis, MLflow, pgvector/ANN, fine-tuning, images | Add individually when evidence or acceptance criteria justify them |
| D13 | Accepted | Version shared technical context; keep optional personal work in ignored `.local/` | Public instructions, plans and commands must remain usable in a fresh clone without local notes |
| D14 | Accepted | Describe AI assistance honestly and evaluate accepted artifacts | No claim of unaided authorship or human verification based only on model review |

## Open decisions

| ID | Question | Resolution stage |
| --- | --- | --- |
| O01 | Which dataset/category supports exact-variant labels and permitted use? | F0 evidence and source audit |
| O02 | Which attributes define identity, and how is ambiguity labeled? | F1, informed by F0 sample |
| O03 | Which Python runtime, environment/package tool and minimal dependencies? | Inspect environment; specify before first executable task |
| O04 | Which LLM/provider/model revision and what authorized spend limit? | Before paid experiments; use current docs and user-provided authorization |
| O05 | What acceptable error/coverage trade-off and review workload? | After initial errors are understood; freeze before final test |
| O06 | Can an actual catalog operator review assumptions/examples? | Optional during feasibility; absence must remain explicit |
| O07 | Which deployment target and operating budget? | Application stage, not a feasibility prerequisite |

## Revision notes
- 2026-10-27: Separated public technical documentation from optional local prompts and personal context. Product scope and evaluation requirements are unchanged.
- 2026-10-27: Starter records the reassessed direction. No model, category, license conclusion, measured result, or installed stack has been established.
