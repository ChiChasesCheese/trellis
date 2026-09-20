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
  "traffic.load-balancing": ["<id shown first>", "…"],
  "traffic.gateways": ["<id shown first>", "…"],
  "traffic.rate-limiting": ["<id shown first>", "…"]
}

## traffic.load-balancing — Load Balancers
L4 vs L7, balancing algorithms, health checks, and LB high availability itself.
- `traffic-bounded-load-consistent-hashing` Q: Consistent hashing at the LB gives cache affinity, but plain consistent hashing has a load problem. What is it, and how does bounded-load CH fix it?
  A: Random ring placement plus skewed key popularity means some backends receive far more than the mean — affinity and balance fight each other, and a hot key can b
- `traffic-http2-connection-pinning` Q: You put gRPC services behind an L4 load balancer; one backend runs hot while new instances sit idle. Why, and what are the fixes?
  A: L4 balances **connections**, and gRPC/HTTP-2 clients open one long-lived multiplexed connection — every request from a client pins to whichever backend won the 
- `traffic-l4-vs-l7` Q: L4 vs L7 load balancer — what does each see, and when is L4 the right choice despite L7's flexibility?
  A: - **L4** sees only IP+port: forwards TCP/UDP flows, no payload inspection. Extremely fast, millions of connections, protocol-agnostic. - **L7** terminates the c
- `traffic-lb-algorithm-choice` Q: Round robin vs least-connections vs consistent hashing — match each to the workload it exists for.
  A: - **Round robin** (weighted): requests are cheap and uniform, backends identical — the simple default. - **Least connections** (or least outstanding requests): 
- `traffic-lb-health-and-ha` Q: The load balancer is itself a single point of failure. How is the LB tier made highly available, and what health-check subtlety prevents it from making outages worse?
  A: HA: **redundant LB pairs sharing a virtual IP** (VRRP/keepalived failover), or **anycast/ECMP** spreading one IP across an LB fleet; DNS with multiple records a
- `traffic-request-hedging` Q: Request hedging: mechanism, the cost math that makes it cheap, and its prerequisites?
  A: If no reply arrives within roughly the **p95 latency**, send the same request to a second replica; take whichever answers first and cancel the other. The user's

## traffic.gateways — Reverse Proxies & API Gateways
What a gateway centralizes — TLS termination, auth, routing, quotas — and the single-point risks it adds.
- `traffic-bff-pattern` Q: Backend-for-Frontend: what failure of the single shared API gateway does it address, and at what cost?
  A: A single gateway serving web, mobile, and partners accretes conflicting per-client logic — payload shaping, aggregation, feature quirks — owned by no one (the g
- `traffic-gateway-buffering` Q: Reverse-proxy request/response buffering — what does it protect upstream from, and when must you turn it off?
  A: The proxy absorbs a slow client's upload fully, then forwards to the upstream at LAN speed; responses likewise: upstream hands off the full response in millisec
- `traffic-gateway-centralizes` Q: An API gateway sits in front of 30 microservices. Which cross-cutting concerns does it centralize that would otherwise be reimplemented 30 times?
  A: - **TLS termination** — one place holding certs. - **Authentication** — validate the JWT/session once, forward trusted identity headers; services skip auth logi
- `traffic-gateway-risks` Q: What risks does putting an API gateway in front of everything create, and how is each mitigated?
  A: - **Single point of failure**: gateway down = whole product down → run it as a **stateless horizontally-scaled fleet** behind an L4 LB; config from a replicated
- `traffic-reverse-proxy-vs-gateway` Q: Reverse proxy vs API gateway — same box or different? Draw the line.
  A: Same mechanical position (server-side intermediary terminating client requests), different altitude: - **Reverse proxy** (nginx, Envoy) is the *mechanism*: forw
- `traffic-timeout-budget-propagation` Q: The gateway times out at 10 s, but a service it calls uses a 15 s timeout on its own downstream call. What goes wrong, and what discipline fixes it?
  A: After 10 s the gateway returns 504 and the client may retry — while the abandoned request **keeps computing downstream** for 5 more seconds. Under overload this

## traffic.rate-limiting — Rate Limiting
Token bucket vs sliding window, local vs distributed enforcement, and what to return when you shed.
- `traffic-critical-capacity-reservation` Q: When an API fleet saturates, dropping low-priority traffic first is the obvious move. How does *reserving capacity* for critical requests (Stripe-style fleet-usage shedding) differ from reactive priority shedding, and why keep the reservation even when the fleet is healthy?
  A: - **Reactive priority shedding** waits for distress signals (queue depth, latency, CPU) and then drops the least important traffic first. It works, but it engag
- `traffic-distributed-rate-limiting` Q: Rate limit is 1,000 req/s per API key, enforced across 20 gateway instances. Compare the two enforcement designs and their failure trade-off.
  A: - **Centralized counters** (Redis, atomic Lua/INCR): exact global limit, but adds a network hop per request and the store becomes a hot dependency — decide **fa
- `traffic-rate-limit-key-choice` Q: What key do you rate limit on — and what goes wrong with per-IP limits?
  A: Primary: the **authenticated principal** (API key / user id) — the unit quotas and billing are written against. Per-IP is the fallback for unauthenticated endpo
- `traffic-rate-limiting-vs-load-shedding` Q: Rate limiting vs load shedding — different triggers, different fairness. Draw the distinction and say why you need both.
  A: - **Rate limiting**: a *per-client contract* (quota), enforced even at 10% utilization — protects tenants from each other and makes cost predictable. - **Load s
- `traffic-rate-vs-concurrency-limiter` Q: An API gateway runs both a request-rate limiter and a concurrency limiter (Stripe runs both). What does each one cap, and which failure mode does each protect against?
  A: - **Rate limiter** caps **requests per second** per key. Protects against *too many requests*: bursts, runaway retry loops, abusive scripts — volume problems, e
- `traffic-shedding-response` Q: When a rate limiter rejects a request, what exactly should the response contain — and why does the wrong response amplify load?
  A: - **HTTP 429 Too Many Requests** (or 503 for server-wide shedding) — a distinct code so clients and dashboards can tell throttling from errors. - **`Retry-After
- `traffic-sliding-window-counter` Q: The sliding-window **counter** (the production approximation, e.g. Cloudflare): keep one counter for the current fixed window and one for the previous; estimated rate = {{c1::current count + previous count × the fraction of the sliding window overlapping the previous window}}. Memory is {{c2::O(1) per key — two counters}}, versus a sliding **log** storing every request timestamp; the price is assuming requests were {{c3::evenly distributed across the previous window}}, so the boundary-burst error is small and bounded.
- `traffic-token-bucket-vs-sliding-window` Q: Token bucket vs sliding window for rate limiting — what does each guarantee, and which allows bursts?
  A: - **Token bucket**: tokens refill at rate r, bucket holds up to b; a request spends a token. **Allows bursts up to b** while capping the long-run average at r —
