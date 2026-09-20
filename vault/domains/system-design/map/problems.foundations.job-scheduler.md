%% trellis:begin %%
# Distributed Job Scheduler
*Design Problems / Building Blocks & Warm-ups*

Run millions of scheduled and ad-hoc jobs at least once, on time, with retries and no double-firing.

**Requires:** [[domains/system-design/map/async.queues|Message Queues]], [[domains/system-design/map/correctness.idempotency|Idempotency]]

## Readings
- [[solution-job-scheduler|设计题解：分布式任务调度器（Distributed Job Scheduler）]]
- [[src-dropbox-job-scheduler|How we designed Dropbox's ATF — an async task framework]]
- [[src-kleppmann-job-scheduler|How to do distributed locking (Martin Kleppmann)]]
- [[src-uber-job-scheduler|Cadence Multi-Tenant Task Processing]]

## Drills
- [[design-job-scheduler|Drill: Design a distributed job scheduler like a cron-as-a-service platform]]

## Cards (8)
1. [[problems-job-scheduler-full-scan-vs-timing-wheel]]
2. [[problems-job-scheduler-cron-clustering-peak-multiplier]]
3. [[problems-job-scheduler-at-least-once-vs-no-double-execution]]
4. [[problems-job-scheduler-fencing-token-lease]]
5. [[problems-job-scheduler-cron-reuses-oneoff-discovery]]
6. [[problems-job-scheduler-dag-event-driven-trigger]]
7. [[problems-job-scheduler-retry-backoff-dead-letter]]
8. [[problems-job-scheduler-multi-tenant-weighted-fairness]]
%% trellis:end %%

## Notes
