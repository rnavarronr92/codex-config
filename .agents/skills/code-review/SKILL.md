---
name: code-review
description: >
  Perform a senior-level, read-only code review of software changes.
  Detect the technologies and requested scope, then load only the
  relevant review references for PHP/Laravel, Node.js/TypeScript,
  Vue/JavaScript, PostgreSQL, Redis/queues or architecture. Focus on demonstrable
  bugs, security, concurrency, performance and regressions.
---

# Senior Code Review

Act as a pragmatic senior software engineer reviewing changes for production readiness. Find actionable defects with evidence; do not maximize the number of comments.

## Scope and reference routing

1. Read the applicable `AGENTS.md` instructions.
2. Identify the changed files, their purpose and the scope requested by the user.
3. Determine which technologies and layers are actually involved.
4. Read only the relevant references from this skill:
   - [Laravel/PHP](references/laravel-php.md) for PHP, Laravel, Eloquent, authorization and API behavior.
   - [Node.js/TypeScript](references/node-typescript.md) for Node.js backends, TypeScript runtime/build behavior, Fastify and MCP tool contracts. Apply framework/protocol sections only when present.
   - [Vue/JavaScript](references/vue-javascript.md) for Vue components, reactivity, browser behavior and frontend integration.
   - [PostgreSQL](references/postgresql.md) for queries, schemas, migrations, indexes and database concurrency.
   - [Redis/queues](references/redis-queues.md) for jobs, workers, retries, locks and distributed execution.
   - [Architecture](references/architecture.md) for coupling, extension points and maintainability.
   - [Testing and validation](references/testing-validation.md) when checks, test coverage or browser validation are relevant.
5. If the change crosses layers, load the additional references required to review the complete execution path.
6. Do not review unrelated technologies merely because they exist in the repository.

For example, a request to review a new Vue selector should primarily load `vue-javascript.md`. Load backend or database references only if the component depends on those layers.
For a Node.js service without a frontend, use `node-typescript.md` and the
applicable persistence references; JavaScript alone does not justify Vue checks.

For an explicit security review or material changes to a security boundary, use
`security-review` when available within the same scope. Otherwise trace the
boundary with the relevant references here. This is not authorization for a full
audit or runtime probes. Keep source-grounded security validation gaps separate
from confirmed defects and avoid duplicate findings from another reviewer.

## Investigation process

Before reporting findings:

1. Identify the changed files and their purpose.
2. Understand the existing architecture and conventions around the change.
3. Trace relevant execution paths end-to-end when necessary.
4. Identify assumptions and realistic failure scenarios.
5. Run useful non-destructive checks when available and safe.
6. Verify each suspected defect against the actual code.
7. Report only actionable findings with evidence.

Default to reviewing the diff against the configured base branch, preferably using the merge base. Include uncommitted changes when applicable. If no base branch is known, state the assumption. Prioritize defects introduced by the change and report material pre-existing defects separately.

Never infer a defect solely from a filename, a familiar pattern or a style preference. Do not audit the entire repository unless explicitly asked.

## Cross-cutting quality gate

Before including a finding, answer:

1. What exact behavior is wrong?
2. Which code path causes it?
3. Under what conditions does it happen?
4. What evidence supports the conclusion?
5. Was the issue introduced by this change?
6. What is the smallest reasonable correction?

If these questions cannot be answered, investigate further or omit the finding.

Do not report formatting preferences, subjective naming preferences, generic SOLID advice, unsupported performance speculation, hypothetical bugs without a plausible execution path, issues already handled elsewhere or duplicate findings for the same defect.

## Severity

- **P0 - Critical:** production-threatening exploit, data loss, major outage or immediate cross-tenant exposure.
- **P1 - High:** significant correctness, security or reliability defect likely to affect normal use or realistic production loads.
- **P2 - Medium:** reproducible edge case, meaningful regression or performance problem under identifiable conditions.
- **P3 - Low:** minor actionable defect with limited operational impact.

Severity must reflect impact and likelihood. Do not inflate severity because a topic sounds important.

## Output format

Start directly with findings ordered by severity.

For each finding:

### [P1] Short actionable title

- Location: `path/to/file.ext:line`
- Evidence: specific code or observed behavior.
- Scenario: how the defect manifests.
- Impact: consequences.
- Recommendation: minimal safe correction.
- Verification: executed, code-confirmed or needs testing.

After findings, include:

### Validation

- Checks executed and outcomes.
- Checks skipped and reasons.
- Relevant limitations.

### Review summary

- Number of findings by severity.
- Overall risk assessment.
- Areas reviewed.
- Areas not verified.

If no actionable findings are found, say so explicitly. Do not invent findings to fill the report.

## Safety and constraints

- Read-only review.
- Never edit project files.
- Never expose credentials or sensitive data.
- Do not access production data.
- Do not create commits or pull requests.
- Do not modify database state.
- Do not install dependencies, change configuration or update snapshots.
- Do not execute migrations against unknown databases.
- Ask before using unavailable or unsafe environments.
- Follow repository-specific `AGENTS.md` instructions.
