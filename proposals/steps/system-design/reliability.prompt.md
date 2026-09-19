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
  "reliability.availability": ["<id shown first>", "…"],
  "reliability.resilience.retries": ["<id shown first>", "…"],
  "reliability.resilience.containment": ["<id shown first>", "…"],
  …
}

## reliability.availability — Availability Math
Nines, serial vs parallel composition, redundancy patterns, failover modes and their data-loss windows.
- `reliability-correlated-failures` Q: Two replicas at 99.9% "should" give six nines in parallel. Why do real systems get far less, and what restores some of the promised benefit?
  A: The parallel formula assumes **independent** failures; real faults are correlated: - **Shared fate**: same rack/AZ/power, same load balancer, same cloud control
- `reliability-failover-modes-tradeoff` Q: Rank hot, warm, and cold standby failover by recovery speed, and name the hidden risk hot standby adds.
  A: - **Hot (active-active or synced active-passive)**: seconds — standby already serves or has current state. Costs ~2x and risks **split-brain**: both nodes belie
- `reliability-fault-vs-failure` Q: Fault vs failure (DDIA framing): what is the difference, and what does that make "fault tolerance" mean in practice?
  A: - **Fault**: one component deviates from spec (a disk dies, a node returns garbage, a network link drops packets). - **Failure**: the *system as a whole* stops 
- `reliability-gray-failure` Q: A node passes every health check but serves 100x slower due to a dying disk. What is this failure class, why is it worse than a crash, and what detects it?
  A: **Gray (partial) failure** — the component is degraded, not dead, and the health checker's view differs from the clients' view (*differential observability*). W
- `reliability-nines-downtime-budgets` Q: Downtime allowed per month: 99.9% ("three nines") ≈ {{c1::43 minutes}}, 99.99% ≈ {{c2::4.4 minutes}}, 99.999% ≈ {{c3::26 seconds}} — each extra nine cuts the budget by 10x and typically requires automated (not human-in-the-loop) failover.
- `reliability-serial-parallel-composition` Q: Components in **series** multiply availabilities: two 99.9% dependencies give {{c1::0.999 × 0.999 ≈ 99.8%}} — every hard dependency subtracts nines. Components in **parallel** (either can serve) give 1 − (1−A)², so two 99.9% replicas yield {{c2::99.9999%}} — assuming truly independent failure modes.

## reliability.resilience.retries — Timeouts & Retries
Timeout budgets, deadline propagation, exponential backoff with jitter, retry storms and retry budgets.
- `reliability-deadline-propagation` Q: Service A (1s timeout) calls B, which calls C. C responds in 2s. What goes wrong with naive per-hop timeouts, and what is the fix?
  A: B and C keep doing work for a caller that has **already given up** — wasted capacity, and A may have retried, doubling load. Worse, if inner timeouts are longer
- `reliability-retry-storm` Q: A service slows down, clients retry, and the service dies completely. Name the failure mode and three design rules that prevent it.
  A: **Retry storm** — retries multiply offered load exactly when capacity is lowest (3 layers each retrying 3x = 27x amplification). - **Exponential backoff with ji
- `reliability-retryable-errors` Q: Classify which failures are worth retrying and which are not — and explain why a *timeout* is the hardest case.
  A: - **Retry**: connection refused / reset / DNS failure *before* the request was sent (nothing executed), `503`, `429` (obey `Retry-After`), gRPC `UNAVAILABLE` / 
- `reliability-server-driven-backoff` Q: Every client is individually well-behaved (exponential backoff + jitter, 3 attempts) and the service is still being retried into the ground. Why, and what two mechanisms fix it?
  A: Client-side backoff is **local knowledge**: each client only sees its own failures, so it cannot know that 10k other clients are backing off against the same ov
- `reliability-timeout-budget-arithmetic` Q: Gateway → A → B → C, each hop with a 1s timeout and 3 attempts, under a 3s user-facing budget. Do the arithmetic and give the configuration rules.
  A: Retries **multiply down the stack**: C can take 3×1s = 3s; B wraps that in 3 attempts → 9s; A → 27s. The user's 3s budget is blown 9× over, and the extra attemp

## reliability.resilience.containment — Failure Containment
Circuit breakers, bulkheads, load shedding, chaos engineering, and safe deployment strategies.
- `reliability-avoid-fallback` Q: Why do fallback paths ("if the primary fails, switch to the backup logic") tend to fail exactly when they are needed, and what do teams like Amazon's do instead of writing them?
  A: Fallback code fails when needed because of three compounding properties: - **Untested**: it runs so rarely that it bit-rots; the first real execution is during 
