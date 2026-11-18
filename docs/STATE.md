# Current state

Updated: 2026-11-18

- Phase: F0 done; F1 in progress; full F2-F4 draft. Active plan: [000-feasibility.md](plans/000-feasibility.md), revision 22; F2-P done; owner accepted the scope on 2026-11-18, and F2-D1 is ready. No baseline has been implemented or run.
- Data: [current development manifest](data/alaska-monitor-development.json) retains 15 identities, 32 members, 15 original references and 17 cross-host queries under `capacity-information-hash-v2`. The v1 snapshot and original AI findings remain preserved; owner membership review is a separate nonblinded event, not independent final-test verification.
- Validation during F2-P: existing CLI rebuilt the ledger from the original hash-pinned archive, both CSVs and private mapping and validated current/v1 manifests. Counts, 11 holds, 124 exposed groups, D013/D019 deferrals and insufficient D099 are unchanged. No new software tests or quality evaluation; detailed evidence is in revision 22.
- Accepted next task: F2-D1, two simple deterministic ranking variants, each comparing all 17 queries with all 15 references; separate inference projection, normalization, ranking and grading. Report per-query, micro/macro and D112 sensitivity results; no automation threshold or O05 closure.
- Boundary: the owner accepted revision 22's development-only exception to the full F1 -> F2 dependency. It does not complete F1/F2 or approve F1-S, final split/reservation, absence evaluation, independent test review or LLM/provider processing. Underlying-content rights remain unresolved; raw data stay local.
- Next action: implement the accepted [F2-D1 scope and acceptance criteria](plans/000-feasibility.md#f2-p-bounded-development-baseline-plan-revision-22-2026-11-18) and run only that slice in a subsequent execution task; scope approval does not need repeating. No Git mutation was performed; inspected base commit is `1ca7d71`.
