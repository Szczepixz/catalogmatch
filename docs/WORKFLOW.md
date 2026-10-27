# Development workflow

## Operating principle
Use short planning, implementation and review cycles for substantial changes. Routine edits do not require separate roles or sessions. Shared files carry the handoff; personal prompt text and model preferences are optional local tooling.

## Recommended cycle
1. **Plan:** inspect the current files, resolve the next important uncertainty, and prepare one executable task or a small coherent group in the active plan.
2. **Implement:** execute only the selected task/group, validate it, inspect the diff, and record evidence in the same plan.
3. **Review:** inspect actual artifacts and test results, challenge the assumptions, and accept or request focused fixes. Use a fresh review chat when a complex design warrants a less anchored assessment.
4. **Continue:** update the plan and the short current-state pointer. Plan the next slice using what was learned.

Do not plan every function for the whole project. Maintain a rough roadmap and detailed instructions only for the next slice. The implementer may choose routine details but must not silently change identity semantics, splits, acceptance criteria or architecture.

## Roles

### Planner
Read the actual environment and relevant files. List already-established facts separately from assumptions. Make routine choices without repeated permission requests. Resolve high-impact unknowns or turn them into explicit discovery tasks.

Use [the template](plans/TEMPLATE.md). A task is ready when it has a concrete outcome, inputs, bounded scope, interfaces if relevant, acceptance criteria, feasible validation and relevant authorization. Cite exact files and sections, not another chat. Verify dependency/API assumptions against primary docs when necessary.

Do not call a task ready if it depends on an unknown dataset schema or license; instead make resolving that uncertainty the task. A paid experiment can remain pending authorization while offline tasks proceed.

### Implementer
Read the chosen plan revision, inspect affected files, and check whether assumptions still hold. Complete the selected task with proportional validation. Do not stop for routine reversible decisions or every substep.

If the plan is materially wrong, record the evidence and the smallest proposed revision. Continue independent in-scope work, but do not silently change the meaning of the task or exceed permissions. Return the question to the planning chat through a written handoff, not automatic messages.

### Reviewer
Read the actual changed artifacts, relevant surrounding code and plan evidence. Test risk-bearing behavior when needed; do not rerun every check by default. Review split validity and labels as carefully as application code. An implementation report is not proof of correctness.

Record actionable findings, severity, affected files and acceptance impact in the active plan. Do not demand extra frameworks or stylistic refactors. An implementation marked `review` is not automatically `done`. AI review is not independent human verification: check the evidence, and label the verification actually performed.

## One source of truth per concern
| Concern | Location |
| --- | --- |
| Persistent instructions | `AGENTS.md` |
| Product and scope | `docs/PROJECT_BRIEF.md` |
| Durable decisions | `docs/DECISIONS.md` |
| Evaluation rules | `docs/EVALUATION.md` |
| Current pointer | `docs/STATE.md` |
| Task status, evidence, review and handoff | Active file in `docs/plans/` |
| Verified setup/run commands | `README.md`, once executable code exists |
| Documentation placement and publication | `docs/DOCUMENTATION.md` |

Do not create separate logs duplicating all task history. Keep plan updates compact. Keep useful completed stages in place and point STATE to the next plan. Follow the [documentation policy](DOCUMENTATION.md) when moving or trimming files. Shared technical decisions must never exist only in ignored notes.

## Status conventions
Tasks: `draft` -> `ready` -> `in_progress` -> `review` -> `done`.
Use `blocked` for a concrete unresolved dependency, with the missing input and independent work listed. Use `superseded` when a replacement task makes an old one obsolete. These are document labels, not Codex goal-tool states.

Task requests define whether planning, execution or review is authorized. No extra approval is needed solely because work moves from one routine step to another. A `ready` label never grants financial or destructive-action permission.

Review significant stages; batch trivial fixes into the next meaningful review. This is not a requirement for three chats per edit.

## Handoff minimum
At a boundary, update the active plan with:
- Selected task and plan revision; status and actual files changed.
- Checks/experiments actually run and their results or artifact paths.
- Deviations and material decisions, including approval scope if applicable.
- Known limitations, failures, blockers and next exact action.
- One or two important technical points that explain the result or its limitations.

If Git is available, inspect status/diff and preserve unrelated changes. Record a base commit if available; do not create commits to make the workflow look complete. Without Git, record the changed-file list and review those files directly.

## Concurrency
Use one writer at a time in the same checkout, including Markdown state files. Stop a writing turn before starting another. Do not assume shared UI project membership means two chats use the same checkout; verify the working directory.

If work repeatedly fails, reassess the assumptions or execution approach rather than expanding instructions indefinitely. Personal tool/model choices need not be part of the public task history.

## Codex references
[AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) is a documented Codex feature. The plan/state/workflow filenames in this repository are our conventions, not special files automatically loaded by Codex. AGENTS explicitly points to them.

[OpenAI's iterative workflow example](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex) also separates persistent guidance from phase artifacts. This project uses a smaller set of files to reduce process overhead.