- `reliability-bulkhead-vs-shedding` Q: Bulkheads vs load shedding — which failure does each contain, and when do you need both?
  A: - **Bulkheads** partition resources (connection pools, thread pools, instances) per dependency or tenant, so one slow dependency exhausts only its own pool — co
- `reliability-chaos-hypothesis` Q: What separates chaos engineering from "randomly breaking things in prod," and what are the steps of a proper experiment?
  A: Chaos engineering is **hypothesis testing** about resilience, not vandalism: 1. Define a **steady-state metric** (e.g. checkout success rate). 2. State the hypo
- `reliability-circuit-breaker-states` Q: What problem does a circuit breaker solve that per-request timeouts and retries do not, and how do its three states work?
  A: Timeouts protect one call; a breaker protects the **caller's capacity** — when a dependency is down, threads/connections stop being wasted on calls that are doo
- `reliability-config-deploy-risk` Q: Why are config/flag changes the riskiest deploy class — behind many of the largest real outages — and what discipline fixes it?
  A: Config changes bypass everything that makes code deploys safe: they often propagate **globally and near-instantly** (no canary, no batches), skip CI/tests, feel
- `reliability-constant-work` Q: The constant-work pattern says a reliable system should do the *same amount of work* whether everything is calm or everything is failing — e.g. Route 53 pushes the full health-check result file every few seconds instead of sending deltas on change. What does this buy?
  A: - **Failure mode = normal mode.** A delta-based system does almost nothing when calm and a flood of work when many things change at once — so its busiest, least
- `reliability-deploy-strategies` Q: Blue-green vs canary vs rolling deployment: what does each optimize for, and which one actually validates a release?
  A: - **Rolling**: replace instances in batches. Cheap (no spare fleet), but old and new run mixed for a while and rollback means rolling again — slowest to undo. -
