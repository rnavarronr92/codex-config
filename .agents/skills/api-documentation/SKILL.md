---
name: api-documentation
description: >
  Inspect application routes, handlers, validation and responses to create or
  update accurate API documentation, including Laravel APIs with high-volume
  data access, preferably in OpenAPI format. Preserve evidence boundaries and
  never invent undocumented behavior.
---

# API Documentation

Act as a senior engineer responsible for documenting an existing API from its
implementation and tests.

## Scope

Use this skill when the user asks to document, review or update API endpoints,
contracts, OpenAPI specifications or developer-facing API references.

Default to analysis and documentation changes only. Do not change endpoint
behavior, authentication, validation or application code unless the user
explicitly requests implementation.

## Source discovery

Identify the framework and API style first. Inspect the smallest relevant set
of sources:

- Route declarations and route groups.
- Controllers, handlers or resolvers.
- Request validation and authorization policies.
- Serializers, resources, presenters or response transformers.
- Domain services when they affect observable behavior.
- Existing OpenAPI files, API reference pages and examples.
- Integration, contract and end-to-end tests.
- Authentication middleware and versioning conventions.

Treat executable behavior and tests as stronger evidence than comments. If
sources disagree, report the conflict instead of silently choosing a value.

## REST API review

When the API follows REST, verify that the documentation reflects the actual
HTTP contract rather than only listing routes:

- Model paths around resources and collections, using the project's naming
  convention consistently.
- Document the meaning of `GET`, `POST`, `PUT`, `PATCH` and `DELETE` as the
  implementation actually uses them.
- Verify safe and idempotent operations instead of assuming them from the HTTP
  verb.
- Document status codes for success, validation, authentication,
  authorization, conflict, not-found, throttling and server failure cases when
  they are observable.
- Describe representation formats, content types, request headers and
  conditional requests when supported.
- Document filtering, sorting, pagination and field expansion as query
  parameters with their limits and ordering guarantees.
- Explain resource relationships and nested resources without implying
  operations that the server does not expose.
- Record caching, ETags, retry behavior and consistency guarantees when they
  are part of the contract.
- Identify versioning, deprecation and backward-compatibility rules.

Do not force REST conventions onto RPC, GraphQL or action-oriented endpoints.
If the implementation is only partially RESTful, document the observed
behavior and identify deviations as recommendations rather than facts.

## Laravel API review

When the project uses Laravel, inspect the conventions that shape the public
contract:

- Route groups, prefixes, names, middleware and API versioning.
- Controllers and invokable actions.
- Form Requests, authorization rules and validation messages.
- API Resources, resource collections and conditional relationships.
- Policies, gates, authentication guards and tenant isolation.
- Exception handlers and the project's standard error envelope.
- Pagination resources, filters, sorting and allowed includes.
- Feature tests and contract tests for status codes and response shapes.

Do not derive the response schema from an Eloquent model alone. Resources,
transformers and authorization may hide fields or change the representation.

## High-volume API considerations

Document performance-relevant behavior when it is confirmed by code,
configuration or tests:

- Cursor versus offset pagination and ordering requirements.
- Maximum page size and server-side limits.
- Allowed filters and sort fields; do not imply arbitrary query expressions.
- Eager-loaded relationships and the cost of includes or expansions.
- Bulk operations, asynchronous processing and job status endpoints.
- Idempotency keys, retry behavior and duplicate-request handling.
- Rate limits, caching, conditional requests and consistency guarantees.
- Timeout, throttling and partial-failure behavior.

Do not recommend cursor pagination, asynchronous processing, caching or bulk
endpoints solely because the dataset is large. Record the evidence and explain
the compatibility tradeoffs before suggesting a contract change.

## Endpoint contract

For every documented operation, capture when confirmed:

- HTTP method and path.
- Operation purpose and API version.
- Authentication and authorization requirements.
- Path, query and header parameters.
- Request body schema, validation and examples.
- Successful response status and schema.
- Error statuses and error body shape.
- Pagination, filtering, sorting and ordering behavior.
- Idempotency, rate limits and retry considerations when documented.
- Resource relationships and links when observable.

Do not claim that an endpoint supports a parameter, status code or response
field unless the code, tests or an authoritative project document confirms it.
Clearly mark inferred behavior and unresolved questions.

## OpenAPI workflow

Prefer OpenAPI as the machine-readable contract when the project has no
established alternative.

1. Inventory the existing endpoints.
2. Group routes by resource and version.
3. Reconstruct schemas from validation and response serialization.
4. Document authentication, common errors and shared components.
5. Add realistic examples without exposing secrets or personal data.
6. Validate paths, references, required fields and response status codes.
7. Compare the result against route listings and API tests.

Do not replace an existing documentation format without explaining the tradeoff
and preserving the project's established convention.

## Safety and quality

- Never include credentials, tokens, private keys or sensitive production data.
- Do not expose internal implementation details that are not part of the API
  contract.
- Do not change a public contract merely to make documentation easier.
- Do not claim that documentation or tests were validated unless they were
  actually run.
- Record endpoints that are incomplete, ambiguous or inconsistent.
- Separate confirmed behavior, inferred behavior and recommendations.

For contract changes, classify compatibility impact as one of:

- Non-breaking documentation clarification.
- Additive change.
- Behavior change requiring client coordination.
- Breaking change requiring versioning or a migration plan.

## Deliverables

Produce, as appropriate:

- An endpoint inventory.
- An OpenAPI document or a focused OpenAPI change proposal.
- Shared schemas for authentication, pagination and errors.
- Examples for representative success and failure cases.
- A list of contract mismatches and undocumented behavior.
- Validation commands or test cases to keep the documentation current.
- A compatibility assessment for proposed endpoint or schema changes.

Use this response structure:

## Resumen
## Endpoints revisados
## Contrato documentado
## Inconsistencias
## Información faltante
## Validación recomendada
## Recomendación

The recommendation must state whether the documentation is ready to publish,
requires verification or is blocked by missing implementation evidence.
