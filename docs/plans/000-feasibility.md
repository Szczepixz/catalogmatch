# Stage 000: data and baseline feasibility

- Revision: 6
- Status: in_progress (F0 documentation-only audit reviewed and done; F1-F4 remain draft)
- Created: 2026-10-27
- Owner role: planning chat, then implementation chat per selected task
- Updated: 2026-10-30
- Selected task: adopt offer eligibility policy and resolve PW line 5
- Execution: ten-pair model-assisted semantic review complete; eligibility policy v1 accepted (D15); rights unresolved; F0 remains done; F1-F4 draft

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
| F0 | done | [Documentation-only audit](../data-audit.md) reviewed; `needs_targeted_followup` | Documentation-only acceptance; source rights unresolved |
| F1 | draft | Identity policy, reviewed diagnostic data and split design | F0 |
| F2 | draft | Reproducible lexical/rule baseline and error report | F1 |
| F3 | draft | Comparable LLM baseline with observed cost and failure analysis | F2; explicit API/model budget authorization |
| F4 | draft | Continue, simplify, or change-domain decision; next product slice | F2/F3 evidence, or explicit incomplete-stage limitation |

### F0 â€” bounded data feasibility audit

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

The 2026-10-29 user request explicitly authorized F0 source/terms research and conditional sample inspection within this revision's limits. Source rights remained unresolved, so the documentation-only branch was used. The earlier planning authorization did not execute F0; `ready` alone grants no permission. Full datasets, dependencies, paid calls, provider uploads, infrastructure, Git mutations and external messages remain outside scope.

Open: data-specific rights; sample accessibility and exact schema; exact-variant compatibility; sufficient single-category coverage; reliable identity/supplier metadata; future acquisition size. Escalate only a required scope/identity/evaluation change or new authorization. Otherwise finish the unresolved branch with evidence. Do not silently weaken criteria or make F1 dependent on hidden notes.

### F1 â€” identity and evaluation design
Draft category-specific identity rules and annotation instructions. Inspect roughly 100-150 examples, including hard negatives, insufficient evidence and absent-product cases. Arrange owner review of ambiguous rules/labels rather than claiming model-generated labels are human-reviewed.

Design product-disjoint splits and a reference catalog. Preserve original benchmark results separately. State uncertainty and potential contamination. Output paths and schema are to be defined after F0.

### F2 â€” deterministic baseline
Select a minimal environment/dependency set, with required approval, and document actual setup commands. Implement a reproducible local baseline and meaningful offline tests. Measure candidate recall separately from matching and report difficult cases. API/UI/queues are out of scope.

### F3 â€” current LLM comparison
Select provider/model from current documentation, record explicit budget and call limits, and keep credentials outside artifacts. Compare a constrained LLM decision with the deterministic baseline on equivalent candidates. Include abstention, invalid-output handling and actual cost. Keep held-out data separate from prompt tuning. Do not use the same model as sole ground-truth annotator/judge.

If credentials/budget are missing, offline adapter tests may be prepared when authorized, but F3 remains incomplete. Never substitute mock results for live performance.

### F4 â€” decision
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

## F0 execution evidence (2026-10-29)

- Task/revision: F0, revision 2. Output: [data audit](../data-audit.md), recommendation `needs_targeted_followup`. Status `review`; F1-F4 remain `draft`.
- Changed files: `docs/data-audit.md` (new), this plan, `docs/STATE.md`. No decision/evaluation contract changed.
- Read root AGENTS, STATE, this revision and all F0 input documents. Inspected actual repository root, tracked inventory and initial clean status. Current base is `1a4292e`, superseding the planning-time base observation. `py -3.12 --version` returned Python 3.12.4. No personal notes read.
- Source checks: read publisher documentation, repository README/LICENSE, WDC home licensing and earlier corpus documentation; report records exact URLs and dated evidence. Used curl to inspect HTML example links without opening payloads. Initial sandbox curl failed with exit 6 (DNS); identical read outside the sandbox succeeded with exit 0. No sample requests or downloads.
- Result: no applicable data-specific grant established for local inspection. Documented schema remains unobserved. No category chosen, source rejected or alternative audited. No payload hashes, counts, identity diagnostics, overlap reconciliation or offline parse checks: all explicitly not run due to the rights gate.
- Deviation: none from the permitted documentation-only branch. Source review was bounded and completed within the 2-3 hour maximum; no exact elapsed-time measurement claimed. The report supplies an unexecuted conditional acquisition recipe, not tested downloader code.
- Validation: relative Markdown links in all three changed documents resolve; no required local-note links or absolute user paths. Public text inspected for personal context, restricted raw examples and unsupported claims. `git diff --check` passed. Full tracked diff and new report inspected; final status lists only the three intended files. `git ls-files -- .local` returns no tracked files; `git check-ignore -v -- .local/f0/probe` confirms the existing ignore rule. No application tests or dataset checks run.
- Validation tooling correction: the first ad hoc path check falsely matched `https:/` as a drive path and stopped before link checks. Added a preceding-letter boundary, verified URL/drive examples and reran the complete check successfully. No document content was changed to bypass the check.
- Review performed: author/model self-check only; no independent or human review. Rights, exact-variant compatibility, sample accessibility, category coverage and supplier provenance remain unresolved.

