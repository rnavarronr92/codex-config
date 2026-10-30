# Vue and JavaScript review reference

Load this reference when the change includes Vue components, JavaScript, frontend state, browser behavior or API integration from the client.

## Reactivity and lifecycle

- Incorrect `ref` or `reactive` usage.
- Watchers that create loops or stale state.
- Computed values with inappropriate side effects.
- Missing lifecycle cleanup.
- Event listeners, intervals and subscriptions that leak.
- Incorrect component state synchronization.

## Components

- Incorrect props, emits and event contracts.
- Unexpected mutation of props or shared state.
- Unstable keys and list rendering issues.
- Inconsistent loading, empty and error states.
- Race conditions across asynchronous requests.
- Requests completing after a component unmounts.
- Incorrect form validation and submission behavior.

## Integration

- Frontend assumptions that conflict with the API.
- Inconsistent response and error handling.
- Authorization enforced only in the frontend.
- Stale cached data and invalidation problems.
- Unexpected breaking changes in shared components.

## UX and accessibility

- Critical keyboard accessibility issues.
- Incorrect form labels or semantic elements.
- Broken interaction states.
- Obvious responsive defects when verifiable.

Do not claim visual defects without browser evidence, a reproducible layout condition or a clear code-level cause. Load the testing reference when browser checks or component tests are relevant.
