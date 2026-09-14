%% trellis:begin %%
# Distributed Systems for Fun and Profit

Mikito Takada · free-online · [[System Design MOC|System Design]]
[Home ↗](https://book.mixu.net/distsys/)

5 sections · 0 readings · 0 cards · 0/76 leaves reached

## Outline
- Distributed systems for fun and profit — *skipped*
- Distributed systems for fun and profit — *skipped*
- Distributed systems for fun and profit — *skipped*
- Distributed systems for fun and profit — *skipped*
- Distributed systems for fun and profit — *skipped*

## Leaves this corpus never reached (76)
Your reading list: the map says these exist and the book does not teach them.
- [[foundations.method|Interview Method]] — Requirements clarification, scoping functional vs non-functional needs, driving the 40-minute structure yourself.
- [[foundations.estimation|Back-of-Envelope Estimation]] — QPS, storage, and bandwidth sizing from DAU and access patterns; when an estimate changes the design.
- [[foundations.numbers|Latency Numbers]] — Orders of magnitude every engineer should know — memory vs SSD vs disk vs same-DC network vs cross-region.
- [[foundations.tradeoffs|Core Trade-offs]] — Performance vs scalability, latency vs throughput, availability vs consistency — the axes every later choice moves along.
- [[networking.protocols|Transport & HTTP]] — TCP vs UDP guarantees and costs; HTTP semantics, keep-alive, HTTP/2 and 3 in one breath.
- [[networking.dns|DNS]] — Resolution path, record types, TTL as a blunt failover and traffic-steering instrument.
- [[networking.api-styles|REST, gRPC & GraphQL]] — Choosing an API style by coupling, payload shape, streaming needs, and who owns the clients.
- [[networking.realtime|Realtime Delivery]] — Long polling vs SSE vs WebSockets; connection state as the scaling cost.
- [[networking.cdn|CDN]] — Push vs pull CDNs, cache keys, and what belongs at the edge.
- [[traffic.load-balancing|Load Balancers]] — L4 vs L7, balancing algorithms, health checks, and LB high availability itself.
- [[traffic.gateways|Reverse Proxies & API Gateways]] — What a gateway centralizes — TLS termination, auth, routing, quotas — and the single-point risks it adds.
- [[traffic.rate-limiting|Rate Limiting]] — Token bucket vs sliding window, local vs distributed enforcement, and what to return when you shed.
- [[caching.strategies|Write & Read Strategies]] — Cache-aside, read-through, write-through, write-behind, refresh-ahead — who populates the cache and when.
- [[caching.invalidation|Invalidation & Eviction]] — TTLs, eviction policies, stale reads, and cache stampede protection.
- [[caching.placement|Cache Placement]] — Client, CDN, gateway, application, and database layers — what each layer can and cannot absorb.
- [[storage.relational.indexing|Indexing]] — B-tree indexes, composite and covering indexes, leftmost-prefix rule, when indexes hurt.
- [[storage.relational.operations|Operating at Scale]] — Connection pooling, read replicas, federation, MVCC maintenance, and when a single Postgres is the right answer.
- [[storage.internals.btree|B-tree Mechanics]] — Fixed-size pages, splits, the WAL and crash recovery, in-place updates and their concurrency cost.
- [[storage.internals.lsm|LSM-tree Mechanics]] — Memtable to SSTables, compaction strategies (size-tiered vs leveled), Bloom filters, tombstones.
- [[storage.internals.tradeoffs|Engine Trade-offs]] — Read, write, and space amplification; when B-trees beat LSM-trees and vice versa; in-memory engines.
- [[storage.nosql|NoSQL Families]] — Key-value, document, wide-column, graph — the access patterns each one exists to serve.
- [[storage.record-modeling|Record Modeling]] — Shaping the records themselves — one table with a discriminating dimension versus separate stores, and vocabulary collision as a schema hazard.
- [[storage.object|Object Storage & Separation]] — S3-style object stores, storage-compute separation, and the modern default of parking cold and big data there.
- [[storage.search|Search Indexes]] — Inverted indexes, relevance basics, and keeping a search cluster in sync with the source of truth.
- [[storage.encoding|Encoding & Evolution]] — Data formats as contracts between code versions — JSON, Protobuf, Avro; forward and backward compatibility rules.
- [[distributed.cap|CAP & PACELC]] — What the theorem actually constrains during a partition, and the latency trade-off the rest of the time.
- [[distributed.consistency|Consistency Models]] — Linearizability, causal, read-your-writes, eventual — as contracts you promise the client.
- [[distributed.replication.leader|Leader-Based]] — Single-leader replication, log shipping formats, sync vs async, lag and its anomalies, failover mechanics.
- [[distributed.replication.multi-leader|Multi-Leader]] — Multi-datacenter writes, conflict detection and resolution, why LWW loses data.
- [[distributed.replication.leaderless|Leaderless & Quorums]] — Dynamo-style quorums, sloppy quorums and hinted handoff, read repair and anti-entropy.
- [[distributed.partitioning.schemes|Hash vs Range]] — Hash and range partitioning trade-offs; consistent hashing and virtual nodes.
- [[distributed.partitioning.rebalancing|Rebalancing & Routing]] — Moving partitions without downtime; who knows where a key lives — routing tiers and coordination services.
- [[distributed.partitioning.skew|Hot Keys & Skew]] — Detecting and defusing hot partitions — key salting, splitting, and request-level caches.
- [[distributed.partitioning.indexes|Partitioned Secondary Indexes]] — Local vs global secondary indexes — scatter-gather reads vs write amplification.
- [[distributed.transactions.isolation|Isolation Levels & Anomalies]] — Read committed to serializable through the anomalies each level permits — dirty/non-repeatable reads, write skew, phantoms.
- [[distributed.transactions.concurrency-control|Concurrency Control]] — 2PL vs MVCC vs SSI — how databases actually enforce isolation, and their contention behavior.
- [[distributed.transactions.distributed|Distributed Transactions]] — 2PC mechanics and blocking, why it's avoided at scale, and what replaces it.
- [[distributed.consensus|Consensus]] — Why single-leader systems need election, what Raft guarantees, fencing tokens, and the cost of quorum writes.
- [[distributed.time.clocks|Clocks & Timestamps]] — Time-of-day vs monotonic clocks, NTP drift, timestamp ordering hazards, confidence intervals, logical clocks.
- [[distributed.time.failure|Failure Detection & Pauses]] — Timeouts as the only failure detector, process pauses (GC, VM suspend), system models, and defending a chosen timeout.
- [[distributed.crdt|CRDTs & Local-First]] — Conflict-free replicated data types, merge semantics, and offline-capable multi-writer apps.
- [[async.queues|Message Queues]] — Queues vs pub-sub, backpressure, consumer scaling, and when async is the wrong call.
- [[async.log|The Log & Kafka]] — The append-only log as system of record; partitions, consumer groups, offsets, retention.
- [[async.delivery.guarantees|Delivery Guarantees]] — At-most-once vs at-least-once, ordering scope, dead-letter queues and poison pills.
- [[async.delivery.exactly-once|Effectively Exactly-Once]] — Idempotent producers, transactional consume-process-produce, and why end-to-end exactly-once is a composition, not a feature.
- [[async.streaming.cdc|CDC & Event Sourcing]] — Change data capture mechanics, initial snapshots, log compaction, and event sourcing as a contrast.
- [[async.streaming.processing|Stream Processing]] — Event time vs processing time, windows and watermarks, stream joins, and fault-tolerant state.
- [[analytics.olap|OLTP vs OLAP & Columnar]] — Why analytical scans want column layout, compression, and vectorized execution instead of B-trees.
- [[analytics.warehouse|Warehouses & Lakehouses]] — Warehouse vs data lake vs lakehouse; open table formats (Iceberg/Delta) over object storage.
- [[analytics.batch|Batch Processing]] — MapReduce lineage to Spark; shuffles, distributed joins, idempotent reruns, and batch vs stream boundaries.
- [[analytics.derived|Derived Data & Materialized Views]] — Treating caches, indexes, and views as recomputable projections of a log — and keeping them fresh.
- [[correctness.idempotency|Idempotency]] — Idempotency keys, dedup windows, and designing every mutation to survive a retry.
- [[correctness.outbox|Dual Writes & Outbox]] — Why writing DB-then-publish loses events, and how the transactional outbox closes the gap.
- [[correctness.saga|Sagas]] — Long-running workflows via compensating actions when a distributed transaction is off the table.
- [[correctness.ledger|Ledgers & Reconciliation]] — Double-entry design, immutability, balance derivation, and reconciliation as the payments-grade safety net.
- [[architecture.services|Monoliths & Microservices]] — When to split, service boundaries by data ownership, and the operational bill microservices arrive with.
- [[architecture.discovery|Service Discovery & Contracts]] — Registries, health checking, API versioning, and evolving schemas without breaking consumers.
- [[architecture.serverless|Serverless]] — FaaS execution model, cold starts, and where per-request pricing beats owning servers.
- [[reliability.availability|Availability Math]] — Nines, serial vs parallel composition, redundancy patterns, failover modes and their data-loss windows.
- [[reliability.resilience.retries|Timeouts & Retries]] — Timeout budgets, deadline propagation, exponential backoff with jitter, retry storms and retry budgets.
- [[reliability.resilience.containment|Failure Containment]] — Circuit breakers, bulkheads, load shedding, chaos engineering, and safe deployment strategies.
- [[reliability.slo|SLOs & Error Budgets]] — SLIs worth measuring, percentiles over averages, and error budgets as a release throttle.
- [[reliability.observability|Observability]] — Structured logs, metrics, distributed traces; correlation ids and cardinality costs.
- [[reliability.multi-region|Multi-Region]] — Active-passive vs active-active, data residency, RPO/RTO, and why failover you never test doesn't exist.
- [[infra.containers|Containers & Orchestration]] — Containers vs VMs, Kubernetes primitives (pods, services, autoscaling) at design-conversation depth.
- [[infra.mesh|Service Mesh]] — Sidecars and ambient meshes — mTLS, retries, and traffic policy moved out of application code, at a latency cost.
- [[infra.delivery|CI/CD & Progressive Delivery]] — Pipelines, canary and blue-green automation, feature flags, and config/schema changes as deploys.
- [[security.authn.tokens|Sessions & Tokens]] — Server sessions vs JWTs, access/refresh pairs, rotation and reuse detection, sender-constrained tokens.
- [[security.authn.oauth|OAuth2 & OIDC]] — Authorization-code + PKCE flow, what OIDC adds on top, which flow for which client.
- [[security.authn.credentials|Passwords & Passkeys]] — Credential storage, phishing resistance, and the WebAuthn/passkey model.
- [[security.authz|Authorization & API Security]] — RBAC vs ABAC, API keys vs user tokens, TLS everywhere, secrets handling.
- [[ai.foundations|LLM Foundations for Engineers]] — What an LLM actually does at serving time — tokens, context windows, embeddings, prefill/decode — no ML math required.
- [[ai.vector-search|Vector Search]] — Embeddings as vectors, ANN indexes (HNSW/IVF), hybrid retrieval, and freshness of the indexed corpus.
- [[ai.rag|RAG Pipelines]] — Chunking, retrieval, reranking, and grounding as a data pipeline — where quality is won and lost.
- [[ai.inference|Inference Serving]] — GPU batching, KV-cache reuse, streaming responses, and cost/latency levers unique to LLM backends.
- [[ai.evals|Evals & AI Observability]] — Offline vs online evaluation, LLM-as-judge, regression suites for prompts, and tracing AI pipelines.
%% trellis:end %%

## Notes