## Handoff

**F0, accepted at plan revision 2**, remains done. Revision 4 acquired both examples and completed structural inspection under the owner's limited exception to the rights gate; revision 5 completed model-assisted semantic review of PW lines 1-10. Rights remain unresolved. Revision 6 resolved eligibility under D15. Next: prepare a bounded diagnostic proposal with positive pairs, confusing variants, a candidate category and explicit data-use scope. No larger acquisition or F1 execution is authorized by this handoff.

## F0 artifact review (2026-10-29)

- Verdict: accepted for the explicitly permitted documentation-only branch; no blocking findings. F0 is `done`; F1-F4 remain `draft`, and `needs_targeted_followup` remains the recommendation.
- Checked the report against revision 2 acceptance criteria, the evaluation contract, decisions, workflow and documentation policy. Reopened primary sources S1-S5; the documented schema, label-origin/noise statements, offer-disjoint protocol and software-license scope support the report's bounded conclusions. No data-specific permission was established in these sources; this is not a finding that use is prohibited.
- Validation: inspected the tracked diff and full new report; `git diff --check` passed. A Python standard-library check passed for all 14 relative links in the three changed documents and found no absolute drive paths or required local-note links. Git status showed only the intended three documents; `.local/` has no tracked files and its probe path matches the existing ignore rule. Public content was inspected for personal context, raw restricted records and unsupported results.
- Limits: this is model-assisted artifact review, not human validation or a retrospective verification of all prior actions/time spent. No sample endpoints were requested, no payload acquired and no application or dataset tests run. The conditional acquisition procedure remains unexecuted. Rights, exact-variant compatibility, category coverage and supplier provenance remain open.
- Review changes: recorded this verdict and updated the state pointer; the audit evidence and evaluation criteria were preserved. Next action is the targeted rights follow-up specified above.

## Revision notes
- Revision 5 (2026-10-30): completed the separately authorized ten-pair semantic review in this chat; preserved source labels, F0's historical acceptance and F1-F4 draft status. No identity policy, category or evaluation contract selected or changed.
- Revision 3 (2026-10-29): completed the separately requested, documentation-only rights follow-up below; preserved F0's accepted review and F1-F4 draft status. No acquisition authorization or evaluation criteria changed.
- Revision 2 (2026-10-28): bounded F0 with primary-source leads, observed environment, conditional sample limits, reproducible outputs, negative-result path and explicit acceptance/handoff. Later tasks remain coarse; no feasibility execution claimed.
- Revision 1: documentation/publication boundary clarified; technical scope unchanged. No feasibility work has been executed.

## Targeted rights follow-up execution (2026-10-29, revision 3)

- Authorization/scope: at most 60 minutes of public documentation/terms research and updates to the existing audit, plan and STATE for the exact `sample_pairwise.json` and `sample_multi.json` URLs. The user prohibited both payload requests even if rights were confirmed, other data/archive downloads, contact, accepting terms, installs, paid calls, Git mutations, F1 and delegation. No personal notes read. One writer throughout.
- Starting reality: read AGENTS, STATE, the complete active plan, audit and documentation policy. Git HEAD was `1a4292e`; STATE and this plan were already modified, and the audit was already untracked. Inspected their content and tracked diff; preserved these existing F0/review changes. No implementation or dataset artifacts appear in the tracked inventory.
- Approach: reuse S1-S5; investigate publisher statements, research-purpose scope, the documented upstream chain and official explanations. Assess local inspection independently of later publication, redistribution and provider uploads; do not require a general-purpose license for the narrow activity.
- Checks/results: audit S6-S11 records publisher sections, exact href confirmation, PDC2020 and structured-data provenance, Common Crawl FAQ/ToU (dated March 7, 2024), authors' release announcement/paper, website repository README/root and benchmark license. Public searches and the issue/group views supplied no sufficient applicable grant. Access failures and limited issue/group coverage are recorded in the audit, not treated as negative proof. Documentation-only curl failed with sandbox DNS exit 6 and succeeded outside it with exit 0; no sample endpoint requests.
- Outcome: `unresolved` for local acquisition/inspection of both examples. Research invitations are positive evidence; upstream research-only scope and separate owner rights do not establish the needed downstream basis. Recommendation remains `needs_targeted_followup`. No category selected or data suitability established. F0 remains `done`; its historical artifact review is unchanged, and F1-F4 remain `draft`.
- Boundaries: no data acquired, parsed, hashed or inspected; no application/data tests run. No alternative dataset audit, legal-exception analysis or comprehensive historical-terms review. Existing acquisition recipe remains conditional and unexecuted. Stop after concrete leads rather than fill the timebox with repeated generic searches.
- One next action: project owner to request written WDC clarification for the two exact URLs, local storage/offline research inspection, applicable conditions and underlying merchant-content rights, using the audit's final next-action scope and existing F0 limits. No agent contact without separate authorization. Record the response in the audit before any separately authorized download task.

