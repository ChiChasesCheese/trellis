---
nodes: [problems.foundations.lock-service, distributed.consensus]
tags: [problem]
---
# Drill: Design a distributed lock and coordination service

Design a Chubby/ZooKeeper/etcd-class coordination service: it must provide
distributed locks with automatic release on client failure, plus the
primitives needed to build leader election and group membership on top.
Downstream resources must be able to reject writes from a client that no
longer legitimately holds a lock, even after an arbitrarily long pause.

**Constraints to state and honor**
- ~5,000 client processes maintaining sessions; a 5-node consensus ensemble.
- Session TTL 15s with keep-alives; same-region write p99 < 50ms.
- Every lock grant must return a fencing token a downstream resource can check.

**Grading points**
- Computes the real consensus-write demand for the fleet and shows it sits orders of magnitude below a 5-node ensemble's published write ceiling ([[problems-lock-service-write-throughput-headroom]]).
- Explains why adding voting nodes to one ensemble never increases its write throughput, citing the read-up/write-down pattern as ensemble size grows ([[problems-lock-service-write-throughput-falls-with-nodes]]).
- Exposes only generic primitives (create/delete/read/watch, sessions) and builds locks/leader-election as client-side recipes rather than server RPCs ([[problems-lock-service-server-primitives-vs-client-recipes]]).
- Derives the fencing token from the replicated log's own monotonic version rather than inventing a separate token mechanism, and states the downstream-resource enforcement contract ([[problems-lock-service-fencing-token-is-free]]).
- Distinguishes when many watchers on one key should wake exactly one (a lock queue) versus all of them (a broadcast leader pointer) ([[problems-lock-service-watch-herd-effect-context]]).
- Routes routing-only reads to serializable local reads and safety-critical reads to linearizable ones ([[problems-lock-service-read-scalability-choice]]).
- Explains why a Redlock-style multi-instance voting scheme is unacceptable when lock correctness is a safety dependency, not just an efficiency optimization ([[problems-lock-service-vs-redlock]]).
- Avoids stretching a single ensemble across distant regions and instead uses per-region ensembles plus a small global one ([[problems-lock-service-multi-region-latency-tax]]).
- Explains why a paused client cannot safely re-check its own lock validity before writing ([[distributed-fencing-tokens]]).

**Solution**: [[solution-lock-service]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
