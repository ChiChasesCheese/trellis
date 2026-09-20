---
nodes: [problems.geo.google-maps, networking.cdn]
tags: [problem]
---
# Drill: Design a maps and navigation service like Google Maps

Design the backend for a Google Maps-style product: users pan and zoom a map, request a
driving route between two points with an ETA, get the route rerouted automatically if they
deviate, and can download a region for fully offline use.

**Constraints to state and honor**
- Roughly 800 million daily active users at 1.5 sessions/day; in-trip ETA refresh traffic
  runs about 40x the rate of initial route requests, so the two paths need very different
  cost profiles.
- Point-to-point route computation must stay under 500ms P99 even for routes spanning a
  continental-scale road network with tens of millions of nodes.
- Tiles are read-heavy, immutable, and CDN-cacheable; the road graph's topology changes
  slowly but live traffic weights change minute to minute.
- Offline downloads must support full turn-by-turn navigation, not just viewing the map.

**Grading points**
- Explains why the huge gap between in-trip ETA-refresh volume and initial route-request
  volume forces a separate, cheap incremental-update path instead of re-running full route
  planning on every refresh ([[problems-google-maps-eta-refresh-vs-route-qps]],
  [[problems-google-maps-eta-refresh-endpoint-decision]]).
- Explains why plain Dijkstra fails at continental scale and how Contraction Hierarchies
  moves that cost into offline preprocessing via node contraction and shortcut edges
  ([[problems-google-maps-contraction-hierarchies-mechanism]]).
- Can argue why a partitioned hierarchical routing method is chosen over plain Contraction
  Hierarchies once live traffic updates are a requirement, not just an afterthought
  ([[problems-google-maps-ch-vs-mld-tradeoff]]).
- Describes how live ETA is built from aggregated location probes and a graph neural network
  over road-segment groups, citing a concrete, sourced accuracy result rather than an
  unverified number ([[problems-google-maps-gnn-eta-supersegment]]).
- States a concrete degradation path when the traffic/ETA service is unavailable — falling
  back to historical average speeds rather than rejecting requests
  ([[problems-google-maps-eta-outage-fallback]]).
- Explains what has to change about road-graph partitioning at 10x scale and the tension
  between partition size and cross-partition query overhead
  ([[problems-google-maps-10x-graph-partition-finer]]).
- Recognizes that an offline download needs a self-contained road subgraph with a boundary
  buffer, not just cached tiles, to support offline routing at all
  ([[problems-google-maps-offline-needs-road-subgraph]]).
- Connects tile delivery to CDN caching principles — why tiles are an ideal CDN workload
  (immutable, key-addressable, high reuse) — without re-deriving CDN internals.

**Solution**: [[solution-google-maps]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
