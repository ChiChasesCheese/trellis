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
  "distributed.cap": ["<id shown first>", "…"],
  "distributed.consistency": ["<id shown first>", "…"],
  "distributed.replication.leader": ["<id shown first>", "…"],
  …
}

## distributed.cap — CAP & PACELC
What the theorem actually constrains during a partition, and the latency trade-off the rest of the time.
- `distributed-cap-per-operation` Q: Why is "is this system CP or AP?" the wrong granularity — and what is the right one? Give two real examples.
  A: The C/A trade is made **per operation**, not per system — the same store can serve some requests linearizably and others stale. - **Cassandra/DynamoDB**: consis
- `distributed-cap-proof-sketch` Q: CAP proof sketch: partition two replicas, write `x=1` on one side, read `x` on the other. If the read side answers without hearing from the writer's side it may return {{c1::stale data — violating linearizability (sacrifices C)}}; if it waits or refuses until the partition heals it is {{c2::unavailable for that request (sacrifices A)}}. There is no third option, because the only way to know about the write is {{c3::a message across the very link that is down}}.
- `distributed-cap-real-claim` Q: What does the CAP theorem actually constrain — and why is calling a system "CA" a red flag in an interview?
  A: It constrains behavior **only during a network partition**: a replicated system must then either refuse some requests (choose **C**, staying linearizable) or an
- `distributed-cp-partition-behavior` Q: A 5-node CP system (e.g. etcd/ZooKeeper) is partitioned 2 | 3. What can each side do, and what would break if the minority side kept serving?
  A: - **Majority side (3)**: elects/keeps a leader and serves both reads and writes — it can still reach quorum. - **Minority side (2)**: cannot commit writes, and 
