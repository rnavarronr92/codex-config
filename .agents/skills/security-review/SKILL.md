---
name: security-review
description: Perform a focused, read-only security review of a requested diff or module, tracing reachable trust-boundary failures and separating confirmed findings from validation gaps. Use for explicit security review or changes to security-sensitive behavior; not a full penetration test.
---

# Security Review

Review the requested change or module for concrete security defects. Return a
bounded source-based assessment; do not expand a feature review into a full
repository audit, penetration test or compliance claim.

## Scope and risk

- Read applicable repository instructions and the requested requirements/diff.
  Record repository/ref, comparison base and relevant local changes. Capture
  inputs sufficiently to detect later edits; use starting file contents when Git
  comparison is unavailable. Preserve existing work and attribute regressions.
- Identify relevant principals, entry points, protected data/actions and trust
  boundaries. Follow actual middleware, policies, query scopes and callers.
- Focus on changed authorization, tenant isolation, untrusted data handling,
  uploads/downloads, authentication/tokens, sensitive responses/logs, outbound
  requests, secrets, dependencies and CI execution when they are in scope.
  Cosmetic changes do not require an additional security investigation.
- Select references by the affected boundary, combining them only when needed:
  - [Laravel/Vue](references/laravel-vue.md) for Laravel or Vue security paths.
  - [MCP/OAuth](references/mcp-oauth.md) for MCP trust boundaries, OAuth access
    tokens, JWT verification and request identity isolation. Apply only the
    protocol, token format and client/server responsibilities actually present.
  For other stacks or boundaries, inspect their actual controls instead of
  applying unrelated framework assumptions. Reuse relevant `code-review`
  references when available.

## Trace and challenge candidates

For each suspected problem, establish the lower-trust actor, controlled input,
reachable path, expected security invariant, existing enforcement, affected
principal/resource and concrete consequence. Check the complete path before
assuming a missing control: a policy in middleware or scoped query may already
enforce it. A missing additional hardening layer is not itself a vulnerability.

Keep three outcomes distinct:

- **confirmed**: the current source and demonstrated conditions establish a
  reachable security-boundary failure. State whether this is code-confirmed or
  locally reproduced; do not claim runtime evidence from static inspection.
- **needs_validation**: a specific source-grounded concern depends on a missing
  fact, such as deployed proxy behavior or an external identity policy. Give
  that exact fact and a safe validation plan, without assigning confirmed severity.
- **rejected**: evidence disproves the candidate. Mention rejected candidates
  only when useful to explain an important control or avoid repeated work.

For a material candidate, ask a fresh available agent to attempt to disprove it
when delegation is available and requested by the enclosing workflow. Give it
the claim, relevant source/ref and scope, without presenting the claim as true.
The verifier remains read-only and must not delegate further. If independent
verification is unavailable, validate the source directly and disclose that
limitation. Unresolved candidates stay needs_validation, not confirmed.
If running inside a role that cannot delegate, return candidates to the parent
for that independent assignment instead of spawning another agent.

Do not duplicate a finding already owned by another reviewer. Return one root
cause with affected paths; let the coordinator consolidate overlapping reports.
Recheck the reviewed inputs before reporting or mark changed areas incomplete.

## Execution boundaries

Source inspection only by default. Do not execute target-controlled code,
builds, tests, scanners, exploit payloads or installers in this review. Read
existing check results as supporting evidence and identify unverified conclusions.
Suggest the smallest regression check for the implementation phase, using dummy
principals/data in an isolated local environment; this review does not authorize
that execution. Never probe deployed endpoints or retrieve other users' data.

If the task explicitly requests runtime validation or a comprehensive audit,
establish its separate scope and execution environment first; do not silently
switch modes. A worktree or a prompt saying "read-only" is not an OS sandbox.
Cloudflare's full `security-audit` is a separate optional workflow with its own
execution requirements, not a dependency or an automatically invoked step here.

Do not edit files/data, print secrets, change external services, install tools
or create commits/PRs. Save a report only to an explicitly requested destination.
For suspected secrets, report location and credential type without the value.

## Consolidated result

Return reviewed scope and a compact boundary summary, then:

- Confirmed findings with P0/P1/P2/P3 priority, exact paths/lines, actor, source
  trace, violated invariant, concrete impact, minimal fix and regression check.
- Source-grounded needs_validation items, their decisive missing facts and the
  safe next check. Keep these separate from confirmed findings and priority totals.
- Existing controls relevant to the review, verification performed, independent
  validation status, uncovered areas and whether inputs changed during review.

Use the existing `code-review` priority meanings when installed. Otherwise P0
means critical immediate compromise, P1 a serious realistic security failure,
P2 a meaningful bounded defect, and P3 a minor concrete security defect. Priority
reflects impact and realistic preconditions, not the absence of a best practice.
Say explicitly if no actionable findings were established; that is not a security
certification or proof that unreviewed code and deployment are secure.
