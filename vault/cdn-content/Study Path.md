%% trellis:begin %%
# CDN Content — study path

198 cards over 24 weeks ≈ 2 new cards/day.

## Week 1

**Performance Foundations**
- [ ] [[foundations.request-path|End-to-End Request Path]] — 3 cards
- [ ] [[foundations.os-io|Processes, Sockets & I/O]] — 3 cards
- [ ] [[foundations.concurrency|Concurrency, Parallelism & Queues]] — 3 cards
## Week 2

**Performance Foundations**
- [ ] [[foundations.performance|Latency, Throughput & Tail Behavior]] — 3 cards
- [ ] [[foundations.capacity|Capacity & Bottleneck Estimation]] — 3 cards; needs: Latency, Throughput & Tail Behavior
**Networking & HTTP**
- [ ] [[networking.dns-tcp-tls|DNS, TCP, TLS & Connection Setup]] — 3 cards; needs: End-to-End Request Path
## Week 3

**Networking & HTTP**
- [ ] [[networking.http-semantics|HTTP Semantics]] — 3 cards; needs: DNS, TCP, TLS & Connection Setup
- [ ] [[networking.http-versions|HTTP/1.1, HTTP/2 & HTTP/3]] — 3 cards; needs: HTTP Semantics
- [ ] [[networking.proxies|Reverse Proxies, Gateways & Routing]] — 3 cards; needs: HTTP Semantics
## Week 4

**Networking & HTTP**
- [ ] [[networking.streaming|Streaming & Backpressure]] — 3 cards; needs: Concurrency, Parallelism & Queues, HTTP Semantics
**CDN & Caching**
- [ ] [[caching.model|Browser, Shared Cache & CDN Model]] — 3 cards; needs: Reverse Proxies, Gateways & Routing
## Week 5

**CDN & Caching**
- [ ] [[caching.freshness|Freshness & Cache-Control]] — 3 cards; needs: Browser, Shared Cache & CDN Model
- [ ] [[caching.validators|Validators & Revalidation]] — 3 cards; needs: Freshness & Cache-Control
- [ ] [[caching.keys|Cache Keys, Vary & Representation Safety]] — 3 cards; needs: Freshness & Cache-Control
## Week 6

**CDN & Caching**
- [ ] [[caching.hierarchy|Multi-Tier Cache Hierarchy]] — 3 cards; needs: Cache Keys, Vary & Representation Safety
- [ ] [[caching.invalidation|Expiration, Purge & Invalidation]] — 3 cards; needs: Validators & Revalidation, Multi-Tier Cache Hierarchy
- [ ] [[caching.stampede|Stampede & Request Collapsing]] — 3 cards; needs: Multi-Tier Cache Hierarchy
## Week 7

**CDN & Caching**
- [ ] [[caching.eviction|Admission, Eviction & Hot Objects]] — 3 cards; needs: Multi-Tier Cache Hierarchy
- [ ] [[caching.failure|Negative Caching & Failure Policy]] — 3 cards; needs: Validators & Revalidation, Multi-Tier Cache Hierarchy
**Serving Runtimes**
- [ ] [[runtimes.go-http|Go HTTP Services]] — 3 cards; needs: Reverse Proxies, Gateways & Routing
## Week 8

**Serving Runtimes**
- [ ] [[runtimes.go-concurrency|Go Concurrency & Synchronization]] — 3 cards; needs: Concurrency, Parallelism & Queues, Go HTTP Services
- [ ] [[runtimes.go-lifecycle|Go Context, Timeouts & Shutdown]] — 3 cards; needs: Go Concurrency & Synchronization
## Week 9

**Serving Runtimes**
- [ ] [[runtimes.go-quality|Go Testing, Benchmarking & Profiling]] — 3 cards; needs: Go Context, Timeouts & Shutdown
- [ ] [[runtimes.node-event-loop|Node.js Event Loop]] — 3 cards; needs: Concurrency, Parallelism & Queues
- [ ] [[runtimes.node-streams|TypeScript, Node Streams & Backpressure]] — 3 cards; needs: Streaming & Backpressure, Node.js Event Loop
## Week 10

**Serving Runtimes**
- [ ] [[runtimes.lua-openresty|Lua & OpenResty Hot Path]] — 3 cards; needs: Reverse Proxies, Gateways & Routing
- [ ] [[runtimes.polyglot|Polyglot Boundaries]] — 3 cards; needs: Go HTTP Services, Node.js Event Loop, Lua & OpenResty Hot Path
**Content Lifecycle**
- [ ] [[content.rendering|CSR, SSR, SSG & Dynamic Rendering]] — 3 cards; needs: Browser, Shared Cache & CDN Model
## Week 11

**Content Lifecycle**
- [ ] [[content.static-generation|Static Generation & Build Output]] — 3 cards; needs: CSR, SSR, SSG & Dynamic Rendering
- [ ] [[content.isr|Incremental Static Regeneration]] — 3 cards; needs: Validators & Revalidation, Stampede & Request Collapsing, Static Generation & Build Output
- [ ] [[content.ppr|Partial Prerendering & Streaming]] — 3 cards; needs: Streaming & Backpressure, CSR, SSR, SSG & Dynamic Rendering
## Week 12

**Content Lifecycle**
- [ ] [[content.images|Image Optimization Pipeline]] — 3 cards; needs: Cache Keys, Vary & Representation Safety
- [ ] [[content.negotiation|Content Negotiation]] — 3 cards; needs: HTTP Semantics, Cache Keys, Vary & Representation Safety
## Week 13