- `distributed-pacelc` Q: What does PACELC add over CAP, and how do DynamoDB and Spanner classify under it?
  A: The **ELC part**: *Else* (no partition, i.e. almost always), you still trade **Latency vs Consistency** — strong consistency requires coordination (quorum/leade

## distributed.consistency — Consistency Models
Linearizability, causal, read-your-writes, eventual — as contracts you promise the client.
- `distributed-causal-in-practice` Q: Causal consistency is theoretically the sweet spot — the strongest model that stays available under partition — yet almost no mainstream database offers it as a mode. Why not, and what do production systems use to get "causal enough" behavior?
  A: Why it's rare: - **Tracking causality is expensive**: the system must know, for every write, which prior reads/writes it depends on — version vectors or depende
- `distributed-causal-vs-eventual` Q: Under plain eventual consistency, a user sees the reply "No it isn't" before the question it answers. What guarantee prevents this, and what does it deliberately not order?
  A: **Causal consistency**: if write B was made after seeing write A (same session, or read-then-write), every node must apply/expose A before B. Implemented with v
- `distributed-consistency-ladder` Q: The consistency ladder, strongest to weakest, and what each rung gives up: **linearizability** promises {{c1::every operation sees the effects of all operations completed before it in real time — one up-to-date copy}}, and is the only rung that {{c2::cannot stay available during a network partition (must stall or refuse)}}. One step down, **causal consistency** keeps {{c3::the order of operations that depend on each other (read-then-write, same session chains), while letting concurrent operations be seen in different orders on different nodes}}. Below it, **session guarantees** (read-your-writes, monotonic reads) protect {{c4::only one client's view of its own interactions, promising nothing across clients}}. The bottom rung, **eventual consistency**, promises only {{c5::convergence at some unspecified time — no recency bound, and reads may go backwards meanwhile}}.
- `distributed-linearizability-composability` Q: Linearizability is a {{c1::composable ("local") property — if each object is linearizable, the system of all objects is linearizable}}, and it concerns {{c2::single operations on single objects, ordered against real time}}. Serializability is {{c3::not composable — running transactions serializably on two separate databases does not make cross-database executions serializable}}, which is one reason splitting a transactional workload across stores silently weakens its guarantees.
- `distributed-linearizability-vs-serializability` Q: Linearizability vs serializability — what does each guarantee, over what unit, and what do you call their combination?
  A: - **Linearizability**: a *single-object, real-time* guarantee — every read/write appears to take effect atomically at some instant between its start and end, so
- `distributed-linearizability-when-needed` Q: Which concrete features genuinely require linearizability (not just causal or session guarantees), and why?
  A: Anything where **two nodes agreeing on one current value** is the point: - **Locks and leader election**: all nodes must agree who holds the lock — a stale view
- `distributed-quorum-not-linearizable` Q: Dynamo-style store, N=3, W=2, R=2 — strict quorums, no sloppiness. Why are reads still not linearizable?
  A: A write lands on replicas **one at a time**, and reads can interleave with the partial write: reader 1's quorum includes an updated replica and returns the new 
- `distributed-read-your-writes` Q: A user saves their profile, refreshes, and sees the old version (read hit a lagging replica). Name the missing guarantee and three ways to provide it without making all reads strong.
  A: **Read-your-writes (read-after-write) consistency** — a session-level guarantee, weaker than linearizability. - **Route the writer's reads to the leader** for d

## distributed.replication.leader — Leader-Based
Single-leader replication, log shipping formats, sync vs async, lag and its anomalies, failover mechanics.
- `distributed-failover-mechanics` Q: Walk through automatic leader failover in leader-follower replication, and name the three classic hazards.
  A: Steps: **detect** leader death (heartbeat timeout), **elect** the most up-to-date follower as new leader, **reconfigure** so clients and followers point at it. 
- `distributed-lag-anomalies` Q: Name the two classic read anomalies replication lag causes besides missing your own writes, and the guarantee that fixes each.
  A: - **Going backwards in time**: successive reads hit differently-lagged replicas, so data you already saw disappears. Fix: **monotonic reads** — pin a session to
- `distributed-new-follower-setup` Q: You need to add a new follower to a busy single-leader database without stopping writes. Copying the data files while the leader keeps writing yields a torn, inconsistent copy — what is the standard procedure, and what does it demand from the leader's log?
  A: - **Snapshot at a known log position**: take a consistent snapshot of the leader that is tagged with an exact position in the replication log (Postgres LSN, MyS
- `distributed-replication-log-formats` Q: Statement-based vs WAL shipping vs logical (row-based) replication — what breaks or binds with each, and which do modern systems default to?
  A: - **Statement-based** (ship the SQL): breaks on nondeterminism — `NOW()`, `RAND()`, auto-increments, triggers, concurrent-execution order. Requires rewriting st
- `distributed-semi-sync-fallback` Q: Your team runs semi-synchronous replication (the leader waits for one follower's ack before acknowledging a commit) and advertises "zero data loss on failover". Name the ways that promise silently fails in practice.
  A: - **Silent degradation to async**: implementations keep availability when the sync follower stops responding — e.g. MySQL semi-sync commits anyway after a timeo
- `distributed-sync-vs-async-replication` Q: Leader-follower: synchronous vs asynchronous replication — what does each risk, and what's the standard compromise?
  A: - **Async**: leader acks before followers confirm. Risk: leader dies → **acknowledged writes are lost** on failover (the new leader never received them). Fast, 

## distributed.replication.multi-leader — Multi-Leader
Multi-datacenter writes, conflict detection and resolution, why LWW loses data.
- `distributed-collab-editing-replication` Q: Why is real-time collaborative editing (Google-Docs-style) formally a multi-leader replication problem, and what dial does the size of the editing unit control?
  A: - Each user's device holds a **local replica it writes to immediately** (no round-trip per keystroke, works offline) and syncs asynchronously — that *is* multi-
- `distributed-conflict-detection-siblings` Q: Mechanically, how does a replica decide that two writes to the same key *conflict* rather than one superseding the other — and what does it do with the pair?
  A: Each key carries a **version vector** (one counter per leader/replica). A client reads, gets the value plus its version (an opaque "causal context"), and echoes
- `distributed-multi-leader-conflict-timing` Q: The reason multi-leader conflicts are painful is *when* they are detected: in single-leader (or serializable) systems the second writer is {{c1::blocked or given an error while it is still on the request path, so the user can be asked to retry}}, whereas in multi-leader replication both writes are {{c2::accepted and acknowledged locally, and the conflict only surfaces asynchronously when the two leaders exchange logs — nobody is on the line to ask}}. The practical consequence is that resolution must be {{c3::automatic and deterministic (every replica must reach the same answer independently), or deferred by storing siblings for a later on-read merge}}. It also means synchronous conflict detection ("make one write wait for the other leader") is possible but {{c4::throws away the entire point of multi-leader — independent local writes — so you should use single-leader instead}}.
- `distributed-multi-leader-fit` Q: When is multi-leader replication the right call despite its conflict problem, and what are the main conflict-resolution options?
  A: Right call when writes must be accepted in **multiple locations independently**: multi-region apps writing locally (cross-region RTT too high for one leader), o
- `distributed-multi-leader-retrofit-hazards` Q: You turn on multi-leader replication between two datacenters of a database designed for a single leader. Beyond same-key write conflicts, which database features quietly break, and why?
  A: Features that assumed "exactly one node assigns/enforces this" now run independently on every leader: - **Auto-increment keys collide**: both leaders hand out i
- `distributed-multi-leader-topologies` Q: Circular, star, and all-to-all multi-leader topologies — what does each risk, and what extra metadata does every one of them need?
  A: - **Circular / star**: each write forwards along a fixed path. One node down **breaks the chain** until reconfigured, and every write pays multiple hops. MySQL'
- `distributed-offline-client-writes` Q: Why is an offline-capable mobile/desktop app a multi-leader system, and which two schema decisions does that force on you?
  A: Every device has a full local replica that **accepts writes while disconnected** and syncs later — that is exactly multi-leader, with the peculiar property that

## distributed.replication.leaderless — Leaderless & Quorums
Dynamo-style quorums, sloppy quorums and hinted handoff, read repair and anti-entropy.
- `distributed-anti-entropy-cost` Q: Anti-entropy repair is "just a background job" — what does it actually cost, and what breaks if you skip it for too long?
  A: Cost: each pair of replicas builds a **Merkle tree over its ranges** (full read of the data on disk — CPU + IO comparable to a table scan), exchanges hashes top
- `distributed-leaderless-failed-write` Q: In a Dynamo-style leaderless store (N=3, W=2), a write reaches only 1 replica and the client gets an error. Is the value gone? What must the application assume about "failed" writes?
  A: No — the value is **not rolled back**. Leaderless stores have no transaction/abort machinery: the one replica that took the write keeps it. - Later reads may **
- `distributed-leaderless-monotonic-reads` Q: In a Dynamo-style store with W=2, R=2, N=3, a client reads a value and then reads it again and gets an *older* value. Explain how, and why the leader-based fix doesn't apply.
  A: A write reaches replicas one at a time. Read 1's coordinator happened to contact `{A, B}` where A had the new value; read 2's coordinator contacted `{B, C}` — n
- `distributed-leaderless-staleness-monitoring` Q: For a leader-based database you graph replication lag on a dashboard. Why can't you build the same "how stale are reads" graph for a leaderless store, and what do you do instead?
  A: - **Leader-based lag is measurable by subtraction**: writes are applied in one order from a single log, so `leader position − follower position` (or the timesta
- `distributed-quorum-math` Q: Leaderless replication with N replicas: reads see the latest acknowledged write when {{c1::W + R > N}} (write and read sets must intersect). With N=3, W=2, R=2 you tolerate {{c2::one}} replica down for both reads and writes. Setting W=1, R=1 maximizes availability/latency but reads can miss recent writes. Caveat: {{c3::sloppy quorums (writes landing on non-home nodes during faults)}} break the intersection guarantee even when W + R > N — Dynamo-style stores need hinted handoff plus read repair/anti-entropy to converge.
- `distributed-read-repair-anti-entropy` Q: In leaderless stores, read repair vs anti-entropy — how does each catch replicas up, and why do you need both?
  A: - **Read repair**: on a quorum read, the coordinator compares versions across replicas and writes the newest value back to any stale ones — repairs happen on th
- `distributed-sloppy-quorum-handoff` Q: Trace a write under a sloppy quorum with hinted handoff: where does it land, when does it get home, and what are the two ways it never gets there?
  A: The key's N home replicas are decided by the ring. If some are unreachable, the coordinator writes to the **first N reachable nodes instead**, and a stand-in st

## distributed.partitioning.schemes — Hash vs Range
Hash and range partitioning trade-offs; consistent hashing and virtual nodes.
- `distributed-consistent-hashing` Q: In consistent hashing, what fraction of keys moves when a node joins an N-node ring, why is that the whole point, and what problem do virtual nodes solve?
  A: Only ~**K/N** of K keys move — the keys between the new node and its predecessor on the ring. With naive `hash(key) mod N`, changing N remaps **almost every key
- `distributed-hash-vs-range` Q: Hash partitioning vs range partitioning: what does each optimize, and what workload wrecks each?
  A: - **Hash**: uniform key spread → even load, no planning. Wrecked by **range queries** — "last hour of events" scatters across every shard (scatter-gather). - **
- `distributed-partition-hash-properties` Q: What properties must the hash function used for hash partitioning have, which common property does it NOT need — and why is a language's built-in `hash()` a routing bug waiting to happen?
  A: Needs: - **Deterministic across processes, machines, languages, and versions** — every producer/router/client must map the same key to the same partition, forev
- `distributed-rendezvous-hashing` Q: Rendezvous (highest-random-weight) hashing vs a consistent-hashing ring — how does it work, and when is it the better pick?
  A: For a key, compute `hash(key, node)` for **every** node and pick the node with the highest score; for k replicas, take the top k. Membership change moves only t
- `distributed-shard-key-one-way-door` Q: Why is the shard key the highest-stakes decision in a sharded design, and what four properties do you check before committing to one?
  A: Because it is a **one-way door**: the key determines physical placement of every row, so changing it means rewriting the entire dataset. DynamoDB partition keys
- `distributed-vnode-count` Q: Choosing the number of virtual nodes (tokens) per physical node is a variance-vs-overhead trade: with V random tokens per node, load imbalance shrinks roughly as {{c1::1/sqrt(V)}}, which is why naive random placement needs V in the hundreds (Cassandra's historic default was {{c2::256 tokens per node}}) to keep ownership within a few percent of even. The cost of a large V is {{c3::more ranges to track in the ring/metadata, and repair and streaming fragmenting into many small ranges — Merkle-tree repair and bootstrap get slower and more IO-bound}}. Modern deployments therefore drop V drastically (Cassandra 4+ recommends {{c4::16 tokens with the allocation algorithm, which places tokens deliberately to balance load instead of relying on randomness}}). Rendezvous hashing and bounded-load variants sidestep the tuning entirely.

## distributed.partitioning.rebalancing — Rebalancing & Routing
Moving partitions without downtime; who knows where a key lives — routing tiers and coordination services.
- `distributed-dynamic-split-merge` Q: How does dynamic (split/merge) partitioning work, what triggers each operation, and what's the pitfall on an empty database?
  A: Ranges are split when a partition exceeds a size or load threshold — HBase regions (~10 GB), CockroachDB ranges (~512 MiB), DynamoDB partitions (10 GB or when t
- `distributed-fixed-partition-count` Q: The fixed-partition trick: create far more logical partitions than nodes up front (say 1024 partitions on 10 nodes) and rebalance by {{c1::reassigning whole partitions to different nodes — the key-to-partition function never changes, only the partition-to-node map}}. Adding a node then means {{c2::stealing a few partitions from every existing node, and only the partitions being moved are in flight; reads/writes keep going against the old owner until the handover completes}}. The permanent cost is that the partition count is effectively {{c3::fixed for the life of the dataset, so it caps the maximum number of nodes (one partition per node) and sets a floor on per-partition overhead (memory, files, repair units) when the cluster is small}}. Elasticsearch's per-index shard count and Kafka's per-topic partition count are the same design — which is why {{c4::increasing partitions later requires a reindex/split, and for Kafka breaks key-to-partition ordering for existing keys}}.
- `distributed-rebalance-throttling` Q: Why is fully automatic, unthrottled rebalancing a well-known way to turn a small failure into an outage — and what are the standard guards?
  A: Rebalancing consumes exactly the resources you are short of: disk IO, network, and page cache, **at the moment the cluster is already degraded**. The cascade: a
- `distributed-rebalancing-strategy-choice` Q: Three rebalancing strategies — fixed total partition count, dynamic split/merge, and a fixed number of partitions *per node* — each hold a different quantity constant. Which, and how does that decide the choice?
  A: - **Fixed total count** (Kafka topics, Elasticsearch shards): the *number of partitions* is constant; partition **size grows with data**. Choose when you can pr
- `distributed-rebalancing` Q: How do you resplit/rebalance a sharded store without downtime, and what is the classic mistake in choosing partition count?
  A: Live migration recipe: (1) start copying the moving range to the new shard while (2) **dual-writing or streaming changes** (CDC) to keep it in sync, (3) when ca
- `distributed-request-routing` Q: A client holds a key — how does the request find the right partition's node? Give the three routing approaches and where the partition map lives.
  A: - **Ask any node**: nodes share the map (gossip) and forward misdirected requests — no extra infra, one possible extra hop (Cassandra, Riak). - **Routing tier**

## distributed.partitioning.skew — Hot Keys & Skew
Detecting and defusing hot partitions — key salting, splitting, and request-level caches.
- `distributed-data-skew-vs-access-skew` Q: Distinguish data skew from access skew. Which remedies apply to each, and which remedy is useless for one of them?
  A: - **Data skew**: one partition holds disproportionate *bytes/rows* (a range partition on `country` where one country is 60% of users; a tenant with 100x the dat
- `distributed-hot-key-detection` Q: You suspect a hot key but can't emit a metric per key (billions of them). How do you actually find it, and at which layer?
  A: Use a **heavy-hitters sketch**, not per-key metrics: a **count-min sketch** or **space-saving / top-K** structure keeps the top N keys by frequency in fixed mem
- `distributed-hot-key` Q: A celebrity account makes one partition take 100x the traffic of the rest. Why doesn't adding shards help, and what does?
  A: Adding shards rebalances *keys*, but all this load is on **one key** — it still lands on a single partition. Skew, not capacity, is the problem. - **Reads**: ca
- `distributed-salting-read-cost` Q: Salting a hot key writes to `key#0 … key#(S-1)`, spreading writes over up to S partitions, but the reader now must {{c1::fan out S requests and merge the results — read cost and read tail latency are multiplied by S, since latency is the max over S shards}}. Pick S from {{c2::the ratio of the hot key's traffic to a single partition's capacity, plus headroom — not a fixed constant, and applied only to keys detected as hot}}. You can avoid the fanout entirely when the salt is {{c3::derived deterministically from something the reader already knows (e.g. suffix = hash(user_id) % S), so a per-user read goes to exactly one salted key}} — the fanout is only unavoidable when the read genuinely needs the aggregate over all writers. For read-hot rather than write-hot keys, salting is the wrong tool: {{c4::replicate the value into a cache tier / add read replicas instead, since reads don't need to be partitioned to be scaled}}.
- `distributed-tenant-isolation-limits` Q: One tenant's runaway job saturates a shared shard and everyone on it gets timeouts. Which mechanisms contain the blast radius, and what does each actually bound?
  A: - **Per-key / per-tenant rate limits** (token bucket at the routing tier, keyed by tenant): bounds the *offender's* request rate, so the shard never saturates. 

## distributed.partitioning.indexes — Partitioned Secondary Indexes
Local vs global secondary indexes — scatter-gather reads vs write amplification.
- `distributed-avoiding-scatter-gather` Q: You need a second access pattern on a sharded table and don't want scatter-gather. What are your options besides a built-in global index, and how do you choose?
  A: - **Query-shaped duplicate table** ("one table per query", Cassandra idiom): write the same fact twice, partitioned differently. You own the fanout on write and
- `distributed-global-index-staleness` Q: A global (term-partitioned) secondary index is updated asynchronously. Name the two failure modes this creates for application logic, and the operational gotcha nobody expects.
  A: - **Read-your-writes is gone on the index path**: you write an item and immediately query the index — the item is missing (usually sub-second, but unbounded whe
- `distributed-index-write-amplification` Q: Write amplification from global secondary indexes: inserting one row with k global indexes costs {{c1::1 + k writes, and each index write lands on a different partition (usually a different node) than the base row}}. Updating a row is worse than inserting it, because for each index whose indexed column changed you must {{c2::delete the entry under the old term and insert one under the new term — 2 index writes per changed indexed column, in two different index partitions}}. This is why the standard guidance is {{c3::index only the attributes you actually query on, and project only the attributes the query needs (DynamoDB KEYS_ONLY / INCLUDE beat ALL, since every projected attribute is copied on every write)}}. It is also why the writes cannot be transactional with the base row at scale: {{c4::making them atomic would require a distributed transaction across partitions on every single write, so systems make the index eventually consistent instead}}.
- `distributed-scatter-gather-fanout-math` Q: A scatter-gather query fans out to 100 shards, each with a p99 of 10 ms. What is the query's latency distribution, and what do you do about it?
  A: The query finishes when the **slowest** shard replies, so you need *all* 100 under 10 ms: `0.99^100 ≈ 0.37`. About **63% of queries exceed 10 ms** — the per-sha
- `distributed-secondary-index-partitioning` Q: Local (document-partitioned) vs global (term-partitioned) secondary indexes on a sharded store — who pays, the writer or the reader?
  A: - **Local index**: each partition indexes only its own rows. Writes touch one partition (cheap, transactional with the row), but a query on the indexed field mu

## distributed.transactions.isolation — Isolation Levels & Anomalies
Read committed to serializable through the anomalies each level permits — dirty/non-repeatable reads, write skew, phantoms.
- `distributed-dirty-write` Q: A car sale updates two rows: `listings.buyer` and `invoices.recipient`. Two concurrent buyers' transactions interleave so that Alice wins the listing but Bob gets the invoice. Name the anomaly, and how even the weakest standard isolation level prevents it.
  A: **Dirty write** — a transaction overwrites a value that another *uncommitted* transaction has written. Interleaved dirty writes let two transactions each win on
- `distributed-isolation-anomalies` Q: Map the standard isolation levels to the anomaly each one newly prevents, and name the anomaly snapshot isolation still allows.
  A: | Level | Newly prevents | |---|---| | Read committed | Dirty reads/writes | | Repeatable read / **Snapshot isolation** | Non-repeatable (fuzzy) reads; SI gives
- `distributed-lost-update-vs-write-skew` Q: Lost update and write skew are both "two transactions read, then write based on what they read." What structurally separates them, and why do the standard lost-update defenses fail against write skew?
  A: - **Lost update**: both transactions **write the same object** they read (two read-modify-write increments of one counter; one overwrites the other). - **Write 
- `distributed-materializing-conflicts` Q: A booking system checks "is room 101 free 12–1pm?" and inserts a reservation — but there is no existing row for the time slot, so `SELECT ... FOR UPDATE` locks nothing and double-bookings slip through. What is the "materializing conflicts" technique, and why is it a last resort?
  A: The failure is a **phantom**: the conflict is between a query predicate and a *future insert*, and you cannot lock rows that don't exist yet. **Materializing th
- `distributed-phantoms-predicate-locks` Q: What is a phantom, why can't row locks stop it, and how do databases approximate predicate locks in practice?
  A: A **phantom**: one transaction's write (an insert, or an update moving a row into range) changes the result of another transaction's **search condition** — e.g.
- `distributed-read-committed-anomalies` Q: Give a concrete anomaly that read committed permits but repeatable read/snapshot isolation prevents, and one that *both* permit.
  A: **RC permits read skew (non-repeatable read).** Accounts A and B hold $500 each. Your report reads A ($500), a transfer of $100 A→B commits, then your report re
- `distributed-repeatable-read-dialects` Q: Postgres and MySQL/InnoDB both offer `REPEATABLE READ`. Name three behavioral differences that bite in production.
  A: - **Phantoms**: InnoDB RR blocks them for *locking* reads via next-key (gap) locks; Postgres RR is snapshot isolation — plain reads never see phantoms, but noth
- `distributed-write-skew` Q: On-call rule: at least one doctor must stay on shift. Two doctors, in concurrent transactions, each check "≥2 on call" and sign themselves off. Both commit under snapshot isolation. Name the anomaly and two fixes.
  A: **Write skew**: each transaction's read set was invalidated by the *other's* write, but since they wrote **different rows**, SI's write-write conflict detection

## distributed.transactions.concurrency-control — Concurrency Control
2PL vs MVCC vs SSI — how databases actually enforce isolation, and their contention behavior.
- `distributed-2pl-vs-ssi` Q: Two-phase locking vs serializable snapshot isolation — how does each achieve serializability, what does each cost, and when does each win?
  A: - **2PL (pessimistic)**: acquire shared locks to read, exclusive to write, hold **all** locks until commit. Readers block writers and vice versa; cost = deadloc
- `distributed-actual-serial-execution` Q: Besides 2PL and SSI there is a third road to serializability: actually executing transactions serially, one at a time on a single thread (VoltDB/H-Store; Redis works this way too). What makes this viable at all, and what three conditions must hold?
  A: Viable because removing concurrency removes **all** concurrency-control overhead — no locks, no deadlocks, no aborts-and-retries — and a single core plowing thr
- `distributed-deadlock-handling` Q: Under 2PL, what makes the deadlock rate explode, how do engines resolve deadlocks, and what do you change in the application?
  A: Rate scales viciously: deadlock frequency grows roughly with **concurrency squared and transaction length to the fourth power**, divided by the number of distin
- `distributed-mvcc-defaults` Q: MVCC lets readers and writers avoid blocking each other: each transaction reads {{c1::a snapshot of versions committed before it started}}, while writers create new row versions instead of overwriting. The cost is {{c2::version garbage that must be cleaned up (Postgres vacuum; long-running transactions hold the snapshot horizon back and cause bloat)}}. Default isolation in Postgres and MySQL/InnoDB respectively: {{c3::read committed and repeatable read}}.
- `distributed-mvcc-visibility` Q: MVCC visibility rules — when transaction T (with its snapshot) may see a row version: the version's creator must have {{c1::committed before T's snapshot was taken}}, and the creator must not be in {{c2::the list of transactions that were still in progress at snapshot time (recorded when the snapshot is taken)}}, nor aborted, nor have a txid later than the snapshot. A deleted row stays visible to T until {{c3::the deleting transaction is itself visible under the same rules — deletes just mark the version with the deleter's txid; physical removal is garbage collection's job}}.
- `distributed-ssi-abort-behavior` Q: Your Postgres app moves to `SERIALIZABLE` and starts throwing 40001 errors under load. What is SSI doing, and what are the levers?
  A: SSI never blocks; it tracks each transaction's **read set** (SIRead predicate locks) and aborts a transaction when a dangerous read-write dependency structure a
- `distributed-ssi-detection-points` Q: SSI lets transactions run on snapshots without blocking, then aborts the ones whose premises went stale. Concretely, at which two points does the engine notice that a transaction acted on outdated information?
  A: Both detections target the same event — a read that a concurrent write invalidated — caught from the two possible directions: - **Detecting a stale read (write 

## distributed.transactions.distributed — Distributed Transactions
2PC mechanics and blocking, why it's avoided at scale, and what replaces it.
- `distributed-2pc-avoidance` Q: Why is two-phase commit avoided for cross-service transactions at scale, and what do systems do instead?
  A: 2PC is a **blocking protocol with a single point of failure**: after voting "prepared", a participant must hold locks and cannot unilaterally commit or abort — 
- `distributed-2pc-blocking-window` Q: 2PC's cost model, in numbers you can quote: a commit needs {{c1::two round trips to the slowest participant, plus a durable log flush (fsync) at every participant and at the coordinator}}. Availability of the transaction is {{c2::the product of all participants' availabilities — five 99.9% services give 99.5%, so the composite is worse than any member}}. The blocking window when the coordinator dies is {{c3::not a timeout but the coordinator's full recovery time — in-doubt participants hold their locks for as long as it takes a human or a failover to restore the coordinator's log}}, and if that log is lost the only resolution is {{c4::a heuristic decision by an operator, which may commit one participant and abort another — silently breaking atomicity, with reconciliation left to the business}}. The structural fix used by Spanner/CockroachDB is {{c5::making the coordinator itself a replicated state machine (its decision log lives in a Raft/Paxos group), so coordinator failure costs an election, not an outage}}.
- `distributed-2pc-mechanics` Q: Walk the two phases of 2PC and point at the exact commit point. Why can a participant that voted "yes" not simply time out and abort?
  A: 1. **Prepare**: coordinator sends `prepare` with a global txid. Each participant does everything but commit — writes its changes and locks durably to its log — 
- `distributed-internal-vs-heterogeneous-2pc` Q: Spanner and CockroachDB run two-phase commit on essentially every cross-shard write and perform fine, while XA-style 2PC across a database plus a message broker is notorious. Same protocol — what makes the internal case workable and the heterogeneous case not?
  A: - **The participants are replicated shards, not single machines.** In an internal system each participant and the coordinator state live in a Paxos/Raft group —
- `distributed-saga-tradeoffs` Q: A saga replaces a distributed transaction with local transactions plus compensations. Precisely which ACID property do you lose, and what do you do about it?
  A: You keep **atomicity in the eventual sense** (every step either completes or is compensated) and lose **isolation**: each local step commits immediately, so oth
- `distributed-xa-in-practice` Q: What is XA, and what specifically goes wrong when a team adopts it to keep a database and a message broker in sync?
  A: XA is the standard C API/protocol for 2PC across heterogeneous resource managers (a DB, a JMS broker, another DB), driven by a transaction manager that usually 

## distributed.consensus — Consensus
Why single-leader systems need election, what Raft guarantees, fencing tokens, and the cost of quorum writes.
- `distributed-consensus-in-practice` Q: Where does consensus actually sit in production architectures, and why don't you run your main data path through it?
  A: It sits in the **control plane**, on small state: leader election, cluster membership, shard→node maps, distributed locks, config — via etcd/ZooKeeper (Kubernet
- `distributed-coordination-service-primitives` Q: ZooKeeper and etcd are "consensus in a box." Which small set of primitives do they expose, and how do those compose into the classic recipes (distributed lock, leader election, group membership)?
  A: - **Linearizable writes / compare-and-set**: every update goes through total order broadcast, so a conditional write ("create if absent", "set if version = n") 
- `distributed-election-disruption` Q: A Raft node is cut off by a flaky network link. While isolated, it repeatedly times out and increments its term; when the link heals, its inflated term forces the healthy leader to step down even though nothing was wrong. Name the two standard defenses.
  A: The bug pattern: raw Raft treats **any higher term as authority**, so one flapping node can repeatedly depose a working leader — each heal triggers a needless e
- `distributed-epoch-numbers` Q: Every consensus protocol carries an epoch number (term/ballot/view) and runs two quorum checks. What problem do epochs solve, and how do the two quorums interact?
  A: Epochs solve "**which of two would-be leaders is current**" without relying on clocks: within one epoch there is at most one leader, and a **higher epoch always
- `distributed-fencing-tokens` Q: A client holds a distributed-lock lease, pauses for a 20s GC, then resumes and writes — but its lease expired and another client took the lock. How do fencing tokens prevent the corruption, and why can't the client fix this itself?
  A: The lock service issues a **monotonically increasing token** with every lock grant. The *protected resource* (storage) records the highest token it has seen and
- `distributed-flp-and-escape` Q: The FLP result proves consensus is impossible — yet Raft and Paxos clusters reach agreement in production every second. State what FLP actually claims, and the loophole every practical protocol uses.
  A: **The claim is narrower than the slogan**: in a *fully asynchronous* system (no bounds on message delay or processing speed, hence no useful clocks or timeouts)
- `distributed-quorum-sizing` Q: Consensus tolerating f crashed nodes requires {{c1::2f + 1}} nodes (majority quorums must intersect) — so 3 nodes tolerate 1 failure, 5 tolerate 2. A 4-node cluster tolerates {{c2::still only 1 failure (majority is 3), which is why even cluster sizes are pointless}}. Every committed write costs {{c3::a round-trip to the slowest node of the fastest majority}}, which is the latency argument against stretching a consensus group across distant regions.
- `distributed-raft-guarantees` Q: What does Raft actually guarantee about leaders and logs, and what mechanism enforces each guarantee?
  A: - **Election safety**: ≤1 leader per term — each node votes once per term, and a candidate needs a **majority**; two majorities always intersect. - **Leader com
- `distributed-raft-linearizable-reads` Q: Why can't a Raft leader serve linearizable reads from its local state without extra work, and what are the two standard fixes?
  A: The leader may be **deposed and not know it** (partitioned away, long GC pause): a new leader is already committing writes elsewhere, so the old one's local rea
- `distributed-total-order-broadcast` Q: Total order broadcast guarantees {{c1::reliable delivery (no message lost) and totally ordered delivery — every node sees the same messages in the same order}}; it is formally {{c2::equivalent to consensus — each position in the shared log is one consensus decision, so Raft/Paxos give you TOB and vice versa}}. You get linearizable compare-and-set/uniqueness on top of it by {{c3::appending your claim to the log, reading the log back, and winning only if your message is the first claim for that key — log position is the serial order}}. This log framing is why "replicated state machine", "Raft log", and "Kafka partition ordering" are the same idea at different fault-tolerance levels.

## distributed.time.clocks — Clocks & Timestamps
Time-of-day vs monotonic clocks, NTP drift, timestamp ordering hazards, confidence intervals, logical clocks.
- `distributed-clock-error-sources` Q: Every server in your fleet runs NTP, so an engineer assumes timestamps are accurate "to within a millisecond or so." Walk through the error sources that make tens of milliseconds — or unbounded error — the honest assumption.
  A: - **Quartz drift between syncs**: cheap oscillators drift on the order of tens to hundreds of parts per million with temperature — at 200 ppm that's ~17 s/day; 
- `distributed-hybrid-logical-clocks` Q: Lamport timestamps respect causality but bear no relation to wall time; wall clocks read like real time but can order a cause after its effect. What do hybrid logical clocks (HLC) do to get both, and where are they used?
  A: An HLC timestamp is a pair: **(physical component, logical counter)**. - On every event, take the max of the local wall clock and the largest physical component
- `distributed-lamport-vs-vector` Q: Lamport timestamps vs vector clocks: what question can a vector clock answer that a Lamport clock cannot, and what does that cost?
  A: **"Were these two events concurrent?"** Lamport clocks (single counter: bump on local event, take max+1 on receive) guarantee only one direction: A happened-bef
- `distributed-lww-danger` Q: Why is last-write-wins by wall-clock timestamp a data-loss mechanism, not a conflict resolution strategy?
  A: Wall clocks on different nodes disagree: NTP sync leaves ms–100s of ms of skew, clocks **step backwards** on correction, and VMs pause. So "last" is decided by 
- `distributed-monotonic-vs-wallclock` Q: Time-of-day clock vs monotonic clock — which do you use for timeouts and elapsed-time measurement, and what goes wrong if you pick the other?
  A: **Monotonic** for all durations (timeouts, latency measurement, rate limiting): it only moves forward, at a steady rate. Its absolute value is meaningless and *
- `distributed-truetime` Q: Spanner's TrueTime API returns not a timestamp but {{c1::an interval [earliest, latest] bounding the true time (uncertainty from GPS/atomic clock sync, typically a few ms)}}. To make timestamp order match real-time order, a transaction {{c2::commit-waits: holds its result until `latest` of its commit interval has passed}}, guaranteeing every later-starting transaction gets a strictly greater timestamp — this is how Spanner achieves external consistency (strict serializability) across datacenters, paying clock uncertainty as write latency.

## distributed.time.failure — Failure Detection & Pauses
Timeouts as the only failure detector, process pauses (GC, VM suspend), system models, and defending a chosen timeout.
- `distributed-failure-detection` Q: Why can no timeout prove a remote node is dead, and how do real systems pick and use timeouts anyway?
  A: In an asynchronous network you can't distinguish **crashed** from **slow / partitioned / GC-paused**: no reply within T is consistent with all of them, and the 
- `distributed-network-delay-queueing` Q: Datacenter round trips are "sub-millisecond", yet your timeouts must tolerate delays thousands of times larger. Where does the variability in network delay actually come from, and what does that imply for choosing timeouts?
  A: Almost all of it is **queueing**, at every stage of the path: - **Switch buffers** when several senders burst into one link (incast); overflow means drops, and 
- `distributed-process-pause-causes` Q: Distributed algorithms must assume any node can freeze for seconds to minutes at any line of code, then resume as if nothing happened. List the real causes of such pauses, and explain why the paused process cannot defend itself.
  A: Causes, all routine: - **Stop-the-world GC** — worst-case collections run seconds to minutes on large heaps. - **VM suspension / live migration** — the whole gu
- `distributed-system-models` Q: Crash-stop vs crash-recovery vs Byzantine fault models — what does each assume, and which (plus which timing model) do mainstream datacenter systems design for?
  A: - **Crash-stop**: a faulty node halts and never returns — clean but unrealistic. - **Crash-recovery**: nodes may crash and come back, keeping **stable storage**

## distributed.crdt — CRDTs & Local-First
Conflict-free replicated data types, merge semantics, and offline-capable multi-writer apps.
- `distributed-crdt-convergence` Q: What algebraic properties must a CRDT's merge function have, and what operational freedoms do those properties buy?
  A: Merge must be **commutative** (order doesn't matter), **associative** (grouping doesn't matter), and **idempotent** (merging the same state twice is harmless) —
- `distributed-crdt-counters` Q: A G-counter (grow-only) keeps {{c1::one slot per replica; each replica increments only its own slot}}; the value is {{c2::the sum of all slots}}, and merge is {{c3::element-wise max}} — max is idempotent, so re-merging never double-counts, which is exactly why a single shared integer can't work (summing two copies double-counts, max loses increments). A PN-counter supports decrement by {{c4::pairing two G-counters — increments and decrements — and reporting P − N}}. Limitation worth stating: it can transiently go below an intended floor (e.g. negative inventory), because no CRDT can enforce a global invariant without coordination.
- `distributed-crdt-state-vs-op` Q: State-based vs operation-based CRDTs — what does each ship over the network, and what does each demand from the delivery channel?
  A: - **State-based (CvRDT)**: ship the whole state (or a **delta**) and merge. Demands almost nothing from the network — duplicates, reordering, and lost messages 
- `distributed-local-first-limits` Q: A local-first app (Automerge/Yjs-style) writes to the local replica and syncs in the background. What does the server shrink to, and which requirements force real server-side logic back in?
  A: The server shrinks to a **dumb relay + durable store of encrypted ops/states** — it never resolves conflicts, because CRDT merge runs on every client; clients g
- `distributed-or-set` Q: Replicated set: replica A removes element x while replica B concurrently re-adds x. Why do naive sets and 2P-Sets get this wrong, and how does an OR-Set resolve it?
  A: - **Naive set**: add/remove don't commute, so replicas that see them in different orders diverge — no well-defined answer. - **2P-Set**: removals go to a tombst
- `distributed-sequence-crdt-positions` Q: Two collaborative-text replicas both apply "insert at index 5" — and the document diverges, because their index 5s were different characters. How do sequence CRDTs (text/list CRDTs) identify positions so that concurrent edits merge correctly?
  A: Indexes are **relative to a state that other replicas don't share**, so sequence CRDTs abandon them: every element gets a **permanent, globally unique position 
