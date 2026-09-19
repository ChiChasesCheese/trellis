You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "networking.protocols": ["<id shown first>", "…"],
  "networking.dns": ["<id shown first>", "…"],
  "networking.api-styles": ["<id shown first>", "…"],
  …
}

## networking.protocols — Transport & HTTP
TCP vs UDP guarantees and costs; HTTP semantics, keep-alive, HTTP/2 and 3 in one breath.
- `networking-connection-pooling` Q: A service calls a downstream over HTTP/1.1 through a 50-connection pool. Load rises; downstream "latency" explodes while both ends sit at low CPU. Mechanism — and what changes under HTTP/2?
  A: **Pool exhaustion.** HTTP/1.1 allows one in-flight request per connection, so the 51st concurrent request queues waiting for a free connection — that queue wait
- `networking-connection-setup-cost` Q: A cold HTTPS request pays {{c1::1 RTT for the TCP handshake + 1 RTT for TLS 1.3}} before any application byte moves — on a 100 ms cross-region path that's ~200 ms of pure setup. This is why services use {{c2::keep-alive / connection pooling}} between fixed peers, and why QUIC offers {{c3::0-RTT resumption}} for repeat visitors.
- `networking-http1-hol-workarounds` Q: HTTP/1.1's head-of-line blocking lives at the application layer. What exactly blocks, and which browser-era hacks did it force (now anti-patterns under HTTP/2)?
  A: One connection carries **one request at a time**; responses must come back in order, and pipelining broke on middleboxes so browsers disabled it — leaving ~6 pa
- `networking-http2-vs-http3` Q: HTTP/2 multiplexes many streams over one TCP connection. What problem remains, and how does HTTP/3 fix it?
  A: **TCP-level head-of-line blocking**: one lost packet stalls *every* HTTP/2 stream on that connection until retransmission, because TCP delivers bytes in order. 
- `networking-tcp-vs-udp` Q: When is UDP the right transport despite giving up TCP's guarantees? Name the guarantees you're dropping and two workloads that want that.
  A: Dropping: **ordering, retransmission, and connection state** — which means no head-of-line blocking and no handshake/teardown cost. - **Live media / voice / gam
- `networking-tls-resumption` Q: TLS 1.3 session resumption: how do session tickets cut handshake cost, and why must 0-RTT early data be idempotent?
  A: After a full handshake the server issues an encrypted **session ticket**; on reconnect the client presents it as a pre-shared key — resuming without certificate

