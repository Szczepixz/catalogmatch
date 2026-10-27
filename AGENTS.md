# CatalogMatch project instructions

## Purpose and communication
Build an evaluated product matching system: supplier offers -> exact catalog variants -> automatic matches or human review. Prefer a simple, maintainable system with measured results.

Communicate with the user in Polish. Write code, identifiers, comments, documentation, and technical artifacts in English. Keep progress updates concise. Explain important trade-offs candidly.

## Start each task
For substantial work or a handoff, read [current state](docs/STATE.md) and its active plan. For routine edits, inspect only the affected files and relevant rules.

Use [project brief](docs/PROJECT_BRIEF.md) for scope, [decisions](docs/DECISIONS.md) for architectural choices, [evaluation contract](docs/EVALUATION.md) for data/metrics, and [workflow](docs/WORKFLOW.md) for handoffs. Inspect actual files and relevant Git status/diff if available. Plans describe intent; observed artifacts establish reality. Do not assume access to earlier chats.

## Scope and autonomy
- Use the simplest maintainable implementation that meets the selected task's acceptance criteria.
- Implement the selected task, including proportionate tests and necessary local fixes. Do not implement the whole roadmap automatically.
- Resolve routine, reversible details yourself and record material deviations. Escalate changes to product identity, evaluation splits, quality criteria, public contracts, or architecture before dependent work.
- A plan's `ready` status is a handoff signal, not user permission for paid services, major dependencies, infrastructure, or Git operations.
- Ask before adding a significant production dependency, replacing an established framework, changing infrastructure/important configuration, or performing destructive operations. Reuse explicit authorization already given; record its scope in the plan.
- Never commit, push, merge, rebase, reset, force-push, or change remote branches unless explicitly requested. Preserve existing user changes.
- Use one writer per checkout. Do not launch other chats or delegate to subagents unless the user explicitly requests it.

## Engineering constraints
- Begin with local feasibility experiments. No framework-heavy application scaffold before the data and baseline questions are addressed.
- Python is the primary language. Runtime, package manager, and dependencies must be selected from the inspected environment and documented; none are installed by this starter.
- Separate normalization, candidate retrieval, pair/selection scoring, and decision policy. Prefer plain functions and small modules over premature plugin interfaces.
- Keep domain decisions outside HTTP handlers and vendor-specific SDK code.
- Preserve raw input. Normalization must not silently remove identity-bearing attributes.
- Prefer deterministic rules where sufficient. A current LLM baseline is required experimentally; a deployed LLM, custom classifier, reranker, and fine-tuning are conditional on evidence.
- Add agents, vector infrastructure, queues or services only for a demonstrated requirement.
- Consult primary documentation when introducing a library or relying on uncertain API behavior. Record consequential evidence in the plan/decision register, not a transcript dump.

## Evaluation and data integrity
- Follow [EVALUATION.md](docs/EVALUATION.md). Never tune on the final test set or treat a model's own confidence as measured correctness.
- Keep `same variant`, `different variant`, and `insufficient evidence` distinct. Similarity is not identity; missing candidates do not prove catalog absence.
- Label generated fixtures, synthetic examples, and model-assisted annotations honestly. Model output alone is not gold ground truth.
- Preserve provenance and check dataset usage/redistribution terms. Do not expose secrets, private supplier data, raw provider responses, or restricted datasets in public artifacts.
- Paid calls and resource budgets must be explicitly authorized; an estimated project budget is not authorization. Apply run limits and keep ordinary tests offline.

## Validation and completion
- Start with the narrowest meaningful checks. Test observable behavior, important edge cases, and failure recovery, not implementation trivia.
- Keep software correctness tests separate from probabilistic quality evaluations. Record skipped/failed checks honestly.
- Inspect the relevant diff for meaningful code changes. Do not overwrite tests or weaken acceptance criteria to obtain a pass.
- Update the active plan with changes, actual checks/results, deviations, unresolved risks, and the next action. Update durable docs only when the underlying decision changes.
- Keep `docs/STATE.md` a short pointer to current work, not a duplicate work log.
- Do not claim production readiness, accuracy, performance gains, or business impact without evidence. AI-generated code/tests and model review do not replace inspection of requirements, data and behavior. Do not describe AI review as human review.

## Markdown and publication
- Apply [DOCUMENTATION.md](docs/DOCUMENTATION.md) whenever creating, moving or materially editing documentation.
- Version shared project rules, decisions, evaluation protocols, reproducible results and useful stage plans. Keep temporary working material in optional `.local/`.
- Public documents and commands must work without `.local/`. Do not require or automatically load personal notes; use them only when the user requests that context.
- Update the existing source of truth before adding another document. Keep STATE short and AGENTS practical; remove stale instructions rather than accumulating generic rules.
- Before suggesting files for Git, check their contents, relative links and data permissions. Agent-oriented documents are not inherently private. Do not hide AI usage or genuine failures to imply unaided authorship.
- `.gitignore` is not access control and does not untrack existing files. Do not stage, untrack or rewrite history without explicit authorization.

## Commands
No application, environment, or test commands exist yet. Do not invent successful setup or checks. When the first executable slice exists, document verified commands in README and reference them here.
