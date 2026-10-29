# Claims ledger — group X3

All checks are online reads of source at a named tag or of the official docs; nothing was run locally. Worked-example problems come from `sources/local/lc-in-decks.json` (code copied by script from the deck card).

| card id | claim | source | how checked |
|---|---|---|---|
| uth-gaps-prefix-sum-1-counter | a counter is cumulative, only increases or resets to zero on restart | prometheus/docs `docs/concepts/metric_types.md` (Counter) | read |
| uth-gaps-prefix-sum-1-counter | increase = last sample − first sample (`resultFloat = samples.Floats[numSamplesMinusOne].F - samples.Floats[0].F`) | prometheus@v3.5.0:promql/functions.go:extrapolatedRate | read |
| uth-gaps-prefix-sum-1-counter | result extrapolated to window ends, so integer counters can give non-integer results | prometheus@v3.5.0:docs/querying/functions.md `increase()` and `rate()` | read |
| uth-gaps-prefix-sum-1-counter | fewer than 2 float samples in the window gives no result (`case len(samples.Floats) > 1`, `default: return enh.Out`) | prometheus@v3.5.0:promql/functions.go:extrapolatedRate | read |
| uth-gaps-prefix-sum-1-counter | worked example 100,130,150,190,220 over 60 s: 220−100 = 120, 120/60 = 2 per second | arithmetic | derived |
| uth-gaps-prefix-sum-1-counter | LC 303 example: nums=[-2,0,3,-5,2,-1], sumRange(0,2)=1, sumRange(2,5)=-1 | arithmetic; code copied from deck card (Anki "LC 303") | derived |
| uth-gaps-prefix-sum-2-reset | counter reset handling: `prevValue := samples.Floats[0].F; for _, currPoint := range samples.Floats[1:] { if currPoint.F < prevValue { resultFloat += prevValue }; prevValue = currPoint.F }` | prometheus@v3.5.0:promql/functions.go:extrapolatedRate | read |
| uth-gaps-prefix-sum-2-reset | example 100,110,120,5,15: 15−100 = −85, +120 = 35 = 10+10+5+10 | arithmetic | derived |
| uth-gaps-prefix-sum-2-reset | take `rate()` first, then aggregate; otherwise `rate()` cannot detect counter resets when a target restarts | prometheus@v3.5.0:docs/querying/functions.md `rate()` | read |
| uth-gaps-prefix-sum-2-reset | a reset is any decrease between two consecutive samples (so a restart followed by growth beyond the old value between two scrapes is invisible) | prometheus@v3.5.0:docs/querying/functions.md `resets()`; same loop in functions.go | read, logical consequence |
| uth-gaps-prefix-sum-3-kafka-lag | LAG = LOG-END-OFFSET − CURRENT-OFFSET; `getLag` = `offset.filter(o -> o != -1).flatMap(... end - offset0)`; missing value printed as `-` (`MISSING_COLUMN_VALUE = "-"`) | apache/kafka@4.0.0:tools/src/main/java/org/apache/kafka/tools/consumer/group/ConsumerGroupCommand.java | read |
| uth-gaps-prefix-sum-3-kafka-lag | `--describe` prints one row per topic-partition with columns CURRENT-OFFSET, LOG-END-OFFSET, LAG | apache/kafka@4.0.0:docs/ops.html (Checking consumer position) and the printf header in ConsumerGroupCommand.java | read |
| uth-gaps-prefix-sum-3-kafka-lag | committed offset = the next message the application will consume (last processed + 1) | apache/kafka@4.0.0:clients/.../KafkaConsumer.java javadoc of commitSync/commitAsync | read |
| uth-gaps-prefix-sum-3-kafka-lag | compaction keeps original offsets; offsets of compacted-away messages stay valid positions (gaps) | apache/kafka@4.0.0:docs/design.html (Log Compaction Basics) | read |
| uth-gaps-prefix-sum-3-kafka-lag | LC 724 example [1,7,3,6,5,6] → 3 (11 = 11) | arithmetic; code copied from deck card (Anki "LC 724") | derived |
| uth-gaps-intervals-1-overlap | range types (`tsrange` etc.), `&&` overlap operator | postgresql.org/docs/17/rangetypes.html §8.17.2 | read |
| uth-gaps-intervals-1-overlap | `[` inclusive / `(` exclusive bounds; constructors default to `[)` when the third argument is omitted | postgresql.org/docs/17/rangetypes.html §8.17.3, §8.17.6 | read |
| uth-gaps-intervals-1-overlap | `EXCLUDE USING GIST (during WITH &&)` prevents overlapping rows; per-room version needs `btree_gist` for `room WITH =` | postgresql.org/docs/17/rangetypes.html §8.17.10; btree-gist.html | read |
| uth-gaps-intervals-1-overlap | exclusion constraint: for any two rows compared with the operators, not all comparisons may be TRUE | postgresql.org/docs/17/sql-createtable.html (EXCLUDE) | read |
| uth-gaps-intervals-1-overlap | LC 252 statement/example: [[0,30],[5,10],[15,20]] false, [[7,10],[2,4]] true; end==start not overlapping; code copied from deck card | sources/local/lc-in-decks.json → tlc-meeting-rooms-0-whole | read |
| uth-gaps-intervals-2-gist | GiST is a balanced tree-structured access method | postgresql.org/docs/17/gist.html §64.2.1 | read |
| uth-gaps-intervals-2-gist | internal entries hold the smallest range containing the children (`range_gist_union` calls `range_super_union`: "Return the smallest range that contains r1 and r2") | postgres@REL_17_STABLE:src/backend/utils/adt/rangetypes_gist.c | read |
| uth-gaps-intervals-2-gist | on internal pages the `&&` strategy tests `range_overlaps_internal(key, query)` (`range_gist_consistent_int_range`) | same file | read |
| uth-gaps-intervals-2-gist | internal "consistent" only says whether a subtree must be scanned; leaf does exact test / recheck flag | postgresql.org/docs/17/gist.html §64.2 (extensibility, consistent) | read |
| uth-gaps-intervals-2-gist | penalty function decides which branch an insertion follows; balance of the tree decides lookup speed | postgresql.org/docs/17/gist.html (penalty) | read |
| uth-gaps-intervals-2-gist | B-tree and hash on range columns: basically only equality is useful | postgresql.org/docs/17/rangetypes.html §8.17.9 | read (used for the 背景 reasoning, not quoted) |
| uth-gaps-intervals-3-concurrent | unique index checks duplicates atomically at index insertion; exclusion constraint inserts first, then does a separate index scan for conflicting tuples; waits if the conflicting inserter is in progress | postgres@REL_17_STABLE:src/backend/executor/execIndexing.c header comment | read |
| uth-gaps-intervals-3-concurrent | two concurrent inserters find each other's tuple and wait on each other; deadlock detector aborts one; "you get a different error message" | same comment | read |
| uth-gaps-intervals-3-concurrent | error text `conflicting key value violates exclusion constraint` | postgresql.org/docs/17/rangetypes.html §8.17.10 | read |
| uth-gaps-intervals-3-concurrent | SQLSTATE 23P01 exclusion_violation, 40P01 deadlock_detected | postgresql.org/docs/17/errcodes-appendix.html | read |
| uth-gaps-shortest-path-1-spf | each OSPF router holds an identical link-state database, floods its local state, runs the same algorithm and builds a shortest-path tree rooted at itself | RFC 2328 §1.3 intro and §2.2 | read |
| uth-gaps-shortest-path-1-spf | RIP uses "counting to infinity"; 16 is infinity (max usable metric 15) | RFC 2453 (limitations, counting to infinity) | read |
| uth-gaps-shortest-path-1-spf | loop: init tree with root; `ospf_spf_next(v)` adds neighbours to the candidate queue; `vertex_pqueue_pop` takes the nearest; repeat until empty (RFC 2328 §16.1 steps 2–5) | FRRouting/frr@frr-10.7.1:ospfd/ospf_spf.c:ospf_spf_calculate | read |
| uth-gaps-shortest-path-1-spf | example graph A-B 1, A-C 4, B-C 2, B-D 5, C-D 1: distances 0,1,3,4; next hop to C and D is B | arithmetic | derived |
| uth-gaps-shortest-path-1-spf | LC 778 example [[0,2],[1,3]] → 3; code copied from deck card (`+` replaced by `max` stated in the problem text) | sources/local/lc-in-decks.json → tlc-swim-in-rising-water-0-whole | read |
| uth-gaps-shortest-path-2-candidates | candidate list is a priority queue ordered by distance (`vertex_cmp`, `vertex_pqueue_pop`); implemented as a skiplist in 10.7 | FRRouting/frr@frr-10.7.1:ospfd/ospf_spf.c | read |
| uth-gaps-shortest-path-2-candidates | W already in SPF tree: skipped; W's LSA has no link back: skipped (`ospf_lsa_has_link < 0`); worse path (`w->distance < distance`) ignored | same, ospf_spf_next | read |
| uth-gaps-shortest-path-2-candidates | lower-cost path: `vertex_pqueue_del`, recompute nexthop, `vertex_pqueue_add`; equal-cost: only `ospf_nexthop_calculation` (merge next hops) | same, ospf_spf_next | read |
| uth-gaps-shortest-path-2-candidates | equal-cost routes share traffic equally | RFC 2328 §1.3 ("When several equal-cost routes to a destination exist, traffic is distributed equally among them") | read |
| uth-gaps-shortest-path-3-cost-throttle | `cost = refbw / bw + 0.5`, minimum 1, maximum 65535 | FRRouting/frr@frr-10.7.1:ospfd/ospf_interface.c:ospf_if_get_output_cost | read |
| uth-gaps-shortest-path-3-cost-throttle | reference bandwidth default 100 Mbit/s (`OSPF_DEFAULT_REF_BANDWIDTH 100000` Kbps); 100 Mbit/s or faster ⇒ cost 1; must be consistent on all routers | FRRouting/frr@frr-10.7.1:lib/libospf.h; doc/user/ospfd.rst (auto-cost reference-bandwidth) | read |
| uth-gaps-shortest-path-3-cost-throttle | SPF throttle defaults: delay 0 ms, holdtime 50 ms, max holdtime 5000 ms | FRRouting/frr@frr-10.7.1:lib/libospf.h (`OSPF_SPF_DELAY_DEFAULT`, `OSPF_SPF_HOLDTIME_DEFAULT`, `OSPF_SPF_MAX_HOLDTIME_DEFAULT`) | read |
| uth-gaps-shortest-path-3-cost-throttle | timer already scheduled ⇒ new trigger only records the reason, no second timer; event inside hold time ⇒ multiplier++ up to max; past hold time ⇒ multiplier = 1 | FRRouting/frr@frr-10.7.1:ospfd/ospf_spf.c:ospf_spf_calculate_schedule; doc/user/ospfd.rst (timers throttle spf) | read |
| uth-gaps-bfs-1-queue-vs-stack | default is LIFO ⇒ DFO ("usually the most convenient crawl order"); BFO needs DEPTH_PRIORITY=1, SCHEDULER_DISK_QUEUE=PickleFifoDiskQueue, SCHEDULER_MEMORY_QUEUE=FifoMemoryQueue | scrapy@2.19.0:scrapy/core/scheduler.py (Scheduler docstring, "Request order", "Crawling in BFO order"); settings/default_settings.py | read |
| uth-gaps-bfs-1-queue-vs-stack | concurrency means the first few requests may not follow the order; CONCURRENT_REQUESTS=1 enforces it (except the very first) | same docstring ("Concurrency affects order") | read |
| uth-gaps-bfs-1-queue-vs-stack | 20 links per page ⇒ 20^3 = 8000 at depth 3 | arithmetic | derived |
| uth-gaps-bfs-1-queue-vs-stack | LC 200 example [["1","1","0"],["0","0","1"]] → 2; code copied from the Anki deck card (deque BFS) | sources/local/lc-in-decks.json → "LC 200" Anki | derived |
| uth-gaps-bfs-2-depth-buckets | `request.priority -= depth * DEPTH_PRIORITY`; positive ⇒ BFO, negative ⇒ DFO | scrapy@2.19.0:scrapy/spidermiddlewares/depth.py; docs/topics/settings.rst (DEPTH_PRIORITY) | read |
| uth-gaps-bfs-2-depth-buckets | ScrapyPriorityQueue: one internal queue per priority, key = −priority, `curprio = min(...)`, pop takes the smallest key; internal queues FIFO/LIFO decide order within a bucket | scrapy@2.19.0:scrapy/pqueues.py:ScrapyPriorityQueue | read |
| uth-gaps-bfs-2-depth-buckets | default SCHEDULER_PRIORITY_QUEUE is DownloaderAwarePriorityQueue, one ScrapyPriorityQueue per download slot (domain) | scrapy@2.19.0:scrapy/settings/default_settings.py; scrapy/pqueues.py | read |
| uth-gaps-bfs-2-depth-buckets | LC 994 example [[2,1,1],[1,1,0],[0,1,1]] → 4; code copied from deck card | sources/local/lc-in-decks.json → tlc-rotting-oranges-0-whole | read |
| uth-gaps-bfs-3-seen | `RFPDupeFilter` keeps `_fingerprints: set[bytes]`; `request_seen` adds and returns False the first time; with JOBDIR appends length-prefixed fingerprints to `requests.seen` and reloads them | scrapy@2.19.0:scrapy/dupefilters.py | read |
| uth-gaps-bfs-3-seen | fingerprint = SHA-1 (20 bytes) of canonicalized URL, method, body (and chosen headers) | scrapy@2.19.0:scrapy/utils/request.py:fingerprint | read |
| uth-gaps-bfs-3-seen | `enqueue_request` checks `not request.dont_filter and self.df.request_seen(request)` before pushing | scrapy@2.19.0:scrapy/core/scheduler.py:Scheduler.enqueue_request | read |
| uth-gaps-bfs-3-seen | the set is never pruned (no removal path in the class) | scrapy@2.19.0:scrapy/dupefilters.py | read |
| uth-gaps-bfs-3-seen | LC 127 example hit → cog = 5; code copied from the Anki deck card (`visited.add` before `append`) | sources/local/lc-in-decks.json → "LC 127" Anki | derived |
| uth-gaps-bfs-4-cascade | ReplicaSet is owner of Pods; ownerReferences are set by controllers | kubernetes/website docs/concepts/overview/working-with-objects/owners-dependents.md | read |
| uth-gaps-bfs-4-cascade | Deployment is owner of its ReplicaSet (`OwnerReferences: ... NewControllerRef(d, controllerKind)`) | kubernetes@v1.34.0:pkg/controller/deployment/sync.go | read |
| uth-gaps-bfs-4-cascade | graph of nodes with `dependents`; on a delete event of an owner the graph builder adds every dependent to the `attemptToDelete` queue; workers consume it in `attemptToDeleteItem` and delete items that have no solid owner | kubernetes@v1.34.0:pkg/controller/garbagecollector/graph.go, graph_builder.go:processGraphChanges, garbagecollector.go:attemptToDeleteItem | read |
| uth-gaps-bfs-4-cascade | work queue is a slice-based FIFO with a `dirty` set (an item already waiting is not queued twice); several workers run in parallel | kubernetes/client-go@v0.34.0:util/workqueue/queue.go; garbagecollector.go:Run | read |
| uth-gaps-bfs-4-cascade | foreground deletion waits only for dependents with `ownerReference.blockOwnerDeletion=true` that are in the GC cache | kubernetes/website docs/concepts/architecture/garbage-collection.md | read |
| uth-gaps-bfs-4-cascade | LC 102 example [3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]; code copied from deck card | sources/local/lc-in-decks.json → tlc-binary-tree-level-order-traversal-0-whole | read |

## Notes

- Card `uth-gaps-shortest-path-2-candidates`, `-3-cost-throttle`, `uth-gaps-prefix-sum-2-reset`, `uth-gaps-intervals-2-gist`, `uth-gaps-intervals-3-concurrent` carry `**对应 LeetCode：** 无直接对应的题`: no deck problem uses a delete-and-reinsert priority queue, SPF throttling, counter-reset correction, bounding-range tree pruning or exclusion-constraint concurrency.
- Skeleton correction: `gaps.bfs` says Kubernetes finds dependents "by owner relation"; the real mechanism is an event-driven queue with parallel workers, not a strict level-by-level BFS, and the card says so.
- Prometheus code read at v3.5.0 (`promql/functions.go`); the main branch (v3.15.1) adds start-timestamp handling to the same function, which the cards do not rely on.
