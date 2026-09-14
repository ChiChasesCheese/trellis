%% trellis:begin %%
# System Design — study path

345 cards over 8 weeks ≈ 7 new cards/day.

## Week 1

**Foundations**
- [ ] [[foundations.method|Interview Method]] — 6 cards
- [ ] [[foundations.estimation|Back-of-Envelope Estimation]] — 5 cards
- [ ] [[foundations.numbers|Latency Numbers]] — 7 cards
- [ ] [[foundations.tradeoffs|Core Trade-offs]] — 5 cards
**Networking & APIs**
- [ ] [[networking.protocols|Transport & HTTP]] — 6 cards
- [ ] [[networking.dns|DNS]] — 6 cards
- [ ] [[networking.api-styles|REST, gRPC & GraphQL]] — 6 cards
- [ ] [[networking.realtime|Realtime Delivery]] — 6 cards
## Week 2

**Networking & APIs**
- [ ] [[networking.cdn|CDN]] — 6 cards
**Load Balancing & Traffic**
- [ ] [[traffic.load-balancing|Load Balancers]] — 6 cards
- [ ] [[traffic.gateways|Reverse Proxies & API Gateways]] — 6 cards
- [ ] [[traffic.rate-limiting|Rate Limiting]] — 6 cards
**Caching**
- [ ] [[caching.strategies|Write & Read Strategies]] — 6 cards
- [ ] [[caching.invalidation|Invalidation & Eviction]] — 6 cards
- [ ] [[caching.placement|Cache Placement]] — 6 cards
## Week 3

**Storage**
- [ ] [[storage.relational.indexing|Indexing]] — 2 cards
- [ ] [[storage.relational.operations|Operating at Scale]] — 4 cards
- [ ] [[storage.internals|B-trees vs LSM-trees]] — 6 cards
- [ ] [[storage.nosql|NoSQL Families]] — 6 cards
- [ ] [[storage.object|Object Storage & Separation]] — 6 cards
- [ ] [[storage.search|Search Indexes]] — 6 cards
- [ ] [[storage.encoding|Encoding & Evolution]] — 5 cards
**Distributed Data**
- [ ] [[distributed.cap|CAP & PACELC]] — 5 cards
- [ ] [[distributed.consistency|Consistency Models]] — 6 cards
## Week 4

**Distributed Data**
- [ ] [[distributed.replication.leader|Leader-Based]] — 4 cards
- [ ] [[distributed.replication.multi-leader|Multi-Leader]] — 1 cards
- [ ] [[distributed.replication.leaderless|Leaderless & Quorums]] — 2 cards
- [ ] [[distributed.partitioning.schemes|Hash vs Range]] — 2 cards
- [ ] [[distributed.partitioning.rebalancing|Rebalancing & Routing]] — 2 cards
- [ ] [[distributed.partitioning.skew|Hot Keys & Skew]] — 1 cards
- [ ] [[distributed.partitioning.indexes|Partitioned Secondary Indexes]] — 1 cards
- [ ] [[distributed.transactions.isolation|Isolation Levels & Anomalies]] — 3 cards
- [ ] [[distributed.transactions.concurrency-control|Concurrency Control]] — 3 cards
- [ ] [[distributed.transactions.distributed|Distributed Transactions]] — 1 cards
- [ ] [[distributed.consensus|Consensus]] — 7 cards; needs: Replication
- [ ] [[distributed.time|Clocks & Ordering]] — 6 cards
- [ ] [[distributed.crdt|CRDTs & Local-First]] — 5 cards; needs: Replication
## Week 5

**Async & Streaming**
- [ ] [[async.queues|Message Queues]] — 6 cards
- [ ] [[async.log|The Log & Kafka]] — 6 cards; needs: B-trees vs LSM-trees
- [ ] [[async.delivery.guarantees|Delivery Guarantees]] — 3 cards
- [ ] [[async.delivery.exactly-once|Effectively Exactly-Once]] — 3 cards
- [ ] [[async.streaming|Stream Processing & CDC]] — 6 cards
**Analytics & Derived Data**
- [ ] [[analytics.olap|OLTP vs OLAP & Columnar]] — 5 cards; needs: B-trees vs LSM-trees
- [ ] [[analytics.warehouse|Warehouses & Lakehouses]] — 5 cards; needs: Object Storage & Separation
- [ ] [[analytics.batch|Batch Processing]] — 5 cards
- [ ] [[analytics.derived|Derived Data & Materialized Views]] — 5 cards; needs: The Log & Kafka
## Week 6

**Correctness Patterns**
- [ ] [[correctness.idempotency|Idempotency]] — 7 cards; needs: Delivery Semantics
- [ ] [[correctness.outbox|Dual Writes & Outbox]] — 6 cards; needs: Transactions, Message Queues
- [ ] [[correctness.saga|Sagas]] — 6 cards; needs: Transactions
- [ ] [[correctness.ledger|Ledgers & Reconciliation]] — 8 cards; needs: Idempotency
**Architecture**
- [ ] [[architecture.services|Monoliths & Microservices]] — 6 cards
- [ ] [[architecture.discovery|Service Discovery & Contracts]] — 5 cards; needs: Encoding & Evolution
- [ ] [[architecture.serverless|Serverless]] — 5 cards
## Week 7

**Reliability & Operations**
- [ ] [[reliability.availability|Availability Math]] — 6 cards
- [ ] [[reliability.resilience.retries|Timeouts & Retries]] — 2 cards
- [ ] [[reliability.resilience.containment|Failure Containment]] — 5 cards
- [ ] [[reliability.slo|SLOs & Error Budgets]] — 6 cards
- [ ] [[reliability.observability|Observability]] — 6 cards
- [ ] [[reliability.multi-region|Multi-Region]] — 6 cards; needs: Replication, Consensus
**Platform & Infrastructure**
- [ ] [[infra.containers|Containers & Orchestration]] — 4 cards
- [ ] [[infra.mesh|Service Mesh]] — 4 cards; needs: Timeouts & Retries
- [ ] [[infra.delivery|CI/CD & Progressive Delivery]] — 4 cards; needs: Failure Containment
## Week 8

**Security**
- [ ] [[security.authn.tokens|Sessions & Tokens]] — 4 cards
- [ ] [[security.authn.oauth|OAuth2 & OIDC]] — 2 cards
- [ ] [[security.authn.credentials|Passwords & Passkeys]] — 1 cards
- [ ] [[security.authz|Authorization & API Security]] — 6 cards
**AI Systems**
- [ ] [[ai.foundations|LLM Foundations for Engineers]] — 5 cards
- [ ] [[ai.vector-search|Vector Search]] — 7 cards; needs: Search Indexes, LLM Foundations for Engineers
- [ ] [[ai.rag|RAG Pipelines]] — 5 cards; needs: Vector Search
- [ ] [[ai.inference|Inference Serving]] — 7 cards; needs: LLM Foundations for Engineers
- [ ] [[ai.evals|Evals & AI Observability]] — 5 cards
%% trellis:end %%

## Notes
