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
  "architecture.services": ["<id shown first>", "…"],
  "architecture.discovery": ["<id shown first>", "…"],
  "architecture.serverless": ["<id shown first>", "…"]
}

## architecture.services — Monoliths & Microservices
When to split, service boundaries by data ownership, and the operational bill microservices arrive with.
- `architecture-boundaries-data-ownership` Q: What's the rule for drawing service boundaries, and why is a shared database between services considered the cardinal sin?
  A: Rule: a service **exclusively owns its data** — boundary drawn around a business capability (bounded context), and all access to that data goes through the serv
- `architecture-conways-law` Q: Conway's law says architecture copies org structure. How do mature orgs use it as a *design input* rather than a curse?
  A: **Inverse Conway maneuver**: since the system will mirror team communication paths anyway, design the *teams* to match the architecture you want — one long-live
- `architecture-distributed-monolith` Q: Name the symptoms that reveal a "microservices" system is actually a distributed monolith, and the one-question test.
  A: Symptoms: - Services must be **deployed together** or in a fixed order (lockstep releases, coordinated version matrices). - **Shared database** or shared intern
- `architecture-microservices-tax` Q: Name the operational bill that arrives with microservices — the things a monolith gave you for free.
  A: - **In-process call → network call**: latency, partial failure, timeouts/retries/circuit breakers on every edge; a deep call graph multiplies tail latency and f
- `architecture-sync-call-chains` Q: A request fans through a synchronous chain of 5 services. What does the chain do to availability and latency, and what are the three escapes?
  A: Every synchronous hop is a **serial hard dependency**: availabilities multiply (five 99.9% hops ≈ 99.5% — from 43 min to 3.6 h of monthly downtime, [[reliabilit
- `architecture-when-to-split` Q: What are legitimate triggers for splitting a monolith into services — and what is the default recommendation for a new system in 2026?
  A: Legitimate triggers (organizational and operational, not aesthetic): - **Team scaling**: deploy trains and merge conflicts across many teams; you split so teams

## architecture.discovery — Service Discovery & Contracts
Registries, health checking, API versioning, and evolving schemas without breaking consumers.
- `architecture-api-versioning-strategies` Q: URI versioning (/v2/) vs header versioning vs "no versions, additive-only": when is each the right API evolution strategy?
  A: - **Additive-only evolution** (no version bumps): the modern default — only compatible changes ([[architecture-schema-compat-rules]]), clients ignore unknown fi
- `architecture-discovery-mechanisms` Q: Client-side vs server-side service discovery: how does each find healthy instances, and which does Kubernetes give you?
  A: - **Client-side**: caller queries a registry (Consul, Eureka) and load-balances across instances itself. Fewer hops and smart per-request balancing, but discove
- `architecture-expand-contract` Q: You need a breaking API change (rename a field, change semantics) with consumers you don't control deploying on their own schedule. What's the migration pattern?
  A: **Expand and contract** (parallel change): 1. **Expand**: serve both old and new shapes (add the new field/endpoint/version alongside the old; dual-write or tra
- `architecture-registry-compat-modes` Q: A schema registry's compatibility mode dictates **deploy order**: BACKWARD (new schema can read old data) means upgrade {{c1::consumers first}}, then producers; FORWARD (old schema can read new data) means upgrade {{c2::producers first}}; FULL allows {{c3::either order}}. Kafka-style event streams default to BACKWARD because consumers must be able to reprocess {{c4::old events retained in the log}} — the registry rejects an incompatible schema at publish/CI time, before it can strand data. See [[architecture-schema-compat-rules]].
- `architecture-schema-compat-rules` Q: You must evolve an event/API schema while old consumers and old producers are still live. Which changes are safe, and which direction of compatibility do you need?
  A: Safe (compatible) changes: **add optional fields with defaults**; never remove, rename, retype, or reuse a field/tag number — deprecate and leave it. - **Backwa

## architecture.serverless — Serverless
FaaS execution model, cold starts, and where per-request pricing beats owning servers.
- `architecture-cold-starts` Q: What actually happens during a FaaS cold start, roughly how expensive is it, and what are the mitigations?
  A: On a request with no warm instance, the platform must **provision a sandbox (microVM/container), load the runtime, load your code, and run init** before handlin
- `architecture-serverless-backpressure` Q: A traffic spike makes your FaaS platform spawn 3,000 concurrent function instances, which flatten the database behind them. What is the structural mismatch, and the two standard fixes?
  A: FaaS **scales concurrency near-instantly and unboundedly**, while downstream stateful systems (relational DBs, third-party APIs) have hard concurrency/connectio
- `architecture-serverless-constraints` Q: Name the FaaS execution-model constraints that break naive designs — and the classic database mistake.
  A: - **Ephemeral, stateless instances**: no local state between invocations (disk/memory may or may not survive); anything durable goes to external stores. - **Exe
- `architecture-serverless-economics` Q: When does per-request (FaaS) pricing beat owning servers, and when does it flip?
  A: FaaS wins when utilization is **low or spiky**: you pay only for execution time, and idle costs zero — cron jobs, webhooks, rare admin endpoints, unpredictable 
- `architecture-serverless-orchestration` Q: A workflow (order → charge → fulfill → notify) takes hours and must survive crashes, but FaaS functions cap at ~15 minutes and keep no state. What's the pattern?
  A: **Durable workflow orchestration** (Step Functions, Temporal, Durable Functions): the workflow's *state machine* lives in the orchestrator's durable store, and 
