---
nodes: [problems.foundations.job-scheduler, async.queues, correctness.idempotency]
tags: [problem]
---
# Drill: Design a distributed job scheduler like a cron-as-a-service platform

Design a multi-tenant distributed job scheduler: tenants register one-off jobs due at a
future timestamp, recurring cron jobs, and DAG-dependent job steps. The system must find
due jobs and dispatch them without scanning its full backlog, guarantee at-least-once
execution, and guarantee a job is never executed concurrently by two workers even when a
worker pauses and resumes.

**Constraints to state and honor**
- 5,000 tenants, ~10^8 jobs/day, average trigger QPS ~1,157, peak trigger QPS ~6,944
  (a 6x peak multiplier because due times cluster at shared boundaries like the top of
  the hour).
- ~3x10^8 outstanding scheduled rows at any time (~60GB) -- small in bytes, but a naive
  full-table scan for due jobs takes ~300 seconds, violating a P95 < 1s trigger latency
  target.
- Default execution semantics are at-least-once; concurrent double-execution must be
  prevented by a separate mechanism from the one that guarantees at-least-once delivery.
- No single tenant's burst may systematically delay other tenants' on-time triggering.

**Grading points**
- Rejects a full-table-scan discovery mechanism because its cost scales with total
  outstanding jobs rather than jobs actually due, and uses a hierarchical timing wheel
  backed by a time-bucketed persistent store instead
  ([[problems-job-scheduler-full-scan-vs-timing-wheel]]).
- Treats "executed at least once" and "never executed concurrently by two workers" as two
  independent guarantees requiring separate mechanisms, not one implying the other
  ([[problems-job-scheduler-at-least-once-vs-no-double-execution]]).
- Uses a lease with a monotonically increasing fencing token -- not a lease timeout alone
  -- to prevent a paused-then-resumed worker from writing results after a second worker
  has taken over ([[problems-job-scheduler-fencing-token-lease]]).
- Pushes idempotency responsibility down to the worker via a caller-supplied key rather
  than promising end-to-end exactly-once at the scheduler layer
  ([[correctness-idempotency-key-design]], [[correctness-idempotent-consumer-patterns]]).
- Handles recurring cron jobs by precomputing only the next due timestamp and reusing the
  one-off job discovery path, rather than building a separate structure for recurrence
  ([[problems-job-scheduler-cron-reuses-oneoff-discovery]]).
- Handles DAG step dependencies as an event-driven trigger (due when all dependencies
  reach succeeded) rather than forcing them through the time-based discovery path
  ([[problems-job-scheduler-dag-event-driven-trigger]]).
- Uses exponential backoff with a retry cap and a dead-letter queue for permanently
  failing jobs, instead of unlimited fixed-interval retries
  ([[problems-job-scheduler-retry-backoff-dead-letter]], [[async-dlq-poison-pill]]).
- Explains why scheduled workloads need a higher peak multiplier than organic traffic
  (due-time clustering at shared boundaries) and connects this to why multi-tenant
  fairness needs per-tenant rate limiting and weighted dispatch, not FIFO
  ([[problems-job-scheduler-cron-clustering-peak-multiplier]],
  [[problems-job-scheduler-multi-tenant-weighted-fairness]]).

**Solution**: [[solution-job-scheduler]] -- attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
