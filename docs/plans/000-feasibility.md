# Stage 000: data and baseline feasibility

- Revision: 19
- Status: in_progress (source selection closed; F0 done; F1 in progress; F2-F4 draft)
- Created: 2026-10-27
- Owner role: planning chat, then implementation chat per selected task
- Updated: 2026-11-12
- Selected task: implement F1-L annotation/exposure ledger (completed)
- Execution: 30-pair pilot complete; ALASKA Monitor selected under D16/D17; F1 structural loader verified; diagnostic review and protocol pending

## Objective
Determine whether one bounded product-matching task has usable data, defensible labels, and meaningful engineering trade-offs before building the application.

## Existing state and constraints
This repository contains project documentation and a local-note ignore rule only. Inspection on 2026-10-28 found an initialized Git repository at base commit `58da9e5`, with a clean initial working tree. No application, dataset, dependency manifest, virtual environment, tests or deployment were found. Local notes are ignored and not tracked.

Verified on Windows/PowerShell: `py -3.12 --version` reports Python 3.12.4, `py -3.12 -m pip --version` reports pip 24.0, and Git is 2.43.0.windows.1. `uv` was not found on PATH; `python` resolves to a WindowsApps alias, so use the verified launcher. These observations do not establish a reproducible project environment. F0 needs only the existing interpreter and standard library; do not install anything or use global third-party packages. Environment creation/package management for F2 remains open.

Read [project brief](../PROJECT_BRIEF.md), [decisions](../DECISIONS.md) and [evaluation contract](../EVALUATION.md). Exact variant identity is accepted; ALASKA Monitor is selected for feasibility under D16/D17. Input schema, final annotation release, splits and model remain to implement. Earlier environment observations above are historical.

## Timebox and permissions
Estimated stage effort: 20-30 human working hours; review scope if evidence collection exceeds it. This is not an automatic runtime or monetary allowance.

Do not initialize Git, install production dependencies, download large corpora/model weights, run paid APIs or provision infrastructure merely because this plan mentions them. Record concrete user authorization when needed and do independent offline work meanwhile. Public documentation and bounded source/sample inspection can support planning within the user's current request.

## Tasks
| ID | Status | Outcome | Dependency |
| --- | --- | --- | --- |
| F0 | done | [Documentation-only audit](../data-audit.md) reviewed; `needs_targeted_followup` | Documentation-only acceptance; source rights unresolved |
| F1 | in_progress | Reproducible ALASKA Monitor preparation, reviewed diagnostic subset and split design | D16/D17 and revision 9 handoff |
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

