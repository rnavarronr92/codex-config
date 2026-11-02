---
name: data-model-review
description: >
  Review database migrations and related persistence code to derive and
  validate the current data model, including Laravel and PostgreSQL systems
  with large data volumes. Produce an evidence-based schema summary, ERD and
  identified gaps without modifying application code or databases.
---

# Data Model Review

Act as a senior software engineer reviewing the persistence model of an
existing application.

## Scope

Use this skill when the user asks to understand migrations, reconstruct the
current schema, generate an entity-relationship model or detect inconsistencies
between migrations and the application code.

Do not implement migrations, change models or alter a database unless the user
explicitly requests implementation in a later step.

## Investigation

Inspect only the relevant project areas:

- Migration files in execution order.
- Schema dumps or database schema files, when available.
- ORM models and declared relationships.
- Foreign keys, unique constraints, indexes, defaults and nullability.
- Seeders, factories and fixtures when they clarify relationships or states.
- Relevant repositories, queries and API resources.
- Tests that assert persistence behavior.
- Project instructions and existing architecture documentation.

Determine the framework and database engine before interpreting types or
constraints. Do not assume that a model relationship exists merely because a
column name suggests one.

## Laravel and PostgreSQL at scale

When the project uses Laravel with PostgreSQL, apply the following review
perspective. Treat these as investigation criteria, not automatic prescriptions.

### Laravel and Eloquent

- Verify that `foreignId`, `bigInteger`, UUID or other identifier types match
  across primary keys, foreign keys, models and pivot tables.
- Review Eloquent relationships against actual foreign keys, cardinality and
  delete behavior.
- Inspect scopes, casts, enums, soft deletes and timestamps that affect the
  persisted model.
- Identify N+1 risks, accidental model hydration and queries that select more
  columns or rows than the use case requires.
- Consider `chunkById`, cursor-based processing, targeted column selection and
  bulk operations for large datasets, while checking ordering, consistency and
  event behavior.
- Review factories, seeders and test fixtures for unrealistic cardinality or
  states that could hide production-scale problems.

### PostgreSQL and large volumes

- Evaluate indexes against real access patterns, selectivity, sort order,
  partial predicates and write overhead. Do not recommend an index without a
  query or constraint that justifies it.
- Review composite, partial, expression and covering indexes only when the
  workload supports them.
- Identify migrations that can lock or rewrite large tables, including adding
  constraints, changing column types, creating indexes or adding defaults.
- For high-risk changes, consider an expand/contract rollout, batched
  backfills, deferred constraint validation or concurrent index creation. Check
  PostgreSQL and Laravel migration transaction behavior before recommending the
  sequence.
- Review query plans with `EXPLAIN` or `EXPLAIN (ANALYZE, BUFFERS)` only on a
  safe representative environment. Never run intrusive analysis against
  production without explicit authorization.
- Consider pagination strategy, retention, archiving, partitioning and table
  growth only when data volume and access patterns justify them.
- Review transaction boundaries, lock contention, isolation assumptions,
  concurrent updates and idempotency of backfills or repair jobs.
- Consider operational observability: query duration, rows scanned, buffer
  usage, lock waits, migration duration and replication impact when available.

### Recommendations at scale

Rank recommendations by correctness, operational risk, expected benefit and
implementation complexity. Explicitly state:

- Whether the recommendation is required for correctness or only an
  optimization.
- What evidence supports it.
- What workload or data volume assumption it depends on.
- How it should be validated safely.
- Whether it affects deployment, rollback or application availability.

Do not prescribe partitioning, denormalization, sharding or new infrastructure
solely because the database may become large. Require evidence from current or
expected access patterns.

## Reconstruction rules

Build the current model from the final effect of all applicable migrations,
not by describing each migration independently.

For every entity, identify when confirmed:

- Table name and purpose.
- Primary key and identifier strategy.
- Columns, database types, nullability and defaults.
- Foreign keys and delete/update behavior.
- Unique constraints and indexes.
- Timestamps, soft deletion and lifecycle fields.
- Enumerated or state-like values.
- Many-to-many pivot tables and relationship metadata.

Separate confirmed facts from inferences and suggestions. Mark information as
unknown when the repository does not establish it. Do not invent business
rules, cardinalities or data meanings.

## Validation

When safe read-only access is available, compare the reconstructed model with
the actual schema or a disposable database created from the migrations.

Do not modify a shared or production database. If execution is unavailable,
state that the model is source-derived and identify what should be verified.

Check for:

- Migrations that do not reverse cleanly when rollback behavior matters.
- Foreign keys missing from expected relationships.
- ORM relationships that do not match database constraints.
- Nullable columns used as required values, or the opposite.
- Duplicate or redundant indexes.
- Conflicting defaults, status values or identifier types.
- Migration ordering and deployment risks.
- Large-table changes that may require a rollout strategy.

## Deliverables

Produce:

1. A concise schema summary.
2. An entity-relationship diagram in Mermaid when the relationship set is
   understandable from the evidence.
3. A table-by-table inventory of relevant columns and constraints.
4. Inconsistencies, unknowns and deployment risks.
5. Verification steps for facts that could not be confirmed.

Use this response structure:

## Resumen
## Modelo confirmado
## Diagrama entidad-relación
## Inconsistencias y riesgos
## Información faltante
## Verificaciones recomendadas
## Recomendación

The recommendation must distinguish between a model that is ready for use,
one that needs verification and one that is blocked by missing information.
