# Stage 000: data and baseline feasibility

- Revision: 2
- Status: ready (F0 only; stage execution not started)
- Created: 2026-10-27
- Owner role: planning chat, then implementation chat per selected task
- Updated: 2026-10-28
- Selected task: F0
- Execution: planning complete; F0 awaits a separate execution request

## Objective
Determine whether one bounded product-matching task has usable data, defensible labels, and meaningful engineering trade-offs before building the application.

## Existing state and constraints
This repository contains project documentation and a local-note ignore rule only. Inspection on 2026-10-28 found an initialized Git repository at base commit `58da9e5`, with a clean initial working tree. No application, dataset, dependency manifest, virtual environment, tests or deployment were found. Local notes are ignored and not tracked.

Verified on Windows/PowerShell: `py -3.12 --version` reports Python 3.12.4, `py -3.12 -m pip --version` reports pip 24.0, and Git is 2.43.0.windows.1. `uv` was not found on PATH; `python` resolves to a WindowsApps alias, so use the verified launcher. These observations do not establish a reproducible project environment. F0 needs only the existing interpreter and standard library; do not install anything or use global third-party packages. Environment creation/package management for F2 remains open.

Read [project brief](../PROJECT_BRIEF.md), [decisions](../DECISIONS.md) and [evaluation contract](../EVALUATION.md). Exact variant identity is accepted; category, schema and model are not selected. WDC Products is a candidate, not an audited source.

## Timebox and permissions
Estimated stage effort: 20-30 human working hours; review scope if evidence collection exceeds it. This is not an automatic runtime or monetary allowance.

Do not initialize Git, install production dependencies, download large corpora/model weights, run paid APIs or provision infrastructure merely because this plan mentions them. Record concrete user authorization when needed and do independent offline work meanwhile. Public documentation and bounded source/sample inspection can support planning within the user's current request.

## Tasks
| ID | Status | Outcome | Dependency |
| --- | --- | --- | --- |
| F0 | ready | Bounded source/terms/sample audit and an evidence-based F1 recommendation | Separate execution request |
| F1 | draft | Identity policy, reviewed diagnostic data and split design | F0 |
| F2 | draft | Reproducible lexical/rule baseline and error report | F1 |
| F3 | draft | Comparable LLM baseline with observed cost and failure analysis | F2; explicit API/model budget authorization |
| F4 | draft | Continue, simplify, or change-domain decision; next product slice | F2/F3 evidence, or explicit incomplete-stage limitation |

### F0 — bounded data feasibility audit

**Purpose:** determine what evidence and permissions are still needed for F1. This is discovery, not dataset selection, annotation, a benchmark or application implementation. A well-supported negative or unresolved finding is a valid outcome.

**Inputs:** this revision; root `AGENTS.md`; [brief](../PROJECT_BRIEF.md); [decisions](../DECISIONS.md), especially D01/D07 and O01-O03; [evaluation contract](../EVALUATION.md), especially Dataset requirements and Splits; [workflow](../WORKFLOW.md); [documentation policy](../DOCUMENTATION.md). Personal notes are optional and must not supply required technical context.

#### Planning evidence and starting sources

Inspected on 2026-10-28; these are publisher claims, not local data measurements:

- [WDC Products](https://webdatacommons.org/largescaleproductcorpus/wdc-products/) sections 3 and 5 describe identifier-derived clusters, five descriptive attributes and an expert sample with approximately 4% label noise. This is not exact-variant ground truth for our policy.
- Downloads include pair-wise and multi-class examples. Listed archives are approximately 20-21.6 MB and 2.3-2.5 MB respectively; PDC2020-C is 4.3 GB and its category mapping 134 MB. Sizes were not checked against HTTP responses.
- The documented benchmark schema lacks a category field; source URLs are documented only for PDC2020-C. Category and supplier coverage cannot be assumed.
- [Publisher code repository](https://github.com/wbsg-uni-mannheim/wdcproducts) is a provenance lead, not authorization to execute its pipeline.
- [WDC home/license section](https://webdatacommons.org/index.html) names Apache for the extraction framework. This does not establish a data license. Data-specific local-use and redistribution terms remain unresolved.

No data payload was downloaded or inspected during planning. No alternative was researched: current evidence justifies a bounded WDC audit before branching.

#### Execution bounds and method

1. Recheck relevant files, Git status and the interpreter. Do not install dependencies, create an environment, initialize Git or change the index/history. Use a 2-3 hour working timebox for F0, including reporting; at the limit return evidence and the exact missing prerequisite rather than expanding discovery.
2. Resolve terms first using the publisher page, linked repository documentation and any directly linked data terms. Record separately: access, local inspection/use, publishing derived statistics, raw redistribution, and future transmission to a model provider. Use `supported`, `restricted` or `unresolved` with supporting URL, date and scope. Availability and a software license do not establish data rights. Do not contact maintainers or accept terms on the user's behalf. If local inspection rights remain unresolved, skip sample acquisition and complete the documentation-only branch.
3. If permitted, inspect only the publisher's `Example (PW)` and `Example (MC)` links in section 5. Resolve and record exact URLs at execution time. Cap combined dataset transfer at 2 MiB, each response at 1 MiB, and decoded data at 5 MiB. Use bounded reads/timeouts; do not rely on Content-Length alone. Stop on oversize, incomplete JSON, unexpected archives, redirects outside the publisher's hosting, or access restrictions; report the reason. Do not fetch any benchmark archive, corpus, category mapping, weights or live merchant pages, even if an archive is small. A missing suitable sample is a finding, not permission to increase the cap.
4. Inspect up to 50 pair rows and 50 single-offer rows, in source order; record available and inspected counts and any truncation. Do not randomly claim representativeness. Preserve raw values. Record actual field names/types, IDs and label domains; missing/null/empty values separately; unique offer/cluster counts and duplicate IDs with conflicting payloads. Distinguish expected repeated offers in pairs from data errors. Mark absent fields as unavailable rather than synthesizing them. If an example's split is unknown or includes test records, treat it only as schema discovery, never as prompt/threshold development data; keep inspected identities excluded from any later custom frozen test.
5. Examine at most 10 diagnostic cases for identity evidence (model/capacity/pack/condition or other observed attributes), label conflicts and ambiguity. Keep benchmark labels separate from AI-assisted observations; no human-reviewed or gold claims. Record case locators and minimal permitted evidence. No new final identity policy or label corrections in F0. Propose at most one category only if observed records justify further exploration; otherwise leave category open. Tiny examples cannot establish enough category coverage for F1's 100-150 diagnostics.
6. Explain what is missing to convert pair data into offer-to-catalog evaluation: reference-record selection, reliable identity groups, product-disjoint partitions, absent-product construction and supplier metadata. A negative pair is not evidence of catalog absence. Keep source cluster IDs and labels out of proposed inference features. Do not implement retrieval or create splits.
7. Only if WDC fails a concrete access/terms/semantic requirement, inspect documentation for at most one alternative from its original publisher, within the same timebox. Record the trigger and apply the same rights/identity checks; no alternative data download in F0. If unresolved, recommend the smallest follow-up investigation rather than switching product scope or researching the job market.

#### Outputs and interfaces

- Create `docs/data-audit.md` as the single public audit report (not another plan), then link it from this plan. Include source/version/date, evidence table, rights matrix, actual sample coverage/schema/statistics or explicit skipped checks, label-origin assessment, category evidence, end-to-end gaps, and recommendation `proceed_to_F1`, `needs_targeted_followup` or `source_unsuitable`. Distinguish observation, publisher claim, inference and unknown.
- In that report provide a reproducible acquisition/inspection recipe using an arbitrary user-selected work directory: exact URLs, byte limits, source order/row limits, commands or a small standard-library snippet actually used, and expected checks. If data was acquired, record acquisition time, byte counts and SHA-256 for each payload, plus completeness and decoding format. If no acquisition was permitted, give a clearly unexecuted recipe and the missing permission evidence, not invented hashes/counts. No pandas requirement and no reusable application scaffold.
- Raw payloads and scratch work may reside in optional `.local/f0/`; they must not be linked as required public inputs, published, or treated as fixtures. Public reproduction must work without this directory. Publish no raw product text unless redistribution rights are established; use aggregate observations and locators instead.
- End the report with a proposed F1 input contract: required raw/provenance fields, separate source labels and review judgments, identity/grouping uncertainties, permitted acquisition envelope still to approve, and the precise next evidence needed. This is a proposal, not a frozen schema or authorized download.
- Update this plan's F0 row to `review`, add actual files/checks/deviations and the recommendation, and update the short [state pointer](../STATE.md). Leave F1-F4 `draft`. Change the decision register only for supported durable conclusions; preserve open decisions otherwise.

#### Acceptance and validation

- The report supports its conclusion with dated primary sources and explicitly states unresolved rights. An unresolved branch is complete as an audit but does not validate the dataset or make F1 ready.
- Every acquired payload has provenance, bounded acquisition evidence and a hash. Re-run the recorded offline parse/count checks against the saved bytes; verify reported denominators and reconcile overlapping pair/single-offer records before combining counts. No acquisition means these checks are explicitly `not run`.
- Schema claims distinguish documented from observed fields. Category recommendation has sample evidence or is explicitly withheld. Identity ambiguity, source-label noise and the lack of a retrieval benchmark are addressed without changing the evaluation contract.
- Check Markdown relative links, report-to-plan consistency, relevant diff and untracked files. Confirm no personal context, machine-specific paths, raw restricted examples or required local-note links entered public files. Inspect `.local/` ignore/tracking state without changing it.
- Handoff names task/revision, changed files, actual commands/results, skipped checks, limitations and one exact next action. No accuracy, production-readiness or human-validation claim.

#### Permissions and unresolved issues

The 2026-10-28 user request authorizes planning/documentation and bounded source research only. It does not execute F0. A later request to execute F0 can authorize the bounded sample inspection above, conditional on terms; `ready` alone grants no permission. Full datasets, dependencies, paid calls, provider uploads, infrastructure, Git mutations and external messages remain outside scope.

Open: data-specific rights; sample accessibility and exact schema; exact-variant compatibility; sufficient single-category coverage; reliable identity/supplier metadata; future acquisition size. Escalate only a required scope/identity/evaluation change or new authorization. Otherwise finish the unresolved branch with evidence. Do not silently weaken criteria or make F1 dependent on hidden notes.

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
Planning only, 2026-10-28: read the required project documents and explicitly requested local context; inspected file inventory, clean Git status, base commit, local ignore/tracking and runtime commands recorded above. Inspected the primary pages linked in F0. No data payloads, installs, paid calls, application code or Git mutations. Changed this plan and `docs/STATE.md`; no durable architecture decision changed.

## Review
Planner self-check only; no independent model or human review. Review F0 artifacts for identity semantics, rights, leakage and label provenance before making F1 ready.

Planning validation: inspected the full relevant diff; `git diff --check` passed (Git emitted only LF/CRLF conversion notices). A standard-library check confirmed relative Markdown links resolve in both changed files and no absolute user paths were added. Inspected public text for personal content and unsupported claims. Git status showed only the plan and STATE modified; `.local/` remained ignored and untracked. Application tests and dataset checks were not run because neither implementation nor data exists.

## Handoff
Next: a separately requested execution of **F0, plan revision 2**, in this checkout. Produce the audit and stop at `review`; do not execute F1. The central risk is source clusters not representing exact sellable variants. Unresolved data rights may require a documentation-only audit. No paid budget, dataset archive or dependency approval is recorded.

## Revision notes
- Revision 2 (2026-10-28): bounded F0 with primary-source leads, observed environment, conditional sample limits, reproducible outputs, negative-result path and explicit acceptance/handoff. Later tasks remain coarse; no feasibility execution claimed.
- Revision 1: documentation/publication boundary clarified; technical scope unchanged. No feasibility work has been executed.