- `reliability-shuffle-sharding-blast-radius` Q: Blast-radius math for 8 nodes: with plain sharding into 4 fixed shards of 2, one poison-pill client fully takes out {{c1::1/4 (25%)}} of customers. With shuffle sharding (each customer a random 2-node subset) there are {{c2::C(8,2) = 28}} possible virtual shards, so the fraction of customers who share *both* nodes with the bad client — the only ones fully down — is about {{c3::1/28 (≈3.6%)}}; customers sharing one node stay up by retrying on their other node. Scaling nodes grows combinations {{c4::combinatorially (e.g. 100 choose 5 ≈ 75 million)}}, so per-customer isolation approaches single-tenant on shared hardware.
- `reliability-shuffle-sharding-mechanism` Q: What is shuffle sharding, and why does giving each customer a random 2-node subset of an 8-node fleet contain a poison-pill client far better than splitting the fleet into fixed shards?
  A: - **Plain sharding**: split 8 nodes into 4 fixed shards of 2 and pin each customer to one shard. A **poison-pill client** (a request that crashes or saturates w

## reliability.slo — SLOs & Error Budgets
SLIs worth measuring, percentiles over averages, and error budgets as a release throttle.
- `reliability-burn-rate-alerting` Q: Why alert on error-budget burn rate instead of a raw error-rate threshold, and how do multi-window burn alerts work?
  A: A fixed threshold either pages on blips (too sensitive) or sleeps through slow leaks (too dull). **Burn rate** = how many times faster than sustainable you are 
- `reliability-error-budget-throttle` Q: Your SLO is 99.9% monthly success rate. What is the error budget, and what concretely changes when it is exhausted?
  A: Budget = 1 − SLO = **0.1% of requests** (or ~43 minutes of full downtime) per month, deliberately spendable on releases, experiments, and planned risk. When exh
- `reliability-latency-sli-form` Q: Why do SRE teams define a latency SLI as "% of requests faster than 300ms" instead of "p99 < 300ms"?
  A: The threshold form turns latency into a **good-event / total-event ratio**, which: - Plugs directly into **error-budget math** — each slow request spends budget
- `reliability-percentiles-over-averages` Q: Why is p99 latency the SLI to watch instead of the mean — and why does fan-out make tail latency worse than it looks?
  A: Latency is heavily right-skewed: a healthy mean can hide a p99 of seconds, and the slowest requests often belong to your **heaviest users** (biggest carts, most
- `reliability-slo-dependency-ceiling` Q: A service's achievable SLO is capped by its **hard dependencies**: if you call a 99.9% service synchronously on every request, you cannot credibly promise more than {{c1::~99.9% (minus your own failures — hard dependencies multiply in)}}. To offer a *higher* SLO than a dependency you must {{c2::take it off the critical path — cache its data, degrade gracefully without it, or make the call async}}. Rule of thumb: your critical dependencies should each be about one nine *more* reliable than the SLO you sell.
- `reliability-symptom-vs-cause-alerts` Q: "Page on symptoms, ticket on causes" — what does that mean, and why does cause-based paging (CPU > 90%, disk 80% full) rot an on-call rotation?
  A: - **Symptom alerts** fire on what users experience — the SLIs behind your SLO (error rate, latency). Every page then means real or imminent user impact and maps

## reliability.observability — Observability
Structured logs, metrics, distributed traces; correlation ids and cardinality costs.
- `reliability-canonical-log-lines` Q: What is a canonical log line (Stripe's pattern), and why does one wide structured line per request beat many scattered log lines when you are debugging production?
  A: - **The pattern**: at the end of every request, emit **one structured log line carrying every fact about that request** — request id, authenticated user/merchan
- `reliability-exemplars` Q: You see a p99 latency spike on a dashboard and now need one concrete slow request to debug. What feature jumps you straight from the metric to a trace, and how does it work?
  A: **Exemplars**: when recording a latency observation into a histogram bucket, the metrics SDK attaches the current **trace ID** (a sampled reference request) to 
- `reliability-logs-metrics-traces` Q: Logs, metrics, traces: which one answers "is it broken?", "where is it broken?", and "why is this request broken?" — and what does each cost at scale?
  A: - **Metrics** → "is it broken?": pre-aggregated time series; cheap to store and alert on, but you can only ask questions you pre-declared. - **Traces** → "where
- `reliability-metric-cardinality` Q: An engineer adds `user_id` as a label on a request-latency metric. Why does this melt the metrics system, and where does that data belong instead?
  A: Time-series stores keep **one series per unique label combination**. An unbounded label (user id, request id, URL with ids) multiplies cardinality into millions
- `reliability-percentile-aggregation` Q: Each of 50 hosts reports its own p99 latency. Why can't you average (or max) them to get the service p99, and what should hosts export instead?
  A: **Percentiles don't compose** — a percentile is a point on a distribution, and you can't reconstruct the merged distribution from per-host points. Averaging p99
- `reliability-red-vs-use` Q: RED method vs USE method: what does each one measure, and which do you apply to a payment service vs a database host?
  A: - **RED** — for every *request-driven service*: **R**ate (req/s), **E**rrors (failed req/s), **D**uration (latency distribution). This is the user's view; the p
- `reliability-trace-sampling` Q: Head-based vs tail-based trace sampling — what does each decide on, and which one keeps the traces you actually want during an incident?
  A: - **Head-based**: sample decision made at the first hop (e.g. keep 1%), propagated via the trace context so all spans of a kept trace survive. Cheap and simple 

## reliability.multi-region — Multi-Region
Active-passive vs active-active, data residency, RPO/RTO, and why failover you never test doesn't exist.
- `reliability-active-active-vs-passive` Q: When is active-passive the right multi-region design over active-active, given that active-active looks strictly better on paper?
  A: Choose **active-passive** when writes must stay strongly consistent and single-homed: one region owns all writes, so there are no cross-region write conflicts a
- `reliability-async-rpo-math` Q: With async cross-region replication, your effective **RPO equals the replication lag at the moment of disaster**, and writes lost ≈ {{c1::lag × write throughput}} — e.g. 5s of lag at 2,000 writes/s ≈ 10,000 lost writes. Lag is worst exactly when you need it least: {{c2::during traffic spikes and incidents, when the replication channel falls behind}} — so monitor lag as an SLI and alert when it exceeds the RPO objective. True RPO = 0 requires synchronous quorum replication and its cross-region write latency ([[reliability-three-region-quorum]]).
- `reliability-data-residency-conflict` Q: Data residency law says EU user data stays in the EU, but your DR plan fails everything over to us-east. How do these conflict, and what architecture resolves it?
  A: Residency caps where data may be **replicated** — you cannot fail EU data over to a US region, so a global active-passive design is illegal for that data, and r
- `reliability-rpo-vs-rto` Q: RPO vs RTO: which one is about data, which about time-to-recover, and which replication choice controls each?
  A: - **RPO (Recovery Point Objective)**: max acceptable **data loss**, measured backward from the failure. Controlled by replication mode — synchronous replication
- `reliability-three-region-quorum` Q: Why does surviving a full region loss with zero data loss require three regions, not two — and what is the cheap third-region trick?
  A: Synchronous consensus/quorum replication needs a **majority**. With 2 regions, any split or region loss leaves at most half the replicas — no majority, so you e
- `reliability-untested-failover` Q: Why does an untested regional failover "not exist," and what two practices make failover real?
  A: Failover paths rot silently: the standby region drifts (missing config, stale capacity quotas, expired secrets, un-replicated new dependencies), and the first e
