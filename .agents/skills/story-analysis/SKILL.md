---
name: story-analysis
description: Coordinate user-story investigation across relevant layers with bounded subagents, then consolidate requirements and a technical plan. Use for cross-layer story analysis before implementation.
---

# Story Analysis

Analyze the requested story without implementing it. Keep requirements and
decisions in the main thread; delegate independent repository investigation.

## Establish the task

- Read applicable `AGENTS.md` files and identify the repository and story.
- Retrieve the work item through Azure DevOps MCP when available. Otherwise use
  supplied requirements and state which external information remains unverified.
- Use `review-user-story`, when available, to assess unclear requirements from
  an identified accessible work item. When reviewing supplied requirements
  without an accessible work item or ID, assess ambiguities and acceptance gaps
  directly; do not require an ID that cannot add evidence.
- Distinguish confirmed requirements, approval, assumptions and open decisions.
  An instruction to analyze a story does not establish that its scope is approved.
  Investigate independent facts while material business questions remain open.

## Divide independent investigation

Inspect entry points first. For a small change in one area, investigate directly.
When at least two independent areas merit investigation, spawn up to three
subagents within the session's available capacity:

| Area | Preferred custom agent | Assigned evidence |
| --- | --- | --- |
| Backend | `backend-investigator` | Entry points, validation, authorization, services and integration contracts |
| Frontend | `frontend-investigator` | Pages, state, reusable UI, requests and visible states |
| Persistence | `persistence-reviewer` | Models, constraints, queries, transactions and queue/cache interactions |

Use only relevant areas. Prefer the installed roles; if a role is unavailable,
use an available general or exploration agent with the same bounded assignment.
If delegation is unavailable, perform the applicable investigation sequentially
and disclose the fallback. Do not claim that parallel work occurred.

Give each subagent the objective, confirmed criteria, unresolved decisions,
repository path, relevant entry points, assigned area and read-only boundaries.
Ask it to read applicable repository instructions, consult appropriate tools,
avoid further delegation and return:

- Existing behavior and reusable code, with file paths and symbols.
- Dependencies on other areas and contract questions.
- Risks, missing information and relevant existing tests.
- Suggested verification, separate from checks actually executed.

Do not send unrelated chat history or ask each agent to plan the whole story.
Keep overlapping ownership explicit and reconcile shared contracts centrally.

## Consolidate and plan

Wait for every started assignment to finish or fail before reporting. For a
failed assignment, report the gap; retry once when useful or investigate it
directly within the original scope. Never present missing evidence as complete.
Resolve contradictory claims against source evidence and follow cross-layer
dependencies before accepting recommendations.

For approved requirements, use `technical-planner` in the main thread when
available, reusing evidence and rechecking important claims. If unavailable,
produce the equivalent plan: scope, confirmed decisions, actual affected files,
ordered tasks, dependencies, acceptance-to-verification matrix and risks.
If approval or blocking decisions are missing, deliver the investigation and
questions with CONDITIONAL or BLOCKED readiness instead of an approved plan.
READY describes technical readiness; implementation still needs an explicit request.

Include delegated areas, fallbacks, unresolved conflicts and verification limits
in the final consolidated result. Return concise findings rather than raw logs.

## Boundaries

- Analysis and planning only, including for every delegated assignment.
- Do not edit files, application data, work items or external services; do not
  install dependencies, commit, push or start implementation.
- Return the plan in chat unless saving a specific report was requested.
- Do not run migrations, seeders or tests that may write data during analysis.
- Subagents share the parent's permissions and may share its working directory;
  these instructions do not create separate sandboxes or worktrees.
