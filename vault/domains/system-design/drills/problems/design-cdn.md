---
nodes: [problems.foundations.cdn, networking.cdn, caching.placement]
tags: [problem]
---
# Drill: Design a content delivery network (CDN)

Design the CDN itself — not a website that sits behind one — for a multi-tenant operator
serving customer origins worldwide: 300 edge PoPs, 17,361,111 peak requests/second across
all customers, a mix of small static assets and large video segments.

**Constraints to state and honor**
- Edge cache hit rate target ≥ 95%; edge-to-user P99 < 50ms on a hit.
- A purge request must reach every PoP that might hold a copy, with a P99 propagation
  target under 2 seconds — and this is a best-effort, eventually-consistent guarantee,
  never an atomic global swap.
- Any single PoP can fail without a customer-visible outage — only a bounded latency/
  capacity impact on its neighbors.
- Large objects (video, installers) must support parallel, resumable download via byte
  ranges, not a single whole-object GET.

**Grading points**
- Chooses anycast as the primary routing layer over GeoDNS-only and explains why the
  failover granularity differs by orders of magnitude (seconds vs. minutes), not just by
  implementation convenience
  ([[problems-cdn-anycast-vs-geodns-failover-granularity]], [[networking-anycast-vs-geodns]]).
- Inserts a regional origin-shield tier between edge and origin and computes how many
  independent origin fetches it collapses a viral object's traffic into, rather than
  asserting "it helps" without a number
  ([[problems-cdn-shield-reduces-origin-qps-5x]], [[problems-cdn-viral-object-shield-20x]]).
- Defines the cache key as exactly the bytes that change the response and identifies
  which common header (Cookie, full User-Agent) fragments the cache into near-zero hit
  rate if included carelessly
  ([[problems-cdn-cache-key-scope-and-vary]], [[networking-cdn-cache-key]]).
- Distinguishes purge-based invalidation from fingerprinted/versioned URLs, and picks
  versioned URLs for anything (like price) that cannot tolerate a propagation window of
  mixed old/new content
  ([[problems-cdn-purge-not-atomic-versioned-urls]], [[networking-cdn-purge-vs-versioning]]).
- Explains why a single connection's throughput is capped by the bandwidth-delay product
  and why parallel range-request segments raise achievable throughput past that cap
  ([[problems-cdn-bdp-limits-parallel-segments-fix]], [[storage-multipart-ranged-io]]).
- Computes the load a surviving PoP absorbs when a neighbor in its shield group fails,
  and states that shield-group size is a capacity-planning lever between shielding
  efficiency and failure blast radius
  ([[problems-cdn-pop-failure-5pct-neighbor-overload]]).
- Identifies that a single hot object can exceed one edge node's NIC/CPU capacity even
  at 100% cache hit rate, and that the fix is key replication across nodes, not more
  shards ([[caching-hot-key-replication]]).
- States what changes at 10x traffic: the shield tier's fixed absorption percentage
  means origin-bound QPS scales linearly with traffic, so origin protection needs a
  second, cross-regional aggregation tier, not just a bigger origin
  ([[problems-cdn-10x-needs-second-shield-tier]]).

**Solution**: [[solution-cdn]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
