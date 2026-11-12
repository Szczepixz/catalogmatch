# Current state

Updated: 2026-11-12

- Phase: source selection closed. ALASKA Monitor selected for feasibility under D16; monitor identity policy v1.1 adopted under D17, including owner-approved manufacturer-coverage handling.
- Active plan: [000-feasibility.md](plans/000-feasibility.md), revision 18. F0 done; F1 in progress; F2-F4 draft.
- Evidence: [audit](data-audit.md): 30-pair ALASKA pilot, 4 same / 17 different / 9 insufficient; AI-assisted, not gold or system-quality evaluation. [Pilot manifest](data/alaska-monitor-pilot.json) preserves locators and decisions. WDC history retained.
- Data integrity: original ER duplicates and conflicting groups recorded; quarantine 054/063 and pilot-disputed 032/205 from trusted-label preparation. Do not treat remaining source groups as automatically correct.
- Scope: owner accepts bounded local ALASKA inspection despite unresolved underlying-content rights; no publisher contact needed. No raw redistribution, paid calls or additional model-provider processing authorized.
- Four-case outcome: D035/D065/D068 are provisional AI-adjudicated positives; D099 remains insufficient. Both original reviews and revision 16 history are preserved. Diagnostic tally: 18 same / 45 different / 57 insufficient, not gold or accuracy evidence; 15 positives have concordant AI assessments.
- Protocol: revision 18 proposes reviewed identities separate from leakage blocks, per-partition catalogs, unseen-block reservation and controlled absence. Design only; allocation parameters and independent test review remain to agree. Exposure covers 124 source groups; 106 unreviewed/non-held groups remain before alias and eligibility checks (60 span two or more sources), not validated identities.
- Next action: select F1-L to materialize the annotation/exposure ledger and holds, preserving 18/45/57 and original reviews. D099 stays insufficient without new evidence; revision 13 holds remain intact. No final split, catalog release or Git mutation is authorized by the proposal.
- Implementation: verified offline structural loader and synthetic tests. See [run instructions](../README.md#run-locally).
