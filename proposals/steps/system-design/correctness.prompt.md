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
  "correctness.idempotency": ["<id shown first>", "…"],
  "correctness.outbox": ["<id shown first>", "…"],
  "correctness.saga": ["<id shown first>", "…"],
  …
}

## correctness.idempotency — Idempotency
Idempotency keys, dedup windows, and designing every mutation to survive a retry.
- `correctness-dedup-window` Q: How long do you retain idempotency keys / dedup records, and what goes wrong at each extreme?
  A: Retention must **exceed the maximum retry horizon** of every client and queue in front of you — including delayed retries from DLQ redrives and mobile clients r
- `correctness-idempotency-concurrent-retries` Q: Two requests with the same idempotency key arrive concurrently (client timeout fired while the original was still running). What must the server do?
  A: - The key insert's **unique constraint** makes exactly one request the winner; the loser must NOT run the operation. - The loser either **waits** for the winner
- `correctness-idempotency-key-design` Q: Design the idempotency-key flow for a `POST /payments` endpoint (Stripe-style). Who generates the key, what does the server store, and what does a retry get back?
  A: - **Client generates** the key (UUID) *per operation intent* — one key per "charge this cart once", reused across all retries of that intent, never per HTTP att
- `correctness-idempotency-partial-failure` Q: A payment handler claims its idempotency key, calls the card processor, then crashes before recording the result. The key is stuck "in-progress". What must recovery do?
  A: The processor may or may not have charged — so neither blind retry nor blind fail is safe. - Attach a **lease/expiry** to the in-progress state; a stuck key pas
- `correctness-idempotency-payload-hash` Q: An idempotency-key record must also store a {{c1::hash of the request payload (and the endpoint/params)}}; a request reusing the key with a **different** body must be {{c2::rejected with an error (Stripe: 422), never replayed or re-executed}} — otherwise a client bug that reuses keys across distinct operations gets the *first* operation's stored response and silently believes the second one succeeded.
- `correctness-idempotency-response-replay` Q: On an idempotency-key hit, why must the server replay the **stored response** rather than re-execute the handler "since it's idempotent anyway"?
  A: Re-execution can **diverge** from the original run: prices, FX rates, fees, or risk rules may have changed; generated values (ids, timestamps) differ; and refer
- `correctness-idempotent-consumer-patterns` Q: Beyond an idempotency-key table, name three ways to make a mutation safe to apply twice — and the classic operation that is NOT naturally idempotent.
  A: - **Natural idempotency**: absolute writes — `SET status = 'shipped'`, upsert by primary key. Applying twice converges to the same state. - **Conditional write 

## correctness.outbox — Dual Writes & Outbox
Why writing DB-then-publish loses events, and how the transactional outbox closes the gap.
- `correctness-dual-write-problem` Q: A service commits to Postgres, then publishes an event to Kafka. Enumerate the failure modes of this "dual write" — and why wrapping both in try/catch doesn't fix it.
  A: - **Commit then crash before publish** → state changed, event lost; downstream never learns. (The common, silent one.) - **Publish then commit fails** → phantom
- `correctness-outbox-cleanup` Q: An outbox table in Postgres receives every event the system emits. What operational problem builds up, and how do you clean it without breaking the pattern?
  A: Published rows accumulate: table and index **bloat**, MVCC dead tuples from delete/update churn, vacuum pressure, and slowing relay polls. - **Delete-after-ack*
- `correctness-outbox-event-payload` Q: Fat events vs thin events in an outbox: what does each carry, and what race does the thin style cause?
  A: - **Fat (event-carried state)**: the outbox row snapshots all needed state *as of the transaction* (`OrderPlaced` + items, amounts, addresses). Consumers are se
- `correctness-outbox-mechanism` Q: Walk through the transactional outbox pattern: what happens in the transaction, how do events reach the broker, and what guarantee do you end up with?
  A: 1. In **one local transaction**: apply the state change AND insert the event row into an `outbox` table. Atomic — either both exist or neither. 2. A **relay** m
- `correctness-outbox-ordering-cloze` Q: To preserve event order through an outbox: the relay publishes rows in {{c1::commit/insert order (monotonic outbox sequence)}}, uses {{c2::the aggregate id (e.g. account id) as the broker partition key}} so one entity's events stay in one partition, and a polling relay must run {{c3::single-writer per partition/shard}} — parallel unordered pollers silently reorder events.
- `correctness-outbox-relay-lag` Q: The outbox relay dies for 2 hours. What is the failure mode for the system, and what do you monitor to catch it?
  A: Writes keep succeeding — the outbox insert is in the local transaction — so the system stays **available**; events are delayed, not lost, and downstream views g