**Content Lifecycle**
- [ ] [[content.range-compression|Range Requests & Compression]] — 3 cards; needs: HTTP Semantics
- [ ] [[content.versioning|Deployment, Versioning & Rollback]] — 3 cards; needs: Static Generation & Build Output, Expiration, Purge & Invalidation
**Distributed Architecture**
- [ ] [[distributed.regional-cache|Regional Cache Services]] — 3 cards; needs: Multi-Tier Cache Hierarchy
## Week 14

**Distributed Architecture**
- [ ] [[distributed.object-storage|Object Storage]] — 3 cards; needs: Static Generation & Build Output
- [ ] [[distributed.routing|Partitioning, Hashing & Request Routing]] — 3 cards; needs: Regional Cache Services
- [ ] [[distributed.consistency|Replication & Consistency]] — 3 cards; needs: Object Storage
## Week 15

**Distributed Architecture**
- [ ] [[distributed.cross-region|Cross-Region Architecture]] — 3 cards; needs: Partitioning, Hashing & Request Routing, Replication & Consistency
- [ ] [[distributed.retries|Timeouts, Retries & Idempotency]] — 3 cards; needs: Go Context, Timeouts & Shutdown, Replication & Consistency
- [ ] [[distributed.overload|Backpressure, Load Shedding & Circuit Breaking]] — 3 cards; needs: Streaming & Backpressure, Timeouts, Retries & Idempotency
## Week 16

**Distributed Architecture**
- [ ] [[distributed.skew|Hot Keys, Skew & Fleet Capacity]] — 3 cards; needs: Admission, Eviction & Hot Objects, Partitioning, Hashing & Request Routing
**Reliability & Observability**
- [ ] [[reliability.slos|SLIs, SLOs & Error Budgets]] — 3 cards; needs: Latency, Throughput & Tail Behavior
## Week 17

**Reliability & Observability**
- [ ] [[reliability.metrics|Metrics & Cardinality]] — 3 cards; needs: SLIs, SLOs & Error Budgets
- [ ] [[reliability.logging|Structured Logging]] — 3 cards; needs: SLIs, SLOs & Error Budgets
- [ ] [[reliability.tracing|Distributed Tracing]] — 3 cards; needs: Metrics & Cardinality, Structured Logging
## Week 18

**Reliability & Observability**
- [ ] [[reliability.alerting|Dashboards & Alerts]] — 3 cards; needs: Metrics & Cardinality
- [ ] [[reliability.testing|Unit, Integration & End-to-End Testing]] — 3 cards; needs: Negative Caching & Failure Policy, Go Testing, Benchmarking & Profiling
- [ ] [[reliability.load-testing|Load, Soak & Failure Testing]] — 3 cards; needs: Capacity & Bottleneck Estimation, Unit, Integration & End-to-End Testing
## Week 19

**Reliability & Observability**
- [ ] [[reliability.incidents|On-Call, Incidents & Postmortems]] — 3 cards; needs: Dashboards & Alerts, Load, Soak & Failure Testing
**Safe Delivery & Infrastructure**
- [ ] [[delivery.flags|Feature Flags & Kill Switches]] — 3 cards; needs: Dashboards & Alerts
- [ ] [[delivery.shadow|Shadow Mode & Dark Launches]] — 3 cards; needs: Feature Flags & Kill Switches, Metrics & Cardinality
## Week 20

**Safe Delivery & Infrastructure**
- [ ] [[delivery.canary|Canary & Progressive Deployment]] — 3 cards; needs: Feature Flags & Kill Switches, SLIs, SLOs & Error Budgets
- [ ] [[delivery.rollback|Post-Ship Validation & Rollback]] — 3 cards; needs: Shadow Mode & Dark Launches, Canary & Progressive Deployment
## Week 21

**Safe Delivery & Infrastructure**
- [ ] [[delivery.compatibility|Compatibility & Configuration Changes]] — 3 cards; needs: Deployment, Versioning & Rollback
- [ ] [[delivery.cicd|CI/CD & Release Evidence]] — 3 cards; needs: Unit, Integration & End-to-End Testing, Compatibility & Configuration Changes
- [ ] [[delivery.aws|AWS for Content Serving]] — 3 cards; needs: Regional Cache Services, Object Storage
## Week 22

**Safe Delivery & Infrastructure**
- [ ] [[delivery.terraform-kubernetes|Terraform & Kubernetes Basics]] — 3 cards; needs: CI/CD & Release Evidence, AWS for Content Serving
**Security & Cost**
- [ ] [[security-cost.isolation|Tenant & Personalization Isolation]] — 3 cards; needs: Cache Keys, Vary & Representation Safety
- [ ] [[security-cost.poisoning|Cache Poisoning & Key Confusion]] — 3 cards; needs: Tenant & Personalization Isolation
## Week 23

**Security & Cost**
- [ ] [[security-cost.request-integrity|Proxy Request Integrity]] — 3 cards; needs: Reverse Proxies, Gateways & Routing
- [ ] [[security-cost.abuse|Abuse, DDoS & Resource Limits]] — 3 cards; needs: Backpressure, Load Shedding & Circuit Breaking
- [ ] [[security-cost.signed-content|Signed URLs & Private Content]] — 3 cards; needs: Tenant & Personalization Isolation
## Week 24

**Security & Cost**
- [ ] [[security-cost.economics|CDN Unit Economics]] — 3 cards; needs: Capacity & Bottleneck Estimation, AWS for Content Serving
- [ ] [[security-cost.optimization|Performance-Cost Optimization]] — 3 cards; needs: Multi-Tier Cache Hierarchy, Metrics & Cardinality, CDN Unit Economics
%% trellis:end %%

## Notes
