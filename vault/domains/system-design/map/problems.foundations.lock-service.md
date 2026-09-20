%% trellis:begin %%
# Distributed Lock & Coordination Service
*Design Problems / Building Blocks & Warm-ups*

Leases, fencing tokens and sessions on top of consensus — a Chubby/ZooKeeper-class service.

**Requires:** [[domains/system-design/map/distributed.consensus|Consensus]]

## Readings
- [[solution-lock-service|设计题解：分布式锁与协调服务（Distributed Lock & Coordination Service）]]
- [[src-chubby-lock-service|Burrows — The Chubby Lock Service for Loosely-Coupled Distributed Systems (OSDI 2006)]]
- [[src-etcd-lock-service|etcd 文档 — Learning: API]]
- [[src-kleppmann-lock-service|Kleppmann — How to do distributed locking]]
- [[src-zookeeper-lock-service|Hunt, Konar, Junqueira, Reed — ZooKeeper: Wait-free coordination for Internet-scale systems (USENIX ATC 2010)]]

## Drills
- [[design-lock-service|Drill: Design a distributed lock and coordination service]]

## Cards (8)
1. [[problems-lock-service-write-throughput-headroom]]
2. [[problems-lock-service-server-primitives-vs-client-recipes]]
3. [[problems-lock-service-fencing-token-is-free]]
4. [[problems-lock-service-vs-redlock]]
5. [[problems-lock-service-watch-herd-effect-context]]
6. [[problems-lock-service-read-scalability-choice]]
7. [[problems-lock-service-write-throughput-falls-with-nodes]]
8. [[problems-lock-service-multi-region-latency-tax]]
%% trellis:end %%

## Notes
