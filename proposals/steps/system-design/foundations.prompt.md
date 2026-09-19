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
  "foundations.method": ["<id shown first>", "…"],
  "foundations.estimation": ["<id shown first>", "…"],
  "foundations.numbers": ["<id shown first>", "…"],
  …
}

## foundations.method — Interview Method
Requirements clarification, scoping functional vs non-functional needs, driving the 40-minute structure yourself.
- `foundations-clarifying-questions-worth-asking` Q: Interviewer says "design X" with no details. Which clarifying questions actually change the design (vs filler)?
  A: Questions whose answers select an architecture: - **Read/write ratio** — decides caching and replication strategy. - **Scale** (DAU, data size) — one box vs sha
- `foundations-driving-the-40-minutes` Q: Rough time structure for a 40-minute design interview you are expected to drive yourself?
  A: - **~5 min** requirements + scope agreement - **~5 min** back-of-envelope estimates + API sketch - **~10–15 min** high-level architecture end to end - **~10–15 
- `foundations-interview-opening-moves` Q: First five minutes of a system design interview: what two categories of requirements do you pin down, and what form should each take?
  A: - **Functional**: the 3–5 core use cases you will actually design for — explicitly scope out the rest ("I'll focus on posting and the feed; skip search"). - **N
- `foundations-latency-requirement-precision` Q: "It should be fast" — turn that into an engineering requirement. What elements make a response-time requirement precise enough to design against?
  A: - **Metric**: response time **measured at the client** (includes queueing + network), not server service time. - **Percentiles**: a median *and* a tail target (
- `foundations-load-parameters` Q: "Scalable" is meaningless until you describe load. What are load parameters, and how do you pick the right one — e.g. for Twitter's home timeline?
  A: Load parameters are the numbers that describe demand on *your* architecture: QPS per operation, read/write ratio, concurrent connections, cache hit rate, workin
- `foundations-maintainability-design-input` Q: DDIA's three maintainability goals — name them, and where does each show up in a design interview answer?
  A: - **Operability** — make life easy for ops: metrics, runbooks, sane defaults, no manual toil. Show it: say how you deploy, monitor, and migrate the thing you ju

## foundations.estimation — Back-of-Envelope Estimation
QPS, storage, and bandwidth sizing from DAU and access patterns; when an estimate changes the design.
- `foundations-dau-to-qps` Q: Estimation shortcuts: a day is {{c1::~86,400 ≈ 10⁵ seconds}}, so average QPS ≈ {{c2::daily requests ÷ 10⁵}} (e.g. 100M requests/day ≈ 1,000 QPS), and peak QPS is typically {{c3::2–5× average}}.
- `foundations-fanout-estimation` Q: Twitter-style home timelines: ~5k tweets/s written, ~300k timeline reads/s, avg 75 followers. Walk the fan-out-on-write math and the estimate that breaks it.
  A: Fan-out on write: 5k tweets/s × 75 followers ≈ **375k timeline-cache inserts/s** — heavy but feasible, and it makes the dominant operation (reads) a cheap preco
- `foundations-littles-law` Q: Little's Law: average requests in flight = {{c1::arrival rate × average time in system (L = λ·W)}}. So 2,000 QPS at 50 ms mean response time means {{c2::100}} concurrent requests — the number that sizes worker pools, DB connection pools, and per-server concurrency limits. Corollary: when latency doubles under load, required concurrency {{c3::doubles too}}, which is how slowdowns exhaust pools and cascade.
- `foundations-storage-estimate-method` Q: Estimate storage for 100M-DAU Twitter-like service, 2 tweets/user/day, ~1 KB/tweet (skip media), 5-year retention. Walk the math.
  A: - Writes/day: 100M × 2 = **2 × 10⁸ tweets/day** - Data/day: 2 × 10⁸ × 1 KB = **200 GB/day** - 5 years ≈ 2,000 days → **~400 TB** raw; ×3 replication → **~1.2 PB
- `foundations-when-estimates-change-design` Q: Give three estimate outcomes that each flip a design decision (the whole point of doing the math).
  A: - **Working set fits in RAM** (≲ a few hundred GB) → cache or serve it all from memory; no need to optimize disk paths. - **Write QPS exceeds a single node** (~

## foundations.numbers — Latency Numbers
Orders of magnitude every engineer should know — memory vs SSD vs disk vs same-DC network vs cross-region.
- `foundations-coordinated-omission` Q: Your load-test harness sends a request, waits for the response, then sends the next. Name the measurement error and the fix.
  A: **Coordinated omission**: by waiting, the harness backs off *exactly when the system is slow*, so queueing delay vanishes from the data — you measured service t
- `foundations-latency-memory-ssd-disk` Q: Storage tier latencies, order of magnitude: main-memory reference {{c1::~100 ns}}, SSD random read {{c2::~100 µs}}, spinning-disk seek {{c3::~10 ms}} — each tier roughly **1,000× slower** than the one above.
- `foundations-latency-network-rtts` Q: Network round trips: same datacenter {{c1::~0.5 ms}}, same continent / cross-region {{c2::~10–70 ms}}, intercontinental (e.g. US ↔ Europe or Asia) {{c3::~100–150 ms}} — cross-region RTT is the number that makes synchronous geo-replication expensive.
- `foundations-latency-numbers-in-arguments` Q: A p99 budget is 200 ms and each service hop costs ~0.5 ms of same-DC RTT plus its own work. What design smell do the latency numbers expose in a 10-microservice synchronous call chain?
  A: Network RTT itself is cheap (~5 ms for 10 hops) — the real costs are **per-hop p99 amplification** (the slowest of many hops dominates; tail latencies compound)
- `foundations-latency-sequential-reads` Q: Reading 1 MB sequentially: from memory {{c1::~10–50 µs}}, from SSD {{c2::~200 µs–1 ms}} — sequential I/O is close enough to memory speed that {{c3::append-only / log-structured}} designs deliberately trade random writes for sequential ones.
- `foundations-p999-cost` Q: Why does each further latency nine (p99 → p999) cost disproportionately more to fix — and when is p999 still worth paying for?
  A: The extreme tail is dominated by effectively **random events** — GC pauses, page faults, TCP retransmits, context switches, background compactions — not your co
- `foundations-tail-latency-amplification` Q: Tail latency amplification: a page fans out to 100 backend calls, each avoiding its slow path 99% of the time — the whole page avoids all slow paths with probability 0.99¹⁰⁰ ≈ {{c1::37%}}, so {{c2::~63%}} of user requests hit at least one p99-slow call. Fan-out turns a backend's {{c3::p99 into roughly the user-facing median}} — which is why high-fan-out services obsess over tails, not medians.

## foundations.tradeoffs — Core Trade-offs
Performance vs scalability, latency vs throughput, availability vs consistency — the axes every later choice moves along.
- `foundations-availability-vs-consistency-axis` Q: For each, pick availability-first or consistency-first and justify in one line: (a) shopping-cart adds, (b) inventory decrement at checkout, (c) social-feed reads.
  A: - **(a) Cart adds — availability**: losing a sale to an error page costs more than merging a cart later (conflicts resolvable). - **(b) Inventory at checkout — 
- `foundations-elastic-vs-manual-scaling` Q: Elastic (auto) scaling vs manually planned capacity — what does each buy, and when is manual the right answer?
  A: - **Elastic**: tracks unpredictable load and saves money at the trough — but reacts with lag (a sharp spike outruns instance boot), and feedback loops surprise 
- `foundations-latency-vs-throughput` Q: Batching writes raises throughput but hurts which metric, and why? Name the general trade-off.
  A: **Latency vs throughput.** Batching amortizes fixed per-request costs (syscalls, network frames, fsyncs) across many items — throughput up — but each item now w
- `foundations-performance-vs-scalability` Q: "The service is slow" — how do you tell a performance problem from a scalability problem, and why does the distinction matter?
  A: - **Performance problem**: slow for a *single* user even at low load — fix the code path (algorithms, queries, I/O). - **Scalability problem**: fast when idle, 
- `foundations-scale-up-vs-out` Q: When do you keep scaling *up* (bigger machine) instead of *out* (more machines), and what eventually forces the switch?
  A: Scale up while you can: no partitioning, no rebalancing, no distributed failure modes — and a single 2026 box goes further than people assume (TBs of RAM, milli
- `foundations-three-pillars` Q: DDIA judges every data system against three nonfunctional pillars. Name them, and give the operational test you would apply to a running system for each — the question that reveals whether the pillar actually holds.
  A: - **Reliability** — the system keeps doing the right thing when things go wrong: hardware faults, software bugs, human error. Test: *kill a node, ship a bad con
- `foundations-utilization-latency-knee` Q: A latency-sensitive service runs its servers at 60% CPU, and finance proposes 90% to cut cost. Why does response time — especially the tail — blow up long before utilization reaches 100%?
  A: Because of **queueing delay**: requests arrive randomly and burstily, so even below saturation, momentary bursts form queues, and the closer utilization ρ gets 