### F1 - monitor data preparation and evaluation design
Structural preparation and diagnostic review are implemented through revision 17. The catalog/split proposal and next bounded preparation task are in [revision 18](#f1-catalog-and-split-proposal-revision-18-2026-11-12). Use the hash-identified ALASKA Monitor archive, [current monitor policy](../EVALUATION.md#monitor-identity-policy-v1), and [pilot manifest](../data/alaska-monitor-pilot.json). No new source search or archive is needed.

1. Implement a standard-library loader/validator preserving raw records, source IDs, original assignments, duplicate counts and conflicting memberships. Apply known group quarantines (054/063 structural conflicts; 032/205 pilot disagreements) to trusted-label preparation, without rewriting source data. Test duplicate/conflicting assignments, missing records and preservation of model suffixes using clearly synthetic fixtures.
2. Produce a reproducible, versioned diagnostic set of approximately 100-150 pairs, separating source labels, eligibility, project judgments, rationale and reviewer origin. Include supported positives, confusing variants, missing attributes and contradictions. Sampling limits and any additional chat/raw-data exposure must be explicit in the execution scope; source selection approval is not an unlimited model-service budget.
3. Define reference-record selection, validated identity groups, identity-disjoint development/frozen-test partitions and absent-product construction. Exclude the 41 semantically exposed pilot source groups and linked aliases from the final custom test. Automated structural parsing and fixed sampling are not themselves independent annotation or a frozen evaluation.
4. Obtain independent checking of reference judgments before making final quality claims. AI-only diagnostics may support development but are not human gold. Record original benchmark and custom-protocol results separately.

Acceptance: reproducible preparation command, meaningful offline correctness tests, auditable diagnostic manifest, explicit split/catalog protocol and honest annotation status. F1 is not complete merely because a loader runs; F2 baseline work starts after these inputs are defined. Update verified commands in README/AGENTS when executable code exists.

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

Source selection is closed at revision 9: ALASKA Monitor and identity policy v1 are accepted for bounded local feasibility. F0 remains historically done; F1 data preparation is ready, not complete. Execute the F1 tasks above using the audit and pilot manifest. No publisher contact, additional source search, paid calls or raw redistribution is required or authorized.

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

## Remaining-sample diagnostic proposal (2026-10-30, revision 7)

Historical proposal status: prepared before authorization; execution subsequently completed below. Starting commit `8e1cc12`, clean working tree. The user requested the recorded next step: preparation of a bounded diagnostic proposal. Earlier chat semantic authorization covered exactly ten pairs; this proposal explicitly requests extending it to the remaining saved PW rows. Rights remain unresolved; this is no new license or acquisition authorization.

### Question and scope

Can the existing example provide supported same-variant cases and confusing different variants within one candidate category, or is its coverage insufficient? The audit reports 46 source-negative and four source-positive pairs overall, with ten negatives already reviewed. Thus the remaining 40 rows contain four source positives and 36 negatives; these are sampling facts, not trusted exact-variant judgments.

- Input: saved `sample_pairwise.json`, 55,960 bytes, SHA-256 `8c023e0f5571a95a833c431cb94d0f909db3c4bc6e0993d01c5b7488e356d90b`, and its acquisition metadata. Verify hash and 50 physical lines before reading attributes.
- Maximum new semantic exposure: physical lines 11-50, 40 original pairs / 80 offer occurrences, processed in four batches of ten in source order. Include every row, even if excluded or unresolved; do not replace difficult cases. Reference previous lines 1-10 only through the existing audit.
- Zero new dataset downloads, merchant-page visits, external-service calls, paid calls or installations. No MC payload inspection or synthetic/cross-row pair construction. Analysis uses this chat; do not describe that as offline-only processing. Local scripts may use the existing Python standard library.
- Publish original summaries, counts and hash/line/pair/offer locators only; preserve raw payloads locally. No raw titles, descriptions or merchant contact data in versioned artifacts.

### Review procedure

1. Separate row-level supervision (`label`, cluster IDs and hard-negative flag) from the attribute view. Review brand/title/description/price/currency first. Prior knowledge of aggregate labels and previous judgments prevents a fully blinded claim.
2. For each side, record observed product type and eligibility under D15 v1: eligible, excluded with evidence, or uncertain. Missing attributes alone do not justify exclusion. Product types are analyst observations, not source category metadata. Preserve identity-bearing conflicts and distinguish compatible devices from sold items.
3. Record `same_variant`, `different_variant` or `insufficient_evidence`, decisive attributes and remaining uncertainties before comparing source supervision. A positive requires evidence of the same specific sellable model/configuration and resolution of observed capacity, form-factor, pack, condition or other relevant variant distinctions. Shared brand/family, absence of a contradiction and source label 1 are insufficient. If a new category-specific identity decision is necessary, retain `insufficient_evidence` and list the decision for F1 instead of inventing a policy.
4. For an excluded side without a defined sellable item, retain the historical/source pair and record an unresolved identity judgment separately from eligibility. Do not count exclusion as a correct negative or catalog absence. Record assessment origin as AI-assisted, never human/gold annotation.
5. Compare source supervision after each batch's judgments. Report discrepancies as evidence disagreements, not automatic label corrections. Define confusing negatives from observed shared product type/family and a decisive variant conflict, not from the source hard-negative flag alone.
6. Aggregate all 50 pairs with separate previous/new counts. Deduplicate offers by ID for eligibility counts; report pair occurrences separately and flag repeated identities. Preserve all exclusions and uncertain cases, with explicit denominators. Do not compute matching accuracy or treat these annotations as gold.

### Category recommendation and stopping rules

Produce one coverage table by observed product type: pair count, unique offer count, source-label mix, the three review judgments, eligibility exclusions/uncertainty and confusing-negative count. Cross-type pairs remain a separate slice and do not inflate within-category coverage.

Recommend at most one category for further investigation only if it contains at least two supported positive pairs and two confusing negative pairs with clear sellable identity evidence, and those pairs are not merely repeated unordered offer-ID combinations. This is a pragmatic discovery threshold, not statistical validation or an F1 acceptance criterion. Report distinct identities and any correlation even when the threshold is met. Prefer the category with more supported positives, then more confusing negatives; break ties by first occurrence. Do not combine unrelated types to reach the threshold. Owner confirmation is required before adopting the category or its final identity rules.

If no category meets this threshold, report insufficient category evidence and the precise missing slice; stop without downloading or searching for more data. If hashes/schema/counts disagree with the recorded input, stop and report the discrepancy. Ambiguous cases are retained, not a reason to expand the sample. A category recommendation alone cannot make F1 ready: rights, independently checked labels, sufficient diagnostic coverage, identity grouping and offer-to-catalog design remain prerequisites.

### Outputs, validation and handoff

- Update the existing audit with 40 locatable judgments, eligibility evidence, category coverage, limitations and one next action. Update this plan and STATE; create no second audit or application scaffold.
- Reconcile exactly 50 historical-plus-new pair rows, source-label counts and unique offer counts against the saved payload. Validate locators, category totals and exclusion denominators; check public text, relative links and `git diff --check`.
- Keep all inspected identities outside a future custom frozen test and prohibit prompt/threshold/model tuning on this unknown-split sample. No baseline implementation, quality metric, source-label correction or F1 execution follows automatically.
- Proposal preparation performed documentation inspection only; no new raw records were read and no semantic judgments were added. The existing evaluation contract and D15 were preserved.
- Preparation validation: inspected changed scope and handoff text; 17 relative links resolve and the new proposal anchor exists. Confirmed revision 7, F0 done/F1-F4 draft and the unchanged ten historical judgment rows. `git diff --check` passed. No application tests or data-quality evaluation were run.
- Next exact action: obtain authorization to read and analyze PW lines 11-50 in this chat under the bounds above despite the recorded unresolved rights, then execute this proposal. No additional service or acquisition permission is requested.

### Authorized execution and result (2026-10-30)

- Owner explicitly approved the further analysis. Scope: saved PW lines 11-50 in this chat under revision 7, preserving unresolved rights and prohibiting new acquisition/additional services. Starting HEAD `8e1cc12`; the three existing proposal edits were preserved.
- Verified saved metadata, H SHA-256, 55,960 bytes and 50 physical lines. Reviewed four ten-row batches, recording attribute judgments before reading each batch's supervision. Prior aggregate knowledge prevents a blinded claim. No previous raw lines 1-10 were semantically reread; their existing audit summaries supplied historical types/eligibility. No MC attributes or personal notes were read.
- Result: new 35 different / 5 insufficient; combined 44 different / 6 insufficient / 0 same across 50 pairs. All four source positives remain unresolved because configuration or bundle evidence is missing. Row 36 adds uncertain eligibility, not exclusion. D15 yields 95 eligible, one uncertain and one excluded unique offer among 97 (96 retained); occurrence counts are 98/1/1 among 100. No source labels changed or gold/human validation claimed.
- Category outcome: none meets the predeclared two-positive/two-confusing-negative discovery threshold. The audit contains 40 new locators/rationales, category counts, repeated-ID accounting and explicit missing evidence. No rule or threshold was relaxed, no category selected and no F1 work executed.
- Local scratch records fixed judgments before supervision comparison; public reproduction needs the hash-identified sample and documented procedure, not those scratch files. No code/dependencies, additional services, downloads, merchant visits, paid calls or Git mutations.
- Validation: checked all 50 public locators/judgments against saved records and fixed assessments; verified 46/4 source labels, cluster equality, 50 unique unordered pairs, 97 unique offers and identical repeated-ID payloads. Category totals and eligibility denominators reconcile. All 16 relative links in changed documents resolve; no absolute drive paths or full raw titles/descriptions in the new report. Local scratch files are ignored and no local files are tracked. Inspected report/state/plan changes; `git diff --check` passed. No application tests, live source research, human annotation or probabilistic quality evaluation were run.
- Next action: documentation-only comparison of bounded WDC continuation versus one alternative for permitted use and category-specific positive/negative variant evidence. No automatic expansion of acquisition. F0 remains done and F1-F4 draft.

## Documentation-only source comparison (2026-11-01, revision 8)

- Scope/authorization: user requested the recommended next step. Compare WDC continuation with exactly one alternative, ALASKA, using primary documentation only. Starting HEAD `49da153`, clean working tree. No dataset downloads, raw-record inspection, external messages, installations, paid calls, delegation or Git mutations.
- Approach: recheck WDC publisher documentation and repository license; inspect ALASKA author's repository README/LICENSE and paper. Compare category access, label provenance, variant evidence, catalog/split work and rights. Keep publisher claims separate from measured local evidence. This task does not adopt a category or change D01/D15/evaluation requirements.
- Result: the audit records dated sources and recommends ALASKA Monitor for conditional investigation rather than a larger mixed-category WDC sample. Its technical promise does not establish exact-variant ground truth. MIT scope for merchant-derived records and the canonical archive/version need clarification; observed main/master README download links differ. Archive endpoints were not fetched.
- Validation: inspected the relevant diff and source-backed claims; 16 relative links resolve, 50 historical judgments are preserved, and F0/F1-F4 statuses are unchanged. `git diff --check` passed; only the audit, plan and STATE changed. No local files are tracked. No application tests or dataset checks apply to this documentation-only task. The GitHub main tree page returned a tool cache error; raw README/LICENSE and the paper were readable. No archive availability or license completeness is claimed.
- WDC is retained as historical diagnostic evidence, not declared generally unsuitable. No category passed the prior local threshold; documentation cannot substitute for that validation. F0 stays done and F1-F4 draft.
- Next exact action: owner obtains the narrow ALASKA clarification using the unsent draft in the audit (license scope, canonical archive and label granularity). Sending requires explicit authorization; no message was sent. After a response, define a bounded acquisition/inspection task rather than silently extending the WDC exception to ALASKA.

## Final source inspection (2026-11-01, revision 9)

Authorization: owner approved ALASKA inspection and delegated the steps needed to close source selection. This supersedes the pending publisher-contact gate and permits one Monitor archive plus local parsing and a 30-pair analysis in this chat. No author contact is required. This is a bounded student-project decision, not a new data license or permission for raw redistribution, paid services or further provider uploads. Existing uncommitted comparison edits are preserved.

Pre-inspection approach:
- Download one Monitor archive from the author's linked hosting, at most 8 MiB transferred; allow at most 128 MiB decompressed tar stream and 25,000 members, at most 1 MiB per data member. Inspect members without extracting paths; no code in the archive is executed. Record endpoint, time, bytes and SHA-256. A data-only metadata request may pin the publisher revision.
- Apply monitor identity policy v1 below before reading sample records. Parse the ER ground truth, retain provenance and contradictions, and select 15 within-entity pairs across distinct entities/sources plus 15 lexically similar between-entity pairs. Fix the sample before semantic judgments; no replacing ambiguous cases. Seed 20261101 and exact selection details will be recorded with the results.
- Accept the source for feasibility if the sample supplies at least two supported positives from distinct source entities and two supported confusing negatives, with traceable annotations and usable identity-bearing attributes. This is a discovery gate only, not precision certification or completed F1. Otherwise give a final unsuitable/limited verdict without another source search. Do not relax the gate after inspection.

Monitor identity policy v1 (fixed before inspection):
- Target the exact monitor catalog variant, not an individual physical unit or merely a family. Preserve brand, complete model/part number including suffixes, size, resolution, refresh rate, panel/touch configuration, color and explicitly sold bundle/quantity/condition.
- Matching explicit manufacturer and complete model identifiers on both sides can support `same_variant` when identity-bearing evidence is consistent. Case, spacing and formatting-only punctuation may differ; do not drop suffixes or equate distinct part numbers without evidence. A compatible-device mention is not a sold-item identifier.
- Do not require every possible specification to be repeated once the complete model is established. Missing price, an incidental specification or condition on both sides is not alone a contradiction or an automatic abstention. This does not label the items new or invent accessory contents. The evaluation is catalog-variant linkage, not verification of identical commercial terms.
- An explicit variant/condition/bundle qualifier on one side whose compatibility cannot be established on the other requires `insufficient_evidence`. Conflicting complete models or explicit variant attributes support `different_variant`. Material internal contradictions, truncated identifiers or unresolved suffix equivalence require `insufficient_evidence`; price alone never decides.
- Apply D15 separately. Source entity IDs remain supervision, never identity evidence. Preserve benchmark labels and record AI judgments independently. This clarifies future monitor evaluation; it does not relabel the historical WDC review.

### Revision 9 execution outcome

- Download succeeded from the publisher-linked GitHub archive: 3,704,214 bytes, SHA-256 recorded in the audit. Initial sandbox DNS failure transferred zero bytes; approved curl retry succeeded. Decompressed tar and member sizes stayed within bounds; no archive paths were extracted or executed.
- Structural parser found 16,662 JSON records and 2,342 ER rows. Exact duplicate assignments account for 60 rows; nine records have conflicting membership in groups 054/063. Initial no-conflict assertion failed, and raw CSV rows reproduced the issue. Quarantining both full groups (10 records) before selection is the material pre-sample deviation; source data and failure evidence are retained.
- Fixed selection: seed 20261101, 15 cross-source within-entity pairs plus 15 title-Jaccard between-entity pairs. Manifest fixed before semantic review. The latter all happen to be same-source and are biased by boilerplate; no cross-source performance claim. 59 records / 41 source entities were exposed semantically.
- Result: 4 same, 17 different, 9 insufficient across 30 pairs. Within-source-group stratum: 4/2/9; between-group: 0/15/0. Two source-positive contradictions additionally flag groups 032/205 for trusted-label quarantine; they remain in pilot totals. Eligibility: 57 eligible, 2 uncertain retained, 0 excluded unique records. All judgments are AI-assisted, not blinded or human gold.
- Gate passed without changing its two-positive/two-confusing-negative threshold. D16 selects ALASKA Monitor for feasibility and D17 adopts monitor identity v1. Source discovery is closed; noisy annotations require subset review, not automatic rejection or another source hunt. Previous WDC judgments are preserved.
- Changed artifacts: existing audit, evaluation contract, decision register, plan and STATE; new public pilot manifest contains only locators, hashes and original summaries. Raw archive/scratch data remain local. No application, dependency, paid call, external message or Git mutation.
- Validation: a separate archive pass replayed all 30 selections, verified archive/record hashes and source assignments, reconciled counts and confirmed the discovery gate. All 25 Markdown relative links/anchors resolve; 50 WDC rows remain unchanged. Reviewed relevant changes and public manifest; `git diff --check` passed. No application tests or probabilistic evaluation. A documentation edit initially failed because an old heading contained mojibake; retry matched its stable heading prefix and preserved unrelated historical content.
- Next action: implement F1 loader/validator and diagnostic preparation as specified above. Do not reopen publisher-contact or generic rights research as a prerequisite under the owner's accepted bounded scope. Public redistribution and later external-provider processing remain separate decisions.

## F1 structural preparation (revision 10, 2026-11-04)

Implement a bounded standard-library archive reader, preserve source rows and raw attributes, separate quarantines and review candidates, and verify the JSON CLI against synthetic failures and the audited archive. Pair sampling and evaluation design remain pending.

Verified with Python 3.12.4 and no dependencies. The CLI reproduced the audited hash and all requested counts, including nine conflicting records and zero missing references. Full-group exclusions cover ten records for membership conflicts and seventeen for AI-assisted disputes. The 2,246 remaining assignments require substantive review. The local report contains identifiers and aggregates only.

Four offline synthetic tests passed, including malformed inputs and all four resource limits. The first sandbox run could not create fixture files in the temporary directory. The same command passed with temporary-directory access. Next, specify reproducible strata and sample 100-150 diagnostic pairs for independent review. Keep pilot exposure separate before designing catalog and identity-disjoint splits.

## F1 diagnostic selection (revision 11, 2026-11-04)

Fixed 120 cross-source pairs from the audited archive and loader candidates. Exclude both structural and disputed groups, exact pilot pairs and reused endpoints. Select sequential quotas of 40 with deterministic SHA-256 ordering. Within-group sparse anchors have the fewest raw fields first. Between-group anchors take their highest nonzero title-token Jaccard partner. The remaining within-group pairs use hash-ranked anchors and partners. These proxies seek missing evidence, confusing variants and possible matches. Actual identity, contradictions and eligibility require review. The quotas do not estimate population prevalence.

The [manifest](../data/alaska-monitor-diagnostic.json) contains only locators and audit metadata. Left/right flags distinguish previously inspected records from membership in previously inspected source entities. Six pairs touch a pilot record and 33 touch a pilot entity, including those six. No raw attributes were sent to a reviewer or additional service. The [CLI](../../README.md#run-locally) emits an interleaved worksheet without audit fields.

Validated archive replay, all source assignments, quarantines, exposure flags, quotas, 240 unique records, zero pilot pair repeats and worksheet alignment/blank annotations. An initial verification script used the wrong loader field name; rerunning against the preserved assignments passed. Next action is independent substantive review. Catalog construction and final identity-disjoint splitting are deferred.

## F1 returned worksheet (revision 12)

The owner supplied a first AI review from a separate chat and project. Preserved the received CSV locally (SHA-256 `e9e2849b3e41fbf91c4f1231b8dd9304497579167f5839b75f5986a986bef018`). All 120 manifest IDs appear exactly once, with complete answers and allowed categorical values. All 240 eligibility assessments are eligible. The CSV establishes the reported judgments; reviewer isolation and semantic correctness were not independently verified.

| Source stratum | Same | Different | Insufficient |
| --- | ---: | ---: | ---: |
| Within sparse | 9 | 4 | 27 |
| Within general | 10 | 5 | 25 |
| Between title overlap | 0 | 38 | 2 |

Pilot exposure (same/different/insufficient): shared pilot record 3/2/1, pilot entity only 3/11/13, neither 13/34/40. Next, adjudicate nine explicit within-group disagreements (D023, D025, D033, D034, D036, D040, D056, D058, D072) against the offers and D17. Preserve the 54 insufficient judgments separately. Source assignments and quarantines remain as recorded. Final split design is deferred.

## F1 disagreement adjudication (revision 13)

Scope: AI-assisted, unblinded second assessment of the nine source-positive / reviewer-different rows only. The pinned review CSV hash, archive hash, manifest IDs and both original record objects per case were checked locally. Field-specific probes extracted identifiers and relevant qualifiers. No external lookup, new provider call for raw records or human verification. The first review remains immutable.

| Pair | Source entity | D17 assessment | Decisive evidence or unresolved question |
| --- | --- | --- | --- |
| D023 | 161 | different_variant | The left feature block and right manufacturer part field give distinct complete Acer codes ending in .003 and .001 despite the shared V196WL model. |
| D025 | 002 | different_variant | The left title identifies E779029 and the right MPN identifies E700813 within the 1515L family. |
| D033 | 021 | different_variant | Both titles name 1739L but specify distinct Elo identifiers E734455 and E012584. |
| D034 | 192 | different_variant | The W2072a titles specify different HP product codes A3M50AA and B5M13AT. |
| D036 | 156 | insufficient_evidence | Both name U2713HM. Left product colour is black while right case colour is silver. The fields can describe different surfaces of one monitor; a distinct configuration is unresolved. |
| D040 | 075 | different_variant | The left title offers a lot of five Grade A monitors. The right names a Grade C monitor stand. Multiple compatible model references cannot establish the same sold item. |
| D056 | 114 | different_variant | The left title gives M170 and part code 41 91377 117; the right model and MPN give M1700SS and 11-91378-227. |
| D058 | 105 | insufficient_evidence | Both name L1710. The right title explicitly says quantity two; the left does not establish sold quantity. A singular model name alone does not establish a one-unit bundle. |
| D072 | 163 | different_variant | Both MPN fields give complete V246HL codes with different endings, .004 and .005. |

For subsequent trusted-label preparation, hold source entities 161, 002, 021, 192, 075, 114 and 163 out of automatic same-identity grouping. This is a conservative group-level hold, not a blanket different-variant label. Keep D036 and D058 unresolved at pair level. The versioned sampling input and its original quarantine remain fixed for replay. Apply these later holds separately when building a reviewed set. The other 111 first-pass judgments were carried forward without re-review. The resulting diagnostic tally is 19 same, 45 different and 56 insufficient. Next, independently check the 19 provisional positives before using them as reference links. Catalog and final split remain pending.

## F1 independent review packet (revision 14)

Prepared a local packet with all 19 first-pass positives and ten masked controls. All nine within-group first-pass negatives were excluded by the adjudicated-case exclusion, leaving no eligible within-group negative controls. Therefore the five different-variant controls come from the between-group title-overlap stratum. The five insufficient-evidence controls come from within groups. Controls are masking material, not an accuracy sample.

Using revision 12 judgments and the frozen diagnostic IDs, take the first five per control pool in ascending SHA-256 order of the UTF-8 string `f1-r14-v1|control|ID` (substitute the original ID). Interleave all selected IDs by the same ranking with `order` replacing `control`; assign R001 through R029. Keep the mapping and first judgments outside the reviewer packet.

Reopened the ZIP and checked its three entries, all 58 original offer objects and side orientations against the pinned archive and manifest, all 29 blank worksheet rows, control quotas, excluded IDs and the separate comparison key. Both generated files are Git-ignored. Next, obtain the completed worksheet from a reviewer without prior results and compare it using the private key.

## F1 second AI review (revision 15)

Pinned the returned CSV locally, SHA-256 `c8966d6ef5fc284bd124115552e197a4c70a5d10594112e0b6ec4ed8e8f892ae`. The 29 unique IDs matched the worksheet and private key. All fields were populated, all origins AI, and all 58 eligibility decisions eligible. Reviewer isolation was not independently verified.

Fifteen provisional positives received a second same-variant judgment. The cited model identifier occurs on both sides of each pair. These are AI-supported diagnostic links, pending independent human verification. Pair and shared identifier: D011 EA193MI-BK, D013 E178FPB, D019 I2367FH, D024 PA249Q, D049 E241i, D066 P2214H, D070 U2913WM, D073 U2414H, D076 VG278HE, D078 VK278Q, D079 PQ321QE, D085 S2440L, D092 25UM65-P, D105 P2314T and D112 V226WL (also matching UM.EV6AA.002).

Hold four pairs out of reference links pending adjudication. Both reviewers identify the same monitor models. For D035 and D065 the second reviewer questions service duration, for D068 whether both offers include the same service coverage, and for D099 whether the reported operating and maximum power figures are comparable. The second judgments are insufficient evidence in all four cases. Explicit service bundles versus ordinary warranty language, and the materiality of power measurements, need a D17 check before changing the first labels.

All ten masking controls reproduced their first judgments (five different and five insufficient). This purposive comparison does not estimate accuracy. Keep revision 13 decisions intact and defer final splitting.

## F1 four-case adjudication (revision 16, 2026-11-12)

Historical outcome: revision 17 below supersedes the D035/D065 holds and closes the service-policy question. This section preserves the evidence, reasoning and totals under the prior policy.

Scope: local, unblinded AI-assisted adjudication of D035, D065, D068 and D099 only, under unchanged D15/D17. Both original review CSVs remain immutable: each first judgment is `same_variant`, and each second judgment is `insufficient_evidence`. The decisions below form a separate adjudication layer; they are neither human verification nor a final gold set. No external lookup, additional service processing, final split or Git mutation was performed.

Integrity: recomputed the archive SHA-256 against acquisition metadata and the diagnostic manifest (`9084b8998d5afa283865dfcf8e1f3cc4137f6befbe431903a4d83df4b3f7b45d`) and both CSV hashes recorded in revisions 12 and 15; all matched. Replayed the complete 120-pair manifest with the existing loader/selector and obtained exact equality. Checked the 120 first-review IDs and 29 second-review IDs, and regenerated all 29 private-key mappings using revision 14's control/order algorithm, including first-label agreement. The diagnostic manifest SHA-256 is `479d543c58547ca86dac86ea896367416321649a9513e09aef2b942aed8f90a3`; the private-key SHA-256 recorded at this inspection is `a7adfecd38070ddd1e2b1c311092e27c63555d898fd7ac5326419bccea015267` (a new fingerprint, not a comparison to an earlier pinned hash). Raw records were processed locally with targeted field probes; no full offers are reproduced here.

### Consistent service interpretation

All three left offers use the same generic reliability statement naming Premium Panel Guarantee and Advanced Exchange Service, without a duration, upgrade, separate service SKU or explicit extra purchase. That statement alone does not establish an additional sellable service bundle. D035 and D065 differ from D068 because their right offers explicitly list three years of those services under `bundled with` and in the product description, while also listing a three-year manufacturer limited warranty. Thus the records establish advertised included coverage, but do not establish whether it is an additional package or merely the manufacturer's ordinary coverage. Neither a field name alone nor the shared monitor model settles that distinction. D068 has no explicit additional package on either side; absent warranty details alone do not establish a variant conflict.

The precise policy gap for owner decision is whether manufacturer coverage advertised as a bundle, without evidence of an upgrade or separate service SKU, is identity-bearing, and whether an omitted term can be treated as incidental in that situation. D17 explicitly handles ordinary cable inventories but does not settle this service boundary. No blanket warranty exemption or assumed default term is adopted here. D035/D065 remain unresolved rather than silently extending the policy. For a genuinely additional service package, an unknown term on the other side would leave bundle compatibility unresolved under existing D17.

| Pair / second ID | Adjudication | Evidence from both offers and assessment of the reviews | Reference-set consequence |
| --- | --- | --- | --- |
| D035 / R003 | insufficient_evidence | Left identifies P2314H and names both protection services without a term. Right identifies P2314H, advertises both for three years as bundled coverage and also reports a three-year manufacturer limited warranty. The first review correctly identifies the shared model/services but does not settle package equivalence. The second correctly identifies the missing term; it does not prove an extra package exists. Resolve the service-policy gap before promoting the pair. | Keep out of positive reference links; retain as unresolved, not a negative or a group-wide exclusion. |
| D065 / R018 | insufficient_evidence | Left identifies P2414H and names both services without duration. Right identifies P2414H and specifies three-year bundled coverage alongside a three-year manufacturer limited warranty. The same evidence and reasoning as D035 apply; matching screen/model evidence does not settle the service-policy boundary. | Keep out of positive reference links; retain as unresolved, not a negative or a group-wide exclusion. |
| D068 / R017 | same_variant | Left identifies P2214H, 21.5-inch display and generic protection language. Right identifies P2214H with 22-inch nominal / 21.5-inch viewable sizing, matching Full HD and 8 ms specifications, and no explicit service bundle. The first review's model/size reconciliation is supported. The second converts generic protection language into an additional package without offer evidence. Missing ordinary coverage details do not by themselves contradict the complete model. | Add one provisional AI-adjudicated positive link, distinguished from the 15 concordant AI positives; independent human verification remains pending. |
| D099 / R008 | insufficient_evidence | Both identify E2014H, 1600 x 900 and 5 ms; nominal/viewable sizes agree. Left `power description` reports operating consumption of 22 W. Right `power consumption` reports a maximum of 14 W, with 0.5 W standby (matching the left's 500 mW standby). The 22 W and 14 W figures concern active operation, not standby or power-adapter ratings; neither record supplies measurement conditions. The first review omits this discrepancy. The second accurately flags it. The data do not justify reinterpreting 14 W as typical, assuming a typo, or asserting distinct variants; nor do they establish comparable measurements that reconcile the conflict. | Keep out of positive reference links pending evidence resolving the active-power discrepancy; no different-variant or source-group exclusion follows. |

D15: all eight records remain eligible product offers. Missing service terms or inconsistent power specifications do not establish editorial/family-only content. Preserve source assignments, the fixed sampling manifest, all revision 13 holds and its D036/D058 unresolved decisions. The effective adjudicated diagnostic tally is now 16 same, 45 different and 59 insufficient (120 total); the 16 positives comprise 15 concordant AI assessments and one disputed case resolved by this unblinded AI adjudication. Historical revision 12/13 totals and both original reviews remain unchanged. These are diagnostic annotation counts, not accuracy estimates.

Validation: archive/CSV hashes, exact manifest replay and complete deterministic ID mapping passed. A targeted D099 display probe initially hit the Windows console encoding limit; rerunning with UTF-8 succeeded without changing inputs. Documentation diff/whitespace and relative-link checks passed; the preserved input fingerprints were rechecked after editing. No software tests or probabilistic evaluation were run because only documentation changed. Next action: owner decision on the narrowly stated service-policy gap for D035/D065; D099 still requires reconciliatory evidence. Stop after these four cases. Catalog design, final splitting and Git operations remain deferred.

## F1 approved coverage clarification (revision 17, 2026-11-12)

The owner explicitly accepted the proposed manufacturer-coverage rule and re-adjudication of D035/D065. Recorded the durable rule as D17 policy v1.1 in the [evaluation contract](../EVALUATION.md#manufacturer-coverage-v11) and [decision register](../DECISIONS.md). This closes revision 16's policy gap without assuming warranty entitlement equality or a default coverage term. No additional raw-data inspection or external processing was needed; the adjudication uses the field evidence and verified mappings recorded in revision 16.

| Pair / second ID | Current adjudication under v1.1 | Evidence and reference-set consequence |
| --- | --- | --- |
| D035 / R003 | same_variant | Both offers identify P2314H and the same named protection services. The right specifies three years alongside a three-year manufacturer limited warranty; the left omits duration. Neither establishes an explicit extension or separately offered service. Under the approved rule, the bundle field and missing term do not block the established monitor identity. Promote to a provisional AI-adjudicated positive link; do not infer a three-year entitlement on the left. |
| D065 / R018 | same_variant | Both offers identify P2414H and the same protection services. The right specifies three years alongside a three-year manufacturer limited warranty; the left omits duration. No explicit extension or separately offered service is established. Apply the same rule as D035 and promote to a provisional AI-adjudicated positive link without filling in the missing term. |

D068 remains `same_variant`; D099 remains `insufficient_evidence` because its active-power discrepancy is unresolved. Each original first/second review remains `same_variant` / `insufficient_evidence`; the owner approved policy, not independent human annotations. Revision 16's decisions and historical totals remain available. Current diagnostic totals are **18 same / 45 different / 57 insufficient** (120): 15 concordant AI positives plus three AI-adjudicated positives. All D15 eligibility decisions, revision 13 holds and unresolved D036/D058 cases, source assignments and sampling inputs are unchanged. This is not a gold set or a measured quality improvement.

Validation: inspected the documentation diff, checked whitespace and relative links/anchors in all four changed documents, verified tally arithmetic, and rechecked the two preserved review CSV hashes. No software tests or quality evaluation were run for this documentation-only policy update. Scope complete; no final split or Git mutation. Next action, when selected: resolve D099 only if suitable evidence becomes available; otherwise retain its insufficient label. Catalog/split work remains deferred.


## F1 catalog and split proposal (revision 18, 2026-11-12)

Status: design complete, protocol proposed for review; no catalog, identity assignment, reservation or final split has been generated. The owner requested this design step, not execution of the split, a commit or further semantic review. D15, D17 v1.1, D07 and the evaluation contract remain unchanged. This section specifies a custom feasibility protocol, not the original ALASKA benchmark or an approved new public API.

### Observed capacity and design constraints

Read the project brief, workflow, evaluation contract, decisions, loader/selector and public pilot/diagnostic manifests. A bounded local structural pass verified the archive hash against both manifests and inspected assignments only; no new raw offer fields were displayed or semantically reviewed. The working tree was clean at the start of this task.

- The pilot marks 41 source groups exposed; the diagnostic manifest touches 103, including 20 pilot groups. Their union is **124 exposed source groups**. All 240 diagnostic endpoints and the 30 pilot pairs are development material, regardless of review outcome.
- There are 232 source groups. The four original quarantines and seven revision 13 holds cover 11 groups; two fall outside the exposed union. Removing exposure and holds leaves **106 unreviewed source groups containing 779 distinct assigned records**, with **60 groups spanning at least two source hosts**. This is a structural planning pool before alias, duplicate, eligibility and identity checks, not 106 identities or 60 valid test cases. Unassigned archive records are outside the initial reviewed catalog; count/report this scope rather than treating them as negatives or absent products.
- The 18 positive diagnostic pairs touch 17 source groups. D013 lies in held group 075: its positive pair label does not release the group. D066 and D068 share group 122 but have disjoint endpoints; they must not be merged solely because of the source group. Current code selects pairs and reports original quarantines; it does not implement revision 13 holds, adjudication overlays, identity validation or splits.
- The 120-pair effective tally stays 18/45/57. Diagnostic balance is purposive. Human-independent reference checking and the number of usable unseen identities are still unknown. D099 remains insufficient and does not block designing the protocol.

### Three separate evidence layers

1. **Pair assessment:** immutable first/second observations plus dated adjudications with policy version, origin, evidence field locators and supersession links. Keep all 120 pairs, including 57 insufficient cases. Source labels remain a separate column, never a project label inferred by default.
2. **Reviewed identity:** a new project ID and explicitly supported member records. Positive links propose membership; connected components alone cannot certify it. Before adding any member, review its complete identifier and material qualifiers against the selected reference and reconcile all known contradictory or insufficient edges inside the proposed identity. A positive chain cannot erase a negative or unresolved edge. Split or defer conflicted components; retain their audit trail. Unreviewed siblings from a source group never inherit membership. Distinct proposed identities also need alias/deduplication review before one catalog entry per identity is claimed.
3. **Leakage block:** a conservative grouping for partition allocation, not an identity label. Keep all members of a source group together for partition safety; join groups for shared records, exact duplicate payloads or established identity aliases. Suspected aliases require review or joint reservation rather than assignment to opposite partitions. A negative pair by itself does not join blocks. A source group may contain several distinct reviewed identities that still share one leakage block.

Exposure propagates across leakage blocks: any pilot/diagnostic exposure makes the whole connected block development-only. Source-group propagation is deliberately conservative despite noisy source labels. Unresolved alias risks touching a potential test block prevent its release. Structural processing is not semantic exposure, but any later inspection used to tune a model, prompt, policy or threshold is; log it. Cross-group alias checks are necessary because source-disjointness alone is not identity-disjointness.

Holds remain a separate overlay on the immutable sampling inputs: 054/063 membership conflicts; 032/205 pilot disputes; 161/002/021/192/075/114/163 revision 13 holds. All held groups stay out of automatic identity construction and initial scored catalog releases until explicit record-level resolution. Existing pair evidence, including D013, remains usable as a development pair diagnostic. The 18 positive pairs are not a claim of 18 releasable catalog identities.

### Catalog and request construction

Proposed first release: a small, reviewed, cross-source offer-to-catalog experiment. Use only assigned records with recorded eligibility and explicit identity evidence; exclude confirmed D15 ineligible records from eligible-request metrics but preserve them in the audit. Keep unresolved eligibility in the eligible denominator and retain unresolved identity cases in a separate request slice. Do not create a singleton identity from an incomplete record just to fill a quota.

For each releasable identity, select **one original record** as the reference; do not synthesize a richer description by merging offers. It must have established complete identity evidence and no unresolved material contradiction, plus at least one eligible nonduplicate query from another source host. Among qualifying reference records, prefer the one allowing the most cross-source query records, then break ties by SHA-256 of UTF-8 `f1-catalog-v1|reference|locator`. Use the lowest digest, with locator as final tie-breaker. The same fixed rule applies in every partition and cannot depend on matcher results. Keep complete raw inputs locally; preserve missing values and provenance in any derived fields.

Other eligible records in the identity from different hosts become queries, provided they are neither the reference nor exact duplicates of it. Collapse exact payload duplicates into one evaluation representative while retaining all locators and multiplicities in the audit; flags for near-duplicates require review. Reference-only identities lacking cross-source queries do not enter the initial scored release; report them as deferred. Source host is a dataset provenance proxy, not proof of independent suppliers.

Each partition has its own fixed catalog comprising all releasable identities assigned to it. Each query searches the full partition catalog, including other identities as distractors; do not supply only its paired reference. Report catalog size and per-query candidate counts. Keep reference/query locator sets disjoint. Catalog entries for test identities may be available to retrieval at test inference, but never used for training or development tuning. Avoid adding unreviewed archive records as distractors: they could contain unrecognized true aliases and invalidate the target labels.

Inference receives only an opaque catalog-entry ID and offer attributes available at inference. Source entity IDs, project identity IDs, pair labels, review text, partition/exposure flags and source-stratum metadata remain in the evaluator, not model features. Manufacturer identifiers actually present in offers remain valid baseline features, with the identity-annotation dependence and possible contamination acknowledged.

### Proposed partition allocation and freeze

Use two partitions initially: **development and frozen test**, with no artificial training partition for a non-learned baseline. All exposed blocks are development-only. Development supports rules, prompts and threshold calibration; it is not held out. If a learned component is later justified, carve train/calibration identities within development before fitting it; preserve the test boundary.

After leakage blocks, holds, reference eligibility and unseen-pool capacity have been resolved, rank unseen releasable blocks by SHA-256 of UTF-8 `f1-split-v1|block|` followed by their sorted source-group IDs joined with commas. Break digest ties by the same joined IDs. **Propose reserving the first floor(N / 3) blocks for test and the rest for development**, where N is the number of unseen releasable blocks; exposed blocks are additional development material. Allocate whole blocks, never individual pairs or offers. This fraction is a feasibility design choice for owner review, not an existing approved split or a guarantee of adequate statistical power. Report realized identity/query/source counts because block sizes vary. No seed search, favorable-case swapping or backfilling based on model outcomes.

Select and reserve blocks before independent final-test annotation. Test review may reject or leave identities unresolved; retain the originally reserved block inventory and report attrition without replacing difficult cases. A reserved test block inspected for development is retired to development and cannot remain an independent test example; log the event and version the protocol instead of silently moving records.

Before any model evaluation, freeze hashes of archive, observation/adjudication release, identity membership, leakage/exposure ledger, catalog/reference and query manifests, partition assignment, D15/D17 versions and evaluation configuration. Independent reference review must be separated from model development and predictions. The developer must not use detailed final-test records or labels for policy tuning. If an independent review process cannot be arranged, keep an explicitly provisional AI-assisted holdout and defer final quality claims. No fixed minimum sample size or error target is invented here: obtain the actual capacity report and resolve O05 before claiming precision/coverage adequacy. Failure to obtain a useful test is a feasibility finding, not permission to weaken identity or exposure rules.

### Known absence and unresolved requests

Use the ordinary catalog for present-product measurements. Design a separate **controlled absence scenario** after identities and partitions are frozen: rank releasable identities within each partition by SHA-256 of UTF-8 `f1-absence-v1|identity|identity_id`, remove the first floor(M / 5) identities completely from that scenario's catalog, and use their queries as known-absent requests. This proposed 20% synthetic removal is a stress-test parameter, not real-world absence prevalence; report both M and the removed count and leave the scenario unavailable if the count is zero. Keep remaining identities as distractors and report the reduced catalog size. Confirm all aliases of removed identities are absent from the entire scenario catalog; unresolved alias risk prevents a known-absence label.

The same query may appear in the ordinary present scenario and the controlled absence scenario, but these are separate, paired evaluations, never pooled as independent samples. Missing retrieval candidates, an unmatched source label or an insufficient pair never establishes catalog absence. The system actions stay `auto_match` and `review_required`; do not introduce `no_match`.

Retain ambiguous requests, including D099, as development uncertainty cases. A known insufficient pair does not mean the query is insufficient against every possible catalog entry: assess the query against the actual catalog before assigning a request-level target. Requests with unresolved catalog identity have target status `unresolved`, not `absent`. Include them in eligible-request coverage/review counts; report automatic decisions on unresolved cases separately as unsupported decisions, without claiming they are correct or known wrong. Report accuracy/precision only on adjudicable outcomes with that restricted denominator explicit, alongside unresolved counts and overall coverage. Do not call restricted precision overall precision. Confirmed different pairs alone cannot certify a query's relation to an entire catalog.

### Reference verification and release artifacts

For development, AI-assisted identities can support provisional experiments with their origin explicit; do not call source groups or AI consensus gold. For final quality claims, require an independent human check of every released test identity's reference/query membership, material qualifiers and eligibility, plus the evidence for identity separation and absence construction. Record the checker role, date, policy and disagreements; the owner approving D17 does not satisfy record annotation. Return unresolved cases to the unresolved slice rather than forcing labels. If this cannot be obtained, document the limitation and do not make human-gold or final-quality claims.

Proposed data-only artifacts (schemas to be implemented, not files already produced):

| Artifact | Minimum content / invariant |
| --- | --- |
| Observation and adjudication ledger | Pair ID, oriented locators, source assignment separately, original judgment/rationale/origin, review provenance hash, dated adjudications and policy versions; latest applicable decision is reproducible without overwriting history. |
| Identity membership ledger | Project identity ID, explicit member locators, eligibility, evidence field references, verification status, unresolved conflicts; each released record belongs to one reviewed identity. |
| Exposure/hold/leakage ledger | Record and source-group locators, linked blocks, reasons, provenance and exposure events; holds and aliases never silently release themselves. |
| Catalog/query manifest | Reference locator, opaque entry ID, query locator, partition, target identity or explicit unresolved status, scenario and provenance; no raw text in public manifests. |
| Release metadata/report | Schema/policy/algorithm versions, seeds, input/output hashes, counts and exclusions by stage, reference origin, partition overlap/alias checks, scenario catalogs, unresolved risks and actual validation. |

Use plain JSON/CSV and Python 3.12 standard library for the next implementation; no database, framework, dependency or provider call is needed. Exact input/output paths are supplied explicitly. Restricted raw offers and reviewer text stay local; only sanitized locators, hashes and permitted evidence/aggregates can be versioned after content inspection. Do not make scripts auto-load personal notes or hardcode private paths. A reviewer CSV that cannot be shared may be an explicitly supplied input; document its expected schema/hash and provide synthetic software fixtures, without claiming a public clone can regenerate private annotations without that input.

### Staged execution, acceptance and next action

| Task | Status | Scope and completion evidence |
| --- | --- | --- |
| F1-P: catalog/split design | review | This proposal, observed capacity, risks and checks; no split execution. |
| F1-L: annotation and exposure ledger | done in revision 19 | Import the explicitly supplied preserved reviews/private mapping, public manifests and dated revision 13/16/17 adjudications; materialize a sanitized current-label ledger and exposure/hold report. Reproduce 120 unique pairs and 18/45/57 totals, keep all observations, propagate source exposure, and flag D013/075 and D066/D068/122. No new semantic review, identity merge or partition assignment. |
| F1-I: identity/reference preparation | draft; after F1-L | Resolve proposed membership, aliases, duplicates and held cases only within a separately selected bounded review task; produce actual eligible identity/query capacity and independent-review requirements. Never promote whole source groups. |
| F1-S: reservation and release | draft; after protocol agreement and F1-I | Agree allocation/absence parameters and independent review process, reserve blocks, independently verify test references, then freeze artifacts and validate the split. No execution in this task. |

F1-L's implementation should reject checksum/ID/orientation mismatches, duplicate review IDs, missing judgments and unsupported categorical values without producing a partial release. Test observable behavior with synthetic records: immutable original judgments plus overlays, exposed cross-group aliases, group hold versus positive pair, two disconnected positive pairs in one source group, and contradictory edges that prevent release. The ledger preserves insufficient cases and never interprets them as negatives. Replay the real manifest with an explicit local archive path and compare aggregate outcomes; ordinary tests stay offline and synthetic. F1-L can proceed when selected without resolving D099, fixing split proportions or acquiring a human reviewer. This design does not execute that next task automatically.

Final catalog/split acceptance requires: zero record or identity/leakage-block overlap across partitions; zero exposed blocks in test; no unresolved aliases across partitions; no held/unreviewed membership silently released; reference/query disjointness and documented duplicate handling; valid present targets in the actual scenario catalog; complete identity removal for known absence; reproducible hashes/order; full counts of ineligible, unresolved, held and deferred inputs; no label leakage into inference; and explicit independent-check status. An inability to meet these requirements is reported rather than hidden by filtering or relabeling.

Validation of this design: inspected the changed documentation diff; whitespace and relative-link/anchor checks passed. Recomputed exposure union, held-group overlap and structural capacity from the hash-verified archive and versioned manifests; inspected loader/selector behavior. No software tests, new annotations, quality evaluation, catalog generation, split allocation or Git mutations were performed. Key remaining choices for protocol agreement are the one-third unseen-block reservation, controlled 20% absence scenario and independent test review arrangements; actual capacity and O05 must precede claims of evaluation sufficiency. Next exact task: F1-L, a reversible local annotation/exposure ledger, without executing the proposed split.


## F1-L annotation/exposure ledger (revision 19, 2026-11-12)

Implementation approach: a standard-library CLI with explicit archive, first review, second review and private mapping inputs; versioned public provenance pins/adjudication overlays; a sanitized deterministic JSON ledger. Verify all input hashes and replay diagnostic selection before joining observations. Preserve original CSVs and reference rationale text by content hash instead of publishing it. Apply dated plan revisions as separate events; unknown historical event dates remain explicitly unknown. Keep source assignments and all group holds separate from pair labels. Record conservative exposure components from shared membership and exact duplicate objects; no semantic aliases are inferred. Flag disconnected positives and conflicts for later identity review, without constructing identities or a split. Synthetic tests cover validation failures, supersession, holds, exposure propagation and unresolved edges. The public output is locators/annotations only; no raw records or reviewer prose. This task is explicitly authorized by the owner's request to perform the next planned step. No dependencies, external calls or Git mutations are needed.

Completed: [annotation_ledger.py](../../annotation_ledger.py), [adjudication/provenance configuration](../data/alaska-monitor-adjudications.json), [synthetic tests](../../tests/test_annotation_ledger.py), and the [CLI instructions](../../README.md#replay-the-f1-annotation-ledger). Preserved existing loader/selector behavior, source inputs and review CSVs. The generated sanitized ledger was retained locally, not added as a large versioned duplicate; it is reproducible with explicit input paths and does not require personal notes. Revision 13 dates were not recorded precisely, so those events retain `null` dates rather than invented timestamps. Original review prose is preserved in the immutable local CSVs, with per-rationale hashes in the ledger. Evidence field names for adjudications were checked against the local record keys; no new semantic labels were assigned.

Validation: `py -3.12 -m unittest discover -s tests -v` passed all **14 tests** (four existing loader tests, ten ledger tests). An initial narrow run passed eight tests but the CLI test could not write its temporary fixture under the Windows sandbox; rerunning with temporary-directory access passed. No assertion was weakened. Self-review using the code-review-and-quality skill found that public JSON bytes differ between Windows CRLF checkouts and Git LF blobs; the importer now pins LF-normalized public JSON while preserving exact archive/private CSV hashing, with a regression test. No repository-wide Git configuration was changed.

The real CLI was run twice with the verified local archive/reviews/key and produced byte-identical output: **120 pairs, 149 observations, 15 adjudications, 18/45/57 effective judgments**. Exposure covers 124 of 232 source groups before and after structural propagation; 11 groups remain held. The ledger contains 2,273 distinct assigned record locators, 231 conservative blocks and 42 structural linking records (shared membership or exact duplicate-object groups). It flags D013/075 and D066/D068/122 as expected. No nonpositive edge is inside the diagnostic positive components; this is not evidence of conflict-free full source groups or completed alias review. The output SHA-256 on this Windows run is `2921398602b5219d2da6d4e71c108581ddaa818593bd2b73e8f0fc6e85e4abf3`; stdout line endings can differ across platforms, so compare parsed content or normalize line endings for cross-platform output comparison.

Review covered input integrity, error output without raw data, chronological supersession, held positives, disconnected positive evidence, conservative exposure propagation and the publication boundary. Documentation links/anchors and whitespace checks passed; new source, tests and configuration were inspected alongside the tracked diff. No remaining blocking findings identified in this self-review; no independent human/code review or quality evaluation is claimed. Scope complete: no catalog identity release, new semantic review, split, dependency installation or Git mutation. Next exact task: select bounded F1-I membership/alias review for a small development catalog; preserve D099 and all holds until evidence resolves them. Split allocation proposals remain unapproved and unexecuted.
