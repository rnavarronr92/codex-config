# Laravel and PHP review reference

Load this reference when the change includes PHP, Laravel, Eloquent, controllers, services, validation, authorization, models or API behavior.

## Correctness

- Incorrect conditions, null handling and edge cases.
- Incorrect state transitions.
- Validation missing at trust boundaries.
- Incorrect Eloquent relationships or scopes.
- Unintended model events and side effects.
- Exception handling that hides operational failures.
- API contract and backward-compatibility regressions.

## Security

- Authentication and authorization enforcement.
- Policies, gates and tenant or institution boundaries.
- IDOR and unauthorized resource access.
- Mass assignment and unsafe input propagation.
- Sensitive information in responses or logs.
- SQL injection and unsafe raw queries.
- Unsafe file uploads, downloads and paths.

## Database-related behavior

- N+1 and unbounded queries.
- Missing pagination or chunking for large datasets.
- Nonselective filtering and sorting.
- Transaction boundaries and isolation assumptions.
- Concurrent writes and lost updates.
- Uniqueness enforced only in application code.
- Expensive aggregates and repeated calculations.
- Migrations that could lock large tables.
- Destructive or incompatible schema changes.

Do not claim a query is slow solely because it looks complex. Load the PostgreSQL reference when schema, indexes, query plans or database concurrency need deeper review.
