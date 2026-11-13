# Current state

Updated: 2026-11-13

- Phase: F0 done; F1 in progress; F2-F4 draft. Active plan: [000-feasibility.md](plans/000-feasibility.md), revision 21; bounded F1-I and owner-review/reference update complete.
- Policy/source: ALASKA Monitor under D16, D15 eligibility and D17 `monitor-identity-v1.1`. Local inspection is authorized; underlying-content rights remain unresolved. No raw redistribution, paid calls or additional provider processing.
- Pair evidence: replay preserves 120 pairs, 149 original observations, 15 adjudications and 18 same / 45 different / 57 insufficient. These are AI-assisted diagnostics, not gold or system-quality evidence. D099 and all other unresolved judgments remain unchanged.
- Development proposal: [manifest](data/alaska-monitor-development.json) reviews only 34 endpoints from 17 non-held positive pairs; 15 identities, 32 explicit members, 15 original references and 17 cross-source queries. D066/D068 share one reviewed identity; D013/075 remains held and D019 is deferred for an unexplained identifier conflict. No whole source group was promoted.
- Integrity/limits: all 11 holds and 124 exposed source groups remain unchanged. No exact duplicates in the reviewed pool; D112 has shared-template dependence across hosts. Alias findings apply only to this pool. No final split, test reservation, absence experiment or F2; owner confirmed displayed memberships and reported no noticed aliases; no independent/blinded final-test verification.
- Implementation: standard-library validator reuses the loader and freshly replayed ledger. All 25 offline synthetic tests pass; real-data replay is deterministic and reference/query sets are disjoint. [Run instructions](../README.md#validate-the-bounded-f1-i-development-proposal).
- Reference rule: capacity first, then reviewed information completeness, then hash; nine references changed with 15 identities / 15 references / 17 queries preserved. The original manifest and AI findings remain available; the owner assessment is a separate scoped event.
- Next action: agree the scope and acceptance criteria of the next experiment before running F2. D013/D019 remain deferred and D099 unchanged. Final allocation/absence parameters and independent test review still need agreement before F1-S; owner development review does not close those requirements.
