# Stage 000: data and baseline feasibility

- Revision: 1
- Status: draft
- Created: 2026-10-27
- Owner role: planning chat, then implementation chat per selected task
- Execution: not started; first planning chat must refine F0 before implementation

## Objective
Determine whether one bounded product-matching task has usable data, defensible labels, and meaningful engineering trade-offs before building the application.

## Existing state and constraints
This repository contains project documentation and a local-note ignore rule only. There is no verified Python environment, package manager, data, application, test suite or deployment.

Read [project brief](../PROJECT_BRIEF.md), [decisions](../DECISIONS.md) and [evaluation contract](../EVALUATION.md). Exact variant identity is accepted; category, schema and model are not selected. WDC Products is a candidate, not an audited source.

## Timebox and permissions
Estimated stage effort: 20-30 human working hours; review scope if evidence collection exceeds it. This is not an automatic runtime or monetary allowance.

Do not initialize Git, install production dependencies, download large corpora/model weights, run paid APIs or provision infrastructure merely because this plan mentions them. Record concrete user authorization when needed and do independent offline work meanwhile. Public documentation and bounded source/sample inspection can support planning within the user's current request.

## Tasks to refine
| ID | Status | Outcome | Dependency |
| --- | --- | --- | --- |
| F0 | draft | Source/environment audit and a recommended bounded data task | None |
| F1 | draft | Identity policy, reviewed diagnostic data and split design | F0 |
| F2 | draft | Reproducible lexical/rule baseline and error report | F1 |
| F3 | draft | Comparable LLM baseline with observed cost and failure analysis | F2; explicit API/model budget authorization |
| F4 | draft | Continue, simplify, or change-domain decision; next product slice | F2/F3 evidence, or explicit incomplete-stage limitation |

### F0 — first discovery task
**Purpose:** resolve data feasibility and inspect the local toolchain, without implementing the application.

The planner should turn this into one bounded execution task using actual source and environment facts. Suggested work:
- Inspect existing runtime/tool versions without installing or replacing them.
- Inspect WDC Products documentation and a small public sample if terms permit; consider at most one alternative if WDC clearly fails the task.
- Record source/terms, label origin, sample fields, missing values, category/variant semantics, approximate download sizes and acquisition risks.
- Recommend a category only if the sample supports it. Do not assume electronics is suitable.
- Define the next small artifact/schema and reproducible acquisition approach.

**Proposed deliverable:** `docs/data-audit.md` with public technical evidence, limits and a recommendation. This file does not exist yet. Small downloaded samples, if allowed, need provenance and must not be silently treated as redistributable fixtures. Follow [DOCUMENTATION.md](../DOCUMENTATION.md): keep scratch notes, account details and restricted examples local; publish the reproducible method and permitted evidence. The report must remain useful without local files.

**Acceptance:** another engineer can understand where data comes from, what may be used/shared, what labels mean, what remains uncertain, and how to proceed. If terms or semantic fit cannot be established, report that explicitly and propose a bounded alternative; do not call the dataset validated.

**Validation:** check cited primary sources and inspect the actual sample if obtained. No benchmark claims. The planner must specify permitted acquisition size, exact output paths and feasible checks before execution.

### F1 — identity and evaluation design
Draft category-specific identity rules and annotation instructions. Inspect roughly 100-150 examples, including hard negatives, insufficient evidence and absent-product cases. Arrange owner review of ambiguous rules/labels rather than claiming model-generated labels are human-reviewed.

Design product-disjoint splits and a reference catalog. Preserve original benchmark results separately. State uncertainty and potential contamination. Output paths and schema are to be defined after F0.

### F2 — deterministic baseline
Select a minimal environment/dependency set, with required approval, and document actual setup commands. Implement a reproducible local baseline and meaningful offline tests. Measure candidate recall separately from matching and report difficult cases. API/UI/queues are out of scope.

### F3 — current LLM comparison
Select provider/model from current documentation, record explicit budget and call limits, and keep credentials outside artifacts. Compare a constrained LLM decision with the deterministic baseline on equivalent candidates. Include abstention, invalid-output handling and actual cost. Keep held-out data separate from prompt tuning. Do not use the same model as sole ground-truth annotator/judge.

If credentials/budget are missing, offline adapter tests may be prepared when authorized, but F3 remains incomplete. Never substitute mock results for live performance.

### F4 — decision
Continue if the problem is assessable, data use is permitted, and results support meaningful quality/cost/reliability trade-offs. Simplify if a baseline wins; change category/scope if ground truth cannot be established. Do not require a custom model to outperform the LLM to justify building a well-evaluated application.

Prepare the next small vertical-slice plan only after inspecting evidence. Preserve failed hypotheses and uncertainty. No invented claim of 99% precision or customer savings.

## Definition of stage completion
- Data/identity limitations and usage terms are documented.
- A reproducible baseline comparison exists, including a genuine LLM run if authorized; otherwise the missing evidence is explicit and this stage is not labeled fully validated.
- Representative failures, split validity and the chosen approach are explained with evidence.
- The next stage has a bounded scope based on observed results.

## Execution evidence
None. Do not mark planned work as completed.

## Review
Not started. Review should emphasize identity semantics, leakage, label provenance and baseline fairness before style or infrastructure.

## Handoff
Next: planning chat inspects these documents/environment and refines F0. Keep later tasks coarse until F0 provides evidence. No paid budget or dependency approvals recorded.

## Revision notes
- Revision 1: documentation/publication boundary clarified; technical scope unchanged. No feasibility work has been executed.