## correctness.saga — Sagas
Long-running workflows via compensating actions when a distributed transaction is off the table.
- `correctness-saga-compensation-limits` Q: "On failure, just run the compensations." What three realities make saga compensation harder than a rollback?
  A: - **Compensation is semantic undo, not rollback**: a refund is a new transaction (fees, records, latency), and some actions are **non-compensatable** — you can'
- `correctness-saga-compensation-race` Q: A saga cancellation can race its own forward action: the "release seat" compensation arrives at a participant **before** the delayed "reserve seat" command. What happens, and what's the fix?
  A: Naively, the release is a no-op ("nothing reserved"), then the late reserve lands and **holds the seat forever** — the saga believes it rolled back, the partici
- `correctness-saga-isolation` Q: Sagas have ACD but no I. What anomalies does the missing isolation cause, and name the standard countermeasures.
  A: Each step commits locally, so **intermediate state is visible** before the saga's fate is known: - **Dirty read**: another flow sees "payment captured" and ship
- `correctness-saga-orchestration-choreography` Q: Orchestrated vs choreographed saga: how does each work, and when do you pick which?
  A: - **Choreography**: each service reacts to the previous service's events (order-created → payment listens → payment-charged → inventory listens). No central bra
- `correctness-saga-orchestrator-recovery` Q: The saga orchestrator crashes mid-workflow. What must have been persisted for safe resume, and how are the resulting duplicates and silences handled?
  A: The orchestrator is a **persistent state machine**: it durably records the saga instance + current step *before* dispatching each command (its own DB write + co
- `correctness-saga-vs-2pc` Q: Why do payment/order systems use sagas instead of distributed transactions (2PC) across services — and what do you give up?
  A: 2PC requires every participant to hold **locks while blocked on a coordinator** — across heterogeneous services (some of which are external APIs that simply don

## correctness.ledger — Ledgers & Reconciliation
Double-entry design, immutability, balance derivation, and reconciliation as the payments-grade safety net.
- `correctness-balance-derivation` Q: If balance = SUM(entries), how do you make balance reads fast AND enforce "no overdraft" under concurrent spends?
  A: - **Fast reads**: periodic **snapshots/checkpoints** — persist balance as of entry N; current balance = snapshot + entries since N. The snapshot is a cache, alw
- `correctness-double-entry-invariant` Q: Why do payment systems store money as double-entry ledger entries instead of a `balance` column, and what invariant does every transaction maintain?
  A: Every transaction posts **two or more entries that sum to zero** (each debit matched by credits) — money is never created or destroyed, only moved between accou
- `correctness-ledger-clearing-metric` Q: A double-entry ledger mirrors many independent payment systems (Stripe-style). Beyond running reconciliation jobs, what does it mean to make discrepancy detection a *first-class metric* — what does a "clearing" score measure, and why publish it as a number teams are held to?
  A: - Model each fund flow so that **intermediate ("clearing") accounts must return to zero at steady state** — money sitting in a pipe that should have drained is,
- `correctness-ledger-cutoff-settlement` Q: Why does a ledger need a business date and cutoff time distinct from event timestamps, and what happens to entries that arrive after cutoff?
  A: Reports, reconciliation, and settlement all run against a **closed accounting day**: "balance as of end of business date D" must be **frozen** — re-runnable for
- `correctness-ledger-hot-accounts` Q: A platform fee account appears in every transaction — millions of entries/day against one ledger account. Why does it melt down, and how do you design around it?
  A: If posting maintains a materialized balance row, every transaction serializes on that **one row lock** — the fee account becomes a global throughput ceiling. - 
- `correctness-ledger-immutability` Q: A posted ledger entry turns out to be wrong (wrong amount, wrong account). What does a payments-grade ledger do, and what is banned?
  A: **Banned**: `UPDATE` or `DELETE` on posted entries. The ledger is append-only; history that auditors and past reports saw must never change. Correct move: post 
- `correctness-ledger-multi-currency` Q: How does a double-entry ledger handle a customer paying EUR 100 for a USD 108 charge — what does "entries sum to zero" mean with two currencies?
  A: The zero-sum invariant holds **per currency, never across currencies** — summing EUR against USD is meaningless. An FX conversion is modeled as **two balanced l
- `correctness-ledger-three-way-recon` Q: Payments teams reconcile three-way — internal ledger vs processor report vs bank statement. What does each pairwise match catch that two-way misses, and how are breaks classified?
  A: - **Ledger ↔ processor**: did every charge/refund we recorded happen, at the right amount/state? Catches lost webhooks, timeout-ambiguity bugs. - **Processor ↔ 
- `correctness-reconciliation` Q: Your ledger has idempotency keys, an outbox, and zero-sum checks. Why do you still run reconciliation against the payment processor, and what does the job actually do?
  A: Because those patterns protect *your* writes — they can't see the **external world disagreeing**: charges that succeeded at the processor after you recorded a t