## networking.dns — DNS
Resolution path, record types, TTL as a blunt failover and traffic-steering instrument.
- `networking-anycast-vs-geodns` Q: Anycast vs GeoDNS for steering users to the nearest site — mechanism and weakness of each?
  A: - **Anycast**: the *same* IP announced via BGP from many sites; the network routes each client to the topologically closest. Failover is instant (withdraw the r
- `networking-dns-lb-failover-layers` Q: Health-checked DNS (e.g. Route 53) can drop a dead region from its answers. Why do you still need LB-level failover underneath — how is the labor divided?
  A: DNS failover operates at **minutes** granularity: health-check interval + record TTL + resolvers that ignore TTLs ([[networking-dns-ttl-failover]]). That's acce
- `networking-dns-negative-caching` Q: You delete a DNS record by mistake and resolvers start returning NXDOMAIN. You fix the zone — but clients keep failing. Why?
  A: **Negative caching**: resolvers cache NXDOMAIN/NODATA answers too, for the negative TTL — min(SOA MINIMUM field, SOA record's own TTL). Your fix only takes effe
- `networking-dns-record-types` Q: A vs CNAME vs ALIAS/ANAME: which do you use at a zone apex pointing to a load balancer's changing IPs, and why?
  A: - **A/AAAA**: name → IP. Breaks when the LB's IPs change. - **CNAME**: name → another name. Correct for `www`, but **forbidden at the apex** (`example.com`) bec
- `networking-dns-resolution-path` Q: Trace an uncached lookup of `api.example.com` from the browser to an answer. Where do caches sit in that path?
  A: Client stub resolver → **recursive resolver** (ISP or 8.8.8.8) which walks: **root** servers ("ask `.com`") → **TLD** servers ("ask example.com's nameservers") 
- `networking-dns-ttl-failover` Q: Why is DNS a blunt instrument for failover, and what two things do teams do about it?
  A: Because you can't force clients to forget: cached records live until **TTL expires**, and some resolvers/apps ignore TTLs or pin connections — so after a DNS sw

## networking.api-styles — REST, gRPC & GraphQL
Choosing an API style by coupling, payload shape, streaming needs, and who owns the clients.
- `networking-cursor-vs-offset-pagination` Q: Offset vs cursor pagination in an API — what breaks with `OFFSET` at depth and under concurrent writes?
  A: - **Cost**: `OFFSET n` scans and discards n rows — page 10,000 does O(n) work; deep pagination becomes a DB DoS. - **Instability**: rows inserted/deleted betwee
- `networking-graphql-when-and-cost` Q: What client situation makes GraphQL earn its complexity, and what two operational problems does it import?
  A: Earns it when **many diverse clients need different slices of the same graph** (mobile vs web vs partners) — clients query exactly the fields they need, killing
- `networking-grpc-over-rest` Q: When choose gRPC over REST for service-to-service calls — and what do you give up?
  A: Choose gRPC when **you own both ends**: internal microservices wanting compact binary payloads (protobuf), generated typed clients, low per-call overhead, and f
- `networking-grpc-streaming-modes` Q: gRPC's four call types — match each to its use, and name the operational caveat long-lived streams create.
  A: - **Unary**: ordinary request/response — the default. - **Server-streaming**: subscriptions and feeds — replaces client polling with pushed increments. - **Clie
- `networking-rest-as-default` Q: Why does REST over JSON remain the default for public APIs in 2026, despite gRPC and GraphQL?
  A: Because a public API's clients are **unknown and uncontrolled**, and REST maximizes what strangers get for free: - Works from any HTTP client, browser, or `curl
- `networking-webhooks-vs-polling` Q: Exposing events to third-party integrators: webhooks vs letting them poll. What must a webhook provider build that polling gives for free?
  A: Delivery machinery, because consumer endpoints are down or slow constantly: - **Retries with backoff + dead-letter handling** — and since retries reorder and du

## networking.realtime — Realtime Delivery
Long polling vs SSE vs WebSockets; connection state as the scaling cost.
- `networking-heartbeats-idle-timeouts` Q: Why do long-lived connections need application-level ping/pong when TCP already has keepalive?
  A: A dead peer with no traffic is pure silence — indistinguishable from idle. TCP keepalive defaults to **2 hours**, is often disabled by middleboxes, and says not
- `networking-long-polling-costs` Q: What does a hanging long-poll request cost the server, and why do thread-per-request servers cap out first?
  A: Every waiting client holds an open connection and a parked request for up to the poll timeout (kept at ~30 s, under proxy idle limits). With thread-per-request 
- `networking-realtime-backpressure` Q: One WebSocket client on a bad network can't keep up with your push rate. What builds up where, and what are the three standard policies?
  A: The client's TCP receive window fills, the server's kernel send buffer fills, then the **per-connection application queue grows unbounded** — a handful of slow 
- `networking-realtime-transport-choice` Q: Long polling vs SSE vs WebSockets — give the one-line selection rule and a canonical example for each.
  A: Choose by **directionality and frequency**: - **Long polling**: rare updates, maximum compatibility, no infra changes — e.g. legacy notification checks. - **SSE
- `networking-sse-mechanics` Q: Two built-in SSE features that you'd otherwise hand-build on raw WebSockets?
  A: - **Automatic reconnection with resume**: browsers reconnect on drop and send the last received event id in `Last-Event-ID`, so the server can replay what was m
- `networking-websocket-scaling-cost` Q: What makes a WebSocket fleet fundamentally harder to scale than a stateless HTTP fleet? Name the three concrete problems.
  A: **Connection state lives on a specific server.** - **Routing**: to push to user X you must find *which* server holds X's socket → needs a connection registry (e

## networking.cdn — CDN
Push vs pull CDNs, cache keys, and what belongs at the edge.
- `networking-cdn-cache-key` Q: Your CDN hit rate is mysteriously low for static assets. What cache-key mistakes cause this, and what's the fix?
  A: The cache key is (by default) the full URL plus any `Vary` headers — anything that varies fragments the cache: - **Irrelevant query params** (tracking params, r
- `networking-cdn-dynamic-acceleration` Q: Your API responses are fully personalized and uncacheable. What does routing them through a CDN still buy?
  A: - **Handshakes on a short path**: TCP/QUIC + TLS terminate at an edge ~10–20 ms away instead of 150 ms cross-continent — saving 1–2 RTTs where RTTs are cheap. -
- `networking-cdn-purge-vs-versioning` Q: Shipping a new asset build behind a CDN: purge/invalidate vs versioned URLs — compare, and what's the standard practice?
  A: - **Purge**: propagates across PoPs in seconds–minutes (eventual), is a per-URL operational step, and does nothing for copies already in *browser* caches. - **V
- `networking-cdn-stale-while-revalidate` Q: `Cache-Control: stale-while-revalidate` and `stale-if-error` — what does each authorize a CDN to do, and what do you buy?
  A: - **stale-while-revalidate=N**: for N seconds after TTL expiry, serve the stale copy *immediately* while refetching in the background — popular keys never make 
- `networking-cdn-what-belongs-at-edge` Q: Beyond static files, what can a modern CDN edge absorb — and what technique protects the origin even for cache misses?
  A: - **Cacheable dynamic responses**: API GETs with short TTLs (even 1–5 s absorbs a viral spike), personalized pages split so the shared shell caches. - **Termina
- `networking-push-vs-pull-cdn` Q: Push CDN vs pull CDN — how does each get content to the edge, and which fits (a) a video release dropping globally at midnight, (b) a long-tail image catalog?
  A: - **Pull** (the default): edge fetches from origin on first miss, then caches. Zero upload workflow; cost is a slow first request per edge and origin load on mi
