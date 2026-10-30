# Redis and queues review reference

Load this reference when the change includes jobs, queues, workers, Redis, locks, retries, scheduled processing or distributed execution.

Inspect:

- Idempotency under retries or duplicate delivery.
- Race conditions across workers and pods.
- Jobs dispatched before transaction commit.
- Retry, timeout and backoff interactions.
- Overlapping execution and lock expiration.
- Partial failures and external side effects.
- Large serialized job payloads.
- Memory usage and unnecessary data loading.
- Queue backlog, throughput and job duration.
- Redis round trips, cache stampedes and expensive key scans.
- Redis Cluster key-slot compatibility when relevant.

Consider multiple workers and replicas, horizontal scaling, resource limits and external service rate limits. Never optimize throughput at the expense of correctness or data consistency.
