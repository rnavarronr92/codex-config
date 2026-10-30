# Architecture and maintainability review reference

Load this reference when the change affects boundaries, shared abstractions, public APIs, extension points or cross-module behavior.

Evaluate whether the changes:

- Follow existing project conventions.
- Introduce avoidable coupling.
- Duplicate existing business logic.
- Create unnecessary abstractions.
- Expand the public API without justification.
- Break established extension points.
- Make future changes materially harder.

Do not recommend a design pattern merely because it is popular. Explain the concrete consequence of the design. Avoid speculative refactors unrelated to the current change.
