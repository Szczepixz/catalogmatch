# Documentation and publication policy

## Principle
Version information another contributor needs to understand, run, evaluate or safely change the project. Keep personal, transient or sensitive material local. Classification depends on content and purpose, not whether AI wrote the text or an agent reads it.

This policy guides file placement and publication review. It does not authorize staging, committing, pushing, changing repository visibility or rewriting history.

## Placement rules
| Material | Location and treatment |
| --- | --- |
| Product overview, verified commands, results, limitations | Public `README.md`; product first, workflow details later |
| Shared agent instructions | Public `AGENTS.md`; concise, accurate, actionable |
| Product scope and constraints | Public `docs/PROJECT_BRIEF.md` |
| Durable technical decisions and alternatives | Public `docs/DECISIONS.md` |
| Data/evaluation protocols and reproducible evidence | Public `docs/EVALUATION.md` and focused reports under `docs/`, subject to data rights |
| Active stage plans and useful review findings | Public `docs/plans/`; exact scope, acceptance and concise evidence |
| Current technical state | Public `docs/STATE.md`; pointer and next action only |
| Collaboration and validation process | Public `docs/WORKFLOW.md`; enough to reproduce the process |
| Temporary working material and environment-specific notes | Optional `.local/`; ignored, not a project dependency |
| Secrets or private/restricted data | Never publish; ignored Markdown is not secure secret storage. Use appropriate credential/data storage |

Application prompts that affect model behavior are **product artifacts**, unlike personal coding-chat prompts. When implemented, version them with schemas/configuration and link them to experiments. Do not hide inference prompts or evaluation criteria in `.local/`.

Reusable coding prompts may be promoted to public documentation if they help contributors and contain no personal content. There is no requirement to publish every prompt or transcript to disclose AI assistance honestly.

## Before creating a Markdown file
1. Identify its audience and purpose. Prefer updating an existing source of truth.
2. Classify it as shared technical documentation or local working material before choosing the path.
3. For shared content, include only facts, decisions, constraints or evidence needed by a contributor. Separate planned, observed and unverified claims.
4. For local content, use `.local/` and make it optional. Do not automatically read personal notes during unrelated work.
5. A new permanent document should have an obvious reason to exist and an appropriate link from an existing document. Do not create a new report for every turn.

## Fresh-clone independence
All required instructions, decision semantics, setup steps and evaluation protocols must exist outside `.local/`. Public documents must not require or link to a specific local file. They may explain the optional local directory in plain text.

If a useful technical decision originates in a private note, copy a sanitized conclusion and its evidence into the appropriate shared document. Never move personal context into public docs merely to resolve a broken reference. Avoid duplicate public/private versions of the same authoritative plan.

Public execution instructions must not depend on undisclosed chat history. Record relevant authorization scope without account identifiers, credentials or personal conversation dumps.

## Maintenance and completed plans
- Update documentation when behavior, commands, assumptions or decisions materially change. Do not refresh dates without checking content.
- Keep AGENTS focused on recurring constraints. Put task details in the plan; use a dedicated document only when complexity justifies it.
- Update STATE at meaningful boundaries, not for every command.
- On stage completion, keep the goal, important decisions, actual validation, failures/limitations and outcome. Trim duplicated chat narration and transient command output; retain useful evidence or reproducible references.
- Keep completed plans in place when useful. If moving them into an archive, update links and the state pointer in the same change. Do not delete failed hypotheses to make results appear better.
- Label superseded decisions with reasons; distinguish corrections from cosmetic cleanup. Avoid rewriting Git history for presentation.
- Maintain README in reader order: problem/demo, observed results/limits, run instructions, architecture/decisions, then development process. Do not add a placeholder forest of documents for unimplemented features.

## AI assistance and verification
Describe actual AI usage briefly and accurately. Do not imply unaided authorship, independent human review, deployment, or measured improvement that did not occur. No arbitrary percentage of generated code is required.

Model-generated tests and a second model's approval can share the original error. Validate requirements, data labels, splits and observable behavior independently where feasible. Record concrete corrections and experiments rather than marketing the number of agents or Markdown files.

## Before recommending files for Git or a public release
- Inspect the actual file list and relevant diff, including new/untracked files; do not assume every `.md` is suitable.
- Check for secrets, personal details, absolute machine paths, restricted data and unverified claims. Review any raw examples against data permissions.
- Confirm local links resolve using only public files, required context is present, and code/results match the documentation.
- Check that `.local/` is ignored and not already tracked. In an initialized repository, read-only commands such as `git status --short --untracked-files=all`, `git ls-files -- .local`, and `git check-ignore -v -- .local/PROMPTS.md` can help. If Git is unavailable, report that Git-state verification was not performed.
- Ignore rules do not untrack existing files, protect secrets from other tools, or filter ZIP archives. Never use `git add -f` to bypass this policy. If private files are already tracked or published, report it and obtain authorization before changing the index/history; exposed credentials require appropriate remediation.
- Public release archives must explicitly exclude `.local/` and other private content; inspect archive entries before sharing.

## Boundary cases
Keep temporary private observations local while investigating. Promote the resulting technical finding once understood, including a failure if it matters. If a document mixes useful project content with personal notes, split those concerns rather than ignoring all of it or publishing all of it.