- Completion validation (2026-10-30, resumed after usage-limit interruption): inspected the complete audit and relevant tracked diff; 14 relative Markdown links resolve, with no required local-note links or absolute drive paths. Report/plan/STATE agree on unresolved rights, the next action and F0 done/F1-F4 draft. `git diff --check` passed; the untracked audit was also checked for trailing whitespace. Git status contains only the same three intended documents. No application or dataset tests run. Research evidence remains dated 2026-10-29; resumption only completed documentation validation, without new source research. The interruption is not counted as active research time.

## Bounded sample inspection (2026-10-30, revision 4)

User decision: retain WDC and the existing exact-variant project. The user authorized the proposed next step after discussion of unresolved rights: local acquisition and inspection of only the two publisher examples within F0 limits. This supersedes the previous task's payload prohibition and the unresolved-rights stop rule for this bounded inspection only. Rights remain `unresolved`; user authorization is not a data license. Do not publish raw records, send them to a model API, acquire archives or begin F1. Preserve the accepted F0 review.

Approach: verify publisher hrefs; download with standard-library bounded reads (1 MiB per response, 2 MiB total, 5 MiB decoded), reject redirects and compression/archives, record metadata and hashes, then parse locally and inspect at most 50 rows per file. Report structural aggregates without raw text. Reparse saved bytes offline. Update the existing audit and state; no dependency installation.

- Actual result: both HTTP 200 JSONL examples acquired, 55,960 + 33,135 = 89,095 bytes; 50 PW and 50 MC rows, 141 combined unique offers and 127 clusters, six overlapping IDs and no conflicting payloads. Hashes, UTC acquisition times, nullable schema and diagnostic probes are in the audit. Initial sandbox DNS failure consumed zero bytes; approved execution outside the sandbox succeeded.
- Local artifacts: a new ignored `.local/f0-inspection-20261030/` directory contains the acquisition script, failed zero-byte attempt metadata, successful original payloads/metadata and structural summary. No pre-existing local notes were read. The executed acquisition script is embedded in the public audit for reproduction with an arbitrary work directory; raw records are not versioned.
- Validation: independent offline reparse verified hashes, byte/row counts, pair-ID uniqueness/composition and combined offer/cluster counts. Inspected relevant diff and complete audit; relative links and whitespace checked. No application tests, fault-injection tests or model calls. No evaluation contract or identity policy changed.
- Limitation/deviation: the ten diagnostic cases received deterministic evidence probes only; raw-text semantic review and category selection remain pending. No human-reviewed labels or exact-variant correctness claimed. Research-only local inspection does not establish redistribution/provider rights.
- Next action: owner locally reviews PW rows 1-10 for exact-variant identity and ambiguity, separately from source labels, before a larger diagnostic acquisition is proposed. F1-F4 stay draft. This sample follow-up is ready for review with the semantic limitation explicit; the historical accepted F0 review is unchanged.

- Review support: generated an optional local HTML worksheet with the first 10 pairs, escaped raw values and initially collapsed source labels. It does not save judgments and is not a public artifact. The public procedure can regenerate the same rows from the hash-identified examples.

## Bounded semantic follow-up (2026-10-30, revision 5)

