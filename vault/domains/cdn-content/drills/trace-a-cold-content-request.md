---
nodes: [foundations.request-path, networking.dns-tcp-tls, networking.proxies, caching.hierarchy, distributed.object-storage]
tags: [foundation, serving-path]
---
# Drill: Trace a cold content request

Explain one first-time request for a large immutable asset from a browser to a
global CDN, through every cache tier to object storage, and back to the client.

**Constraints to state and honor**
- The browser has no DNS, TLS, or HTTP connection state.
- The edge, regional cache, and shield all miss.
- The object is 40 MB and the client requests only its final 2 MB.
- A second request for the same range arrives while the first fill is running.

**Grading points**
- DNS, TCP or QUIC, TLS, connection reuse, and where TTFB is accumulated.
- Which component is a reverse proxy and which headers it must preserve or remove.
- Cache-key and representation decision before every lookup.
- Range behavior and whether a tier stores the range or the complete object.
- Request collapsing scope and what happens when the object-store read fails.
- Metrics and trace spans needed to prove the explanation against production data.

**Attempt log**
- [ ] Attempt 1 (date, 30 min, self-graded notes):

