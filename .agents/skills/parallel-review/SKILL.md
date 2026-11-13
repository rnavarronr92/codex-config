---
name: parallel-review
description: Coordinate evidence-based code review across affected layers using bounded parallel subagents. Use when a change spans independent review areas or the user requests parallel review; never apply fixes.
---

# Parallel Review

Review the requested change and return one evidence-based report. Reuse
`code-review` when available; use its relevant references instead of copying
technology checklists into every assignment.

## Fix the review scope

- Read applicable repository instructions and identify the requested change.
- Record the repository, HEAD commit, base reference and resolved base commit.
  Use the merge base for branch comparison. Include staged, unstaged and
  untracked source changes when applicable; state exclusions explicitly.
  Capture the reviewed diff and content hashes for included untracked files so
  later edits are detectable even when Git status lists the same paths.
- Prefer a user-supplied base, then a verified configured base. If neither is
  available, state a reasonable assumption or request the missing scope.
  If an explicit base cannot be resolved, report that limitation rather than
  substituting a different branch. Do not fetch or change branches implicitly.
- Inspect the changed paths and relevant callers before dividing the work.

## Delegate only independent areas

For a narrow change, run `code-review` directly. Otherwise spawn up to three
subagents within available session capacity, selecting only affected areas:

| Area | Preferred custom agent | Review ownership |
| --- | --- | --- |
| Backend | `backend-investigator` | Behavior, validation, authorization and service/API integration |
| Frontend | `frontend-investigator` | State, events, requests, UI behavior and integration |
| Persistence | `persistence-reviewer` | Integrity, queries, concurrency, jobs and cache behavior |

Use an available general or exploration agent with equivalent instructions when
the preferred role is missing. If delegation is unavailable, review sequentially
and disclose the fallback. Do not force three agents for an unrelated stack.
The main agent owns cross-layer contract checks and duplicate removal.

Give each agent the same resolved comparison commits, local-change scope,
relevant criteria, assigned paths, read-only boundary and output requirements.
Ask it to use `code-review` if available, load only relevant references, avoid
further delegation, trace callers as needed and report each actionable finding:

- Severity, file location and exact failing behavior.
- Triggering scenario, evidence and impact.
- Whether the change introduced it, and a minimal correction recommendation.
- Checks actually executed, results and unverified claims.

If `code-review` is unavailable, use these requirements directly. Omit subjective
style advice and unsupported performance claims. Use `performance-optimizer`
only for a concrete performance concern, in diagnosis mode, when available.

## Verify and consolidate

Wait for all started assignments to complete or fail. Retry a failed assignment
once when useful, or cover it directly; disclose any remaining gap. Validate
suspected defects against actual paths, reconcile conflicts and deduplicate
findings by root cause. Do not concatenate agent reports without checking them.

Check HEAD, the captured diff and untracked content again before the final response. If the
reviewed inputs changed, identify affected conclusions and reassess those areas
or mark the review incomplete. Do not claim that a review covers a newer change.

Return findings ordered by P0/P1/P2/P3 severity, followed by scope, delegated
areas/fallbacks, executed checks and limitations. Distinguish pre-existing issues
from regressions. An absence of findings is not proof that tests passed.

## Boundaries

- Review only; do not apply fixes, change files, update snapshots, install
  dependencies, mutate external systems or create commits/PRs.
- Only run non-mutating checks in an environment verified safe for those checks.
  Plan database/browser checks when their side effects cannot be excluded.
  Coordinate shared resources centrally rather than running competing tests.
- Save a report only to an explicitly requested destination.
- Agents inherit the parent's permissions and may share its checkout. Separate
  contexts do not provide independent filesystem or database isolation.
