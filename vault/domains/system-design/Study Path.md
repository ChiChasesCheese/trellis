%% trellis:begin %%
# System Design — study path

## Core

*44 of 125 topics: the declared Core and what it requires. Anki deals these first.*

**Foundations**
- [ ] [[foundations.method|Interview Method]] — 6 cards
- [ ] [[foundations.estimation|Back-of-Envelope Estimation]] — 5 cards
- [ ] [[foundations.numbers|Latency Numbers]] — 7 cards
- [ ] [[foundations.tradeoffs|Core Trade-offs]] — 7 cards
**Networking & APIs**
- [ ] [[networking.dns|DNS]] — 6 cards
- [ ] [[networking.realtime|Realtime Delivery]] — 6 cards
- [ ] [[networking.cdn|CDN]] — 6 cards
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
- [ ] [[storage.object|Object Storage & Separation]] — 6 cards
**Distributed Data**
- [ ] [[distributed.cap|CAP & PACELC]] — 5 cards
- [ ] [[distributed.consistency|Consistency Models]] — 8 cards
- [ ] [[distributed.replication.leader|Leader-Based]] — 6 cards
- [ ] [[distributed.replication.multi-leader|Multi-Leader]] — 7 cards
- [ ] [[distributed.replication.leaderless|Leaderless & Quorums]] — 7 cards
- [ ] [[distributed.partitioning.schemes|Hash vs Range]] — 6 cards
- [ ] [[distributed.transactions.isolation|Isolation Levels & Anomalies]] — 8 cards
- [ ] [[distributed.crdt|CRDTs & Local-First]] — 6 cards; needs: Replication
**Async & Streaming**
- [ ] [[async.queues|Message Queues]] — 6 cards
- [ ] [[async.log|The Log & Kafka]] — 8 cards; needs: Storage Engine Internals
- [ ] [[async.delivery.guarantees|Delivery Guarantees]] — 6 cards
- [ ] [[async.delivery.exactly-once|Effectively Exactly-Once]] — 5 cards
**Correctness Patterns**
- [ ] [[correctness.idempotency|Idempotency]] — 7 cards; needs: Delivery Semantics
- [ ] [[correctness.ledger|Ledgers & Reconciliation]] — 9 cards; needs: Idempotency
**Reliability & Operations**
- [ ] [[reliability.resilience.retries|Timeouts & Retries]] — 5 cards
**Design Problems**
- [ ] [[problems.foundations.url-shortener|URL Shortener]] — 8 cards; needs: Write & Read Strategies, NoSQL Families
- [ ] [[problems.foundations.rate-limiter|Distributed Rate Limiter]] — 8 cards; needs: Rate Limiting
- [ ] [[problems.social.chat-messaging|Chat & Messaging (WhatsApp)]] — 8 cards; needs: Realtime Delivery, Message Queues
- [ ] [[problems.social.news-feed|News Feed & Timeline (Twitter/Facebook)]] — 8 cards; needs: Write & Read Strategies, Message Queues
- [ ] [[problems.social.instagram|Photo Sharing (Instagram)]] — 8 cards; needs: Object Storage & Separation, CDN
- [ ] [[problems.media.video-streaming|Video Streaming (YouTube/Netflix)]] — 8 cards; needs: CDN, Object Storage & Separation
- [ ] [[problems.media.google-docs|Collaborative Editing (Google Docs)]] — 8 cards; needs: CRDTs & Local-First, Realtime Delivery
- [ ] [[problems.media.file-sync|File Sync (Dropbox/Google Drive)]] — 8 cards; needs: Object Storage & Separation, Consistency Models
- [ ] [[problems.search.web-crawler|Web Crawler]] — 8 cards; needs: Message Queues, DNS
- [ ] [[problems.geo.proximity|Proximity & Nearby Search (Yelp)]] — 8 cards; needs: Indexing
- [ ] [[problems.commerce.payment-system|Payment System]] — 8 cards; needs: Idempotency, Ledgers & Reconciliation
## The rest

