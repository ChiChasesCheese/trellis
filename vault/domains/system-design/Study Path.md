%% trellis:begin %%
# System Design — study path

## Core

*25 of 76 topics: the declared Core and what it requires. Anki deals these first.*

**Foundations**
- [ ] [[foundations.method|Interview Method]] — 6 cards
- [ ] [[foundations.estimation|Back-of-Envelope Estimation]] — 5 cards
- [ ] [[foundations.numbers|Latency Numbers]] — 7 cards
- [ ] [[foundations.tradeoffs|Core Trade-offs]] — 7 cards
**Load Balancing & Traffic**
- [ ] [[traffic.load-balancing|Load Balancers]] — 6 cards
- [ ] [[traffic.rate-limiting|Rate Limiting]] — 8 cards
**Caching**
- [ ] [[caching.strategies|Write & Read Strategies]] — 6 cards
- [ ] [[caching.invalidation|Invalidation & Eviction]] — 6 cards
**Storage**
- [ ] [[storage.relational.indexing|Indexing]] — 7 cards
- [ ] [[storage.relational.operations|Operating at Scale]] — 7 cards
- [ ] [[storage.internals.btree|B-tree Mechanics]] — 5 cards
- [ ] [[storage.internals.lsm|LSM-tree Mechanics]] — 6 cards
- [ ] [[storage.internals.tradeoffs|Engine Trade-offs]] — 5 cards
- [ ] [[storage.nosql|NoSQL Families]] — 9 cards
**Distributed Data**
- [ ] [[distributed.cap|CAP & PACELC]] — 5 cards
- [ ] [[distributed.consistency|Consistency Models]] — 8 cards
- [ ] [[distributed.replication.leader|Leader-Based]] — 6 cards
- [ ] [[distributed.partitioning.schemes|Hash vs Range]] — 6 cards
- [ ] [[distributed.transactions.isolation|Isolation Levels & Anomalies]] — 8 cards
**Async & Streaming**
- [ ] [[async.queues|Message Queues]] — 6 cards
- [ ] [[async.log|The Log & Kafka]] — 8 cards; needs: Storage Engine Internals
- [ ] [[async.delivery.guarantees|Delivery Guarantees]] — 6 cards
- [ ] [[async.delivery.exactly-once|Effectively Exactly-Once]] — 5 cards
**Correctness Patterns**
- [ ] [[correctness.idempotency|Idempotency]] — 7 cards; needs: Delivery Semantics
**Reliability & Operations**
- [ ] [[reliability.resilience.retries|Timeouts & Retries]] — 5 cards
## The rest

**Networking & APIs**
- [ ] [[networking.protocols|Transport & HTTP]] — 6 cards
- [ ] [[networking.dns|DNS]] — 6 cards
- [ ] [[networking.api-styles|REST, gRPC & GraphQL]] — 6 cards
- [ ] [[networking.realtime|Realtime Delivery]] — 6 cards
- [ ] [[networking.cdn|CDN]] — 6 cards
**Load Balancing & Traffic**
- [ ] [[traffic.gateways|Reverse Proxies & API Gateways]] — 6 cards
**Caching**
- [ ] [[caching.placement|Cache Placement]] — 6 cards
**Storage**
- [ ] [[storage.record-modeling|Record Modeling]] — 3 cards
- [ ] [[storage.object|Object Storage & Separation]] — 6 cards
- [ ] [[storage.search|Search Indexes]] — 6 cards
- [ ] [[storage.encoding|Encoding & Evolution]] — 9 cards
**Distributed Data**
- [ ] [[distributed.replication.multi-leader|Multi-Leader]] — 7 cards
- [ ] [[distributed.replication.leaderless|Leaderless & Quorums]] — 7 cards
- [ ] [[distributed.partitioning.rebalancing|Rebalancing & Routing]] — 6 cards
- [ ] [[distributed.partitioning.skew|Hot Keys & Skew]] — 5 cards
- [ ] [[distributed.partitioning.indexes|Partitioned Secondary Indexes]] — 5 cards
- [ ] [[distributed.transactions.concurrency-control|Concurrency Control]] — 7 cards
- [ ] [[distributed.transactions.distributed|Distributed Transactions]] — 6 cards
- [ ] [[distributed.consensus|Consensus]] — 10 cards; needs: Replication
- [ ] [[distributed.time.clocks|Clocks & Timestamps]] — 6 cards
- [ ] [[distributed.time.failure|Failure Detection & Pauses]] — 4 cards
- [ ] [[distributed.crdt|CRDTs & Local-First]] — 6 cards; needs: Replication
**Async & Streaming**
- [ ] [[async.streaming.cdc|CDC & Event Sourcing]] — 5 cards
- [ ] [[async.streaming.processing|Stream Processing]] — 6 cards
**Analytics & Derived Data**
- [ ] [[analytics.olap|OLTP vs OLAP & Columnar]] — 7 cards; needs: Storage Engine Internals
- [ ] [[analytics.warehouse|Warehouses & Lakehouses]] — 5 cards; needs: Object Storage & Separation
- [ ] [[analytics.batch|Batch Processing]] — 7 cards
- [ ] [[analytics.derived|Derived Data & Materialized Views]] — 6 cards; needs: The Log & Kafka
**Correctness Patterns**
- [ ] [[correctness.outbox|Dual Writes & Outbox]] — 6 cards; needs: Transactions, Message Queues
- [ ] [[correctness.saga|Sagas]] — 6 cards; needs: Transactions
- [ ] [[correctness.ledger|Ledgers & Reconciliation]] — 9 cards; needs: Idempotency
**Architecture**
- [ ] [[architecture.services|Monoliths & Microservices]] — 6 cards
- [ ] [[architecture.discovery|Service Discovery & Contracts]] — 5 cards; needs: Encoding & Evolution
- [ ] [[architecture.serverless|Serverless]] — 5 cards
**Reliability & Operations**
- [ ] [[reliability.availability|Availability Math]] — 6 cards
- [ ] [[reliability.resilience.containment|Failure Containment]] — 9 cards
- [ ] [[reliability.slo|SLOs & Error Budgets]] — 6 cards
- [ ] [[reliability.observability|Observability]] — 7 cards
- [ ] [[reliability.multi-region|Multi-Region]] — 6 cards; needs: Replication, Consensus
**Platform & Infrastructure**
- [ ] [[infra.containers|Containers & Orchestration]] — 4 cards
- [ ] [[infra.mesh|Service Mesh]] — 4 cards; needs: Timeouts & Retries
- [ ] [[infra.delivery|CI/CD & Progressive Delivery]] — 6 cards; needs: Failure Containment
**Security**
- [ ] [[security.authn.tokens|Sessions & Tokens]] — 4 cards
- [ ] [[security.authn.oauth|OAuth2 & OIDC]] — 5 cards
- [ ] [[security.authn.credentials|Passwords & Passkeys]] — 5 cards
- [ ] [[security.authz|Authorization & API Security]] — 6 cards
**AI Systems**
- [ ] [[ai.foundations|LLM Foundations for Engineers]] — 5 cards
- [ ] [[ai.vector-search|Vector Search]] — 7 cards; needs: Search Indexes, LLM Foundations for Engineers
- [ ] [[ai.rag|RAG Pipelines]] — 5 cards; needs: Vector Search
- [ ] [[ai.inference|Inference Serving]] — 7 cards; needs: LLM Foundations for Engineers
- [ ] [[ai.evals|Evals & AI Observability]] — 5 cards
%% trellis:end %%

## Notes
