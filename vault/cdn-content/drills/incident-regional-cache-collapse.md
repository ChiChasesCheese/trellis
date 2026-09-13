---
nodes: [caching.failure, distributed.regional-cache, distributed.overload, reliability.alerting, reliability.incidents]
tags: [incident, on-call]
---
# Drill: Regional cache collapse incident

At 10:05, one region's cache-hit ratio drops from 92% to 18%. HTTP 5xx remains
flat for five minutes, then origin latency and timeout rate climb sharply.

**Constraints to state and honor**
- The cache service reports elevated latency but no outage.
- Traffic shifting risks overloading neighboring regions.
- Stale content is available for most, but not all, routes.
- A configuration release started at 09:58.

**Grading points**
- First dashboard cuts and trace comparison that distinguish key drift, eviction, and dependency slowness.
- Immediate mitigation order: stop change, serve stale, bypass selectively, shed load, or shift traffic.
- Retry and timeout changes that avoid turning dependency slowness into a retry storm.
- User-impact communication, command roles, decision log, and recovery criteria.
- Evidence needed before declaring recovery and postmortem actions that prevent recurrence.

**Attempt log**
- [ ] Attempt 1 (date, 25 min, self-graded notes):