- Authorization: read only the specifically named local pair payload/metadata and optional HTML worksheet; analyze exactly PW physical lines 1-10 in this chat. No personal notes, additional models/services, downloads, merchant pages, installations, paid calls, delegation or Git mutations. The worksheet was not needed or read. This adds no license or broader acquisition permission.
- Starting reality: Git HEAD `fb94af5`; initial working tree clean. Read AGENTS, STATE, active plan, audit, evaluation contract and referenced project brief, decisions, workflow and documentation policy. Existing committed evidence and the historical F0 artifact-review verdict were preserved.
- Method/result: recomputed PW SHA-256 and byte length, matching audit and metadata (55,960 bytes); confirmed 50 physical lines and read only attributes from lines 1-10 before row-level supervision. Fixed nine `different_variant` and one `insufficient_evidence` judgments, then compared labels/cluster equality/flags. Required audit pre-reading disclosed aggregate labels, so this was not fully blinded. The audit is the source of truth for all ten hash/line/pair-ID locators, evidence and comparisons. No label corrections or human/gold claims.
- Findings: model/capacity/product-type/form-factor/design differences support the nine negative judgments. Line 5 lacks a defined left sellable item; its divergence from source 0 concerns insufficient evidence, not a proven source error. Compatibility mentions are not sold-item identifiers. Internal attribute contradictions in lines 4/10 do not affect their product/model mismatch. Category remains open; the all-negative, consecutive tiny sample cannot validate positives or dataset/system quality and must not be used for tuning.
- Changed files: existing audit, this plan and STATE only. No application, tests, dependency or decision/evaluation-contract changes. This completes the selected semantic follow-up, not F1 or a new acceptance review of F0.
- Validation: inspected the full relevant diff and public summaries for raw restricted text, personal content and unsupported claims. All 14 relative Markdown links resolve; no absolute drive paths or required local links in the three documents. Assertions confirmed ten ordered judgment rows, consistent revision/recommendation/next-pair pointers, F0 done and F1-F4 draft. `git diff --check` passed; status contains only these three intended documents. `.local/` has no tracked files and the pair payload matches the existing ignore rule. No application tests or probabilistic evaluation were run; no such implementation changed.
- Next exact action: obtain the owner's answer for line 5 / `67017951#5303451`: exclude family/editorial records with no sellable identity from future inputs, or retain them as `insufficient_evidence`? Record the answer in the audit before proposing further diagnostics. No larger sample is needed for that clarification and none is proposed or fetched now. Rights, positive-pair evidence, category coverage and offer-to-catalog design remain unresolved.

### Follow-up verification (2026-10-30)

- Verdict: no blocking findings in revision 5's bounded semantic report. Compared all ten rationales against the saved first ten PW records; the nine negative judgments and the unresolved sellable identity in line 5 are supported. This is a further AI review with prior access to the report and source labels, not blinded or human validation.
- Repeated checks: payload SHA-256 and 55,960-byte length match metadata and audit; 50 physical lines; all ten ordered locators, source labels, unequal clusters and hard-negative flags match. All 14 relative document links resolve; no absolute drive paths in the three changed documents. Relevant diff inspected and `git diff --check` passed. Local payload remains ignored and no local files are tracked.
- Scope: documentation and saved evidence verification only; no application tests, new downloads, live source-rights research or quality evaluation. Historical execution order and authorization are recorded provenance, not independently reconstructed by these checks. F1-F4 remain draft; the next action above is unchanged.

## Eligibility policy adoption (2026-10-30, revision 6)

- Authorization: owner explicitly delegated selection and adoption of the recommended eligibility rule. Adopted D15 / policy v1 in the decision register and evaluation contract; no further approval is pending for this rule.
- Result: exclude confirmed editorial/family records without a sellable item, preserve raw evidence and exclusion reasons, retain incomplete offers and uncertain eligibility. Report exclusions and both eligible-input and all-input automation denominators; freeze policy before final testing.
- Case resolution: PW line 5 left offer `67017951` is excluded from future eligible offers as `editorial_without_sellable_item`. Historical pair judgment `insufficient_evidence`, source label and ten-pair totals are preserved. This supersedes revision 5's pending owner question; it is not human annotation.
- Scope: documentation only; no runtime filter, data edits, new acquisition, paid calls or Git mutations. F0 remains done and F1-F4 draft. Prior working-tree changes were preserved.
- Validation: inspected the policy changes and affected audit/state/plan text; all 18 relative links across the five changed documents resolve, including the eligibility section target. Confirmed ten historical judgment rows and unchanged F0/F1-F4 statuses. `git diff --check` passed; no application tests apply to this documentation-only change.
- Next action: prepare the bounded diagnostic proposal described in the audit; rights, category selection and evaluation design remain unresolved.