**Networking & APIs**
- [ ] [[networking.protocols|Transport & HTTP]] — 6 cards
- [ ] [[networking.api-styles|REST, gRPC & GraphQL]] — 6 cards
**Load Balancing & Traffic**
- [ ] [[traffic.gateways|Reverse Proxies & API Gateways]] — 6 cards
**Caching**
- [ ] [[caching.placement|Cache Placement]] — 6 cards
**Storage**
- [ ] [[storage.record-modeling|Record Modeling]] — 3 cards
- [ ] [[storage.search|Search Indexes]] — 6 cards
- [ ] [[storage.encoding|Encoding & Evolution]] — 9 cards
**Distributed Data**
- [ ] [[distributed.partitioning.rebalancing|Rebalancing & Routing]] — 6 cards
- [ ] [[distributed.partitioning.skew|Hot Keys & Skew]] — 5 cards
- [ ] [[distributed.partitioning.indexes|Partitioned Secondary Indexes]] — 5 cards
- [ ] [[distributed.transactions.concurrency-control|Concurrency Control]] — 7 cards
- [ ] [[distributed.transactions.distributed|Distributed Transactions]] — 6 cards
- [ ] [[distributed.consensus|Consensus]] — 10 cards; needs: Replication
- [ ] [[distributed.time.clocks|Clocks & Timestamps]] — 6 cards
- [ ] [[distributed.time.failure|Failure Detection & Pauses]] — 4 cards
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
**Design Problems**
- [ ] [[problems.foundations.unique-id-generator|Unique ID Generator]] — 8 cards; needs: Clocks & Timestamps
- [ ] [[problems.foundations.key-value-store|Distributed Key-Value Store]] — 8 cards; needs: Leaderless & Quorums, Hash vs Range
- [ ] [[problems.foundations.distributed-cache|Distributed Cache]] — 8 cards; needs: Invalidation & Eviction, Hot Keys & Skew
- [ ] [[problems.foundations.cdn|Content Delivery Network]] — 8 cards; needs: CDN, Cache Placement
- [ ] [[problems.foundations.message-queue|Distributed Message Queue]] — 8 cards; needs: The Log & Kafka, Delivery Guarantees
- [ ] [[problems.foundations.job-scheduler|Distributed Job Scheduler]] — 8 cards; needs: Message Queues, Idempotency
- [ ] [[problems.foundations.pastebin|Pastebin]] — 8 cards; needs: Object Storage & Separation
- [ ] [[problems.foundations.object-storage|Object Storage (S3)]] — 8 cards; needs: Object Storage & Separation
- [ ] [[problems.foundations.lock-service|Distributed Lock & Coordination Service]] — 8 cards; needs: Consensus
- [ ] [[problems.foundations.auth-service|Authentication & Identity Service]] — 9 cards; needs: Sessions & Tokens
- [ ] [[problems.social.notification-system|Notification System]] — 8 cards; needs: Message Queues, Idempotency
- [ ] [[problems.social.reddit|Forum & Threaded Comments (Reddit)]] — 8 cards; needs: Write & Read Strategies
- [ ] [[problems.social.social-graph-search|Social Graph & Friend Search]] — 8 cards; needs: Hash vs Range
- [ ] [[problems.social.live-comments|Live Comments]] — 8 cards; needs: Realtime Delivery
- [ ] [[problems.social.tinder|Dating & Matching (Tinder)]] — 8 cards; needs: Consistency Models
- [ ] [[problems.media.email-service|Email Service (Gmail)]] — 7 cards; needs: Search Indexes
- [ ] [[problems.media.video-conferencing|Video Conferencing (Zoom)]] — 8 cards; needs: Realtime Delivery
- [ ] [[problems.search.search-engine|Search Engine & Post Search]] — 8 cards; needs: Search Indexes
- [ ] [[problems.search.typeahead|Typeahead & Autocomplete]] — 8 cards; needs: Write & Read Strategies
- [ ] [[problems.search.top-k|Top-K & Trending (Heavy Hitters)]] — 8 cards; needs: Stream Processing
- [ ] [[problems.search.metrics-monitoring|Metrics, Monitoring & Alerting]] — 8 cards; needs: Observability
- [ ] [[problems.search.ad-click-aggregation|Ad Click Aggregation]] — 8 cards; needs: Stream Processing, Effectively Exactly-Once
- [ ] [[problems.search.news-aggregator|News Aggregator (Google News)]] — 8 cards; needs: Message Queues
- [ ] [[problems.geo.ride-hailing|Ride Hailing (Uber)]] — 7 cards; needs: Consistency Models, Realtime Delivery
- [ ] [[problems.geo.google-maps|Maps & Navigation (Google Maps)]] — 8 cards; needs: CDN
- [ ] [[problems.geo.food-delivery|Food & Grocery Delivery (DoorDash/Gopuff)]] — 8 cards; needs: Sagas
- [ ] [[problems.realtime.online-judge|Online Judge (LeetCode)]] — 8 cards; needs: Message Queues, Containers & Orchestration
- [ ] [[problems.realtime.multiplayer-game|Online Multiplayer Game (Chess)]] — 8 cards; needs: Realtime Delivery
- [ ] [[problems.realtime.llm-chat-service|LLM Chat Service (ChatGPT)]] — 8 cards; needs: Inference Serving
- [ ] [[problems.realtime.calendar|Calendar & Scheduling (Google Calendar)]] — 8 cards; needs: Indexing
- [ ] [[problems.realtime.leaderboard|Real-Time Leaderboard]] — 8 cards; needs: Write & Read Strategies
- [ ] [[problems.commerce.stock-exchange|Stock Exchange & Trading (Robinhood)]] — 8 cards; needs: Consensus
- [ ] [[problems.commerce.ticket-booking|Ticket Booking (Ticketmaster)]] — 7 cards; needs: Isolation Levels & Anomalies
- [ ] [[problems.commerce.hotel-reservation|Hotel & Marketplace Reservation (Airbnb)]] — 8 cards; needs: Isolation Levels & Anomalies
- [ ] [[problems.commerce.digital-wallet|Digital Wallet]] — 8 cards; needs: Distributed Transactions, Ledgers & Reconciliation
- [ ] [[problems.commerce.auction|Online Auction (eBay)]] — 8 cards; needs: Concurrency Control
- [ ] [[problems.commerce.e-commerce|E-Commerce Platform (Amazon)]] — 9 cards; needs: Sagas
- [ ] [[problems.commerce.flash-sale|Flash Sale & High-Contention Inventory]] — 8 cards; needs: Rate Limiting, Concurrency Control
%% trellis:end %%

## Notes
