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
  "storage.relational.indexing": ["<id shown first>", "…"],
  "storage.relational.operations": ["<id shown first>", "…"],
  "storage.internals.btree": ["<id shown first>", "…"],
  …
}

## storage.relational.indexing — Indexing
B-tree indexes, composite and covering indexes, leftmost-prefix rule, when indexes hurt.
- `storage-covering-index` Q: What makes an index "covering" for a query, why is it dramatically faster, and what's the cost of covering everything?
  A: The index contains **every column the query needs** (key columns + `INCLUDE`d payload), so the engine answers from the index alone — an **index-only scan** — sk
- `storage-hash-index-limits` Q: A hash index answers `WHERE id = ?` in O(1) — seemingly better than a B-tree's O(log n). Why is the B-tree still the default index almost everywhere? Name what hashing structurally cannot do.
  A: Hashing destroys **key order** — entries land wherever the hash function scatters them. That forfeits everything a sorted structure gives for free: - **Range qu
- `storage-index-leftmost-prefix` Q: You have a composite B-tree index on `(tenant_id, created_at)`. Which of these can use it efficiently: (a) `WHERE tenant_id = ?`, (b) `WHERE created_at > ?`, (c) `WHERE tenant_id = ? AND created_at > ?` — and why?
  A: (a) and (c). A composite index is sorted by the **leftmost column first**; entries for one `tenant_id` are contiguous, and within them sorted by `created_at`. (
- `storage-index-selectivity` Q: There is a B-tree index on the column, but `EXPLAIN` shows a sequential scan. Give the two distinct reasons a planner *chooses* not to use it, and the one that means it *cannot*.
  A: **Chooses not to (cost):** - **Low selectivity** — the predicate matches a large fraction of rows. An index scan costs ~1 random heap I/O per matching row; a se
- `storage-index-write-cost` Q: A table has 9 indexes "just in case." Quantify what each additional index costs the write path, and how you decide which ones to drop.
  A: - Every `INSERT`/`DELETE` becomes **1 + N structure updates** — each index takes a random-ish write into a different B-tree page, plus WAL bytes for each. Inser
- `storage-multicolumn-vs-bitmap-and` Q: Query: `WHERE a = ? AND b = ?`. You could build one composite index on `(a, b)` or rely on two existing single-column indexes on `a` and on `b`. How does the database actually use the two separate indexes, and when is the composite worth building anyway?
  A: With two single-column indexes, Postgres-style engines do a **bitmap index scan**: scan each index separately, build a bitmap of candidate row locations per ind
- `storage-partial-expression-index` Q: A 500M-row `jobs` table has 2k rows in `status='pending'` that a worker polls constantly. What index do you build, and what related index type fixes `WHERE lower(email) = ?`?
  A: A **partial index**: `CREATE INDEX ON jobs (run_at) WHERE status = 'pending'`. - Size tracks the **2k live rows**, not 500M — it stays fully cached, and entries

## storage.relational.operations — Operating at Scale
Connection pooling, read replicas, federation, MVCC maintenance, and when a single Postgres is the right answer.
- `storage-connection-pooling` Q: Why does a fleet of 200 app instances talking straight to Postgres fall over even at modest QPS, and what is the standard fix?
  A: Each Postgres connection is a **forked OS process** with its own memory (~5–10MB) and scheduling cost; a few thousand connections exhausts memory and burns CPU 
- `storage-mvcc-vacuum` Q: Postgres MVCC: what physically happens on `UPDATE`, and what operational problem does that create at high churn?
  A: Nothing is overwritten: `UPDATE` writes a **new row version** and marks the old one with the updating transaction's ID; each snapshot sees the versions visible 
- `storage-normalization-tradeoff` Q: Normalized vs denormalized schema: what exactly does each optimize, and what breaks when you denormalize?
  A: - **Normalized**: every fact stored **once** (many-to-one refs by ID). Optimizes writes and integrity — an update touches one row, no risk of divergent copies. 
- `storage-online-migration-four-phase` Q: A zero-downtime **online migration** (moving live data to a new model or store while still serving traffic, Stripe-style) runs in four phases: **1)** {{c1::dual-write — every new write goes to both the old and the new store}}; **2)** {{c2::backfill — copy all pre-existing data into the new store, rate-limited and checkpointed}}; **3)** {{c3::dual-read / verify — serve from the old path but read both and compare, alerting on any mismatch}}; **4)** {{c4::cut over reads to the new store, then delete the old write path and old data}}. Each phase is observable and reversible on its own, so the migration only advances when the data is proven consistent.
- `storage-online-migration-vs-one-shot` Q: You must move hundreds of millions of live rows to a new data model. Why is a one-shot migration (a single `ALTER TABLE`, or one big copy script run overnight) the wrong tool, and what does the incremental dual-write approach buy instead?
  A: One-shot fails on three counts: - **Locking / load**: a table rewrite or bulk copy hammers the primary and can block writes for hours on a table that must keep 
- `storage-replica-lag-ops` Q: You run Postgres read replicas. How do you actually measure replication lag (two units matter), and what workload events typically make it spike even when the network is fine?
  A: Measure both: - **Bytes**: how far the replica's applied WAL position (LSN) trails the primary's — the true backlog size, meaningful even when writes are bursty
- `storage-scaling-ladder` Q: Your single Postgres is saturating. Give the escalation ladder in order, and the signal that forces each step.
  A: 1. **Tune first**: indexes, query plans, caching, connection pooling — most "DB is slow" cases end here. 2. **Bigger box**: vertical scaling is boring and works

## storage.internals.btree — B-tree Mechanics
Fixed-size pages, splits, the WAL and crash recovery, in-place updates and their concurrency cost.
- `storage-btree-branching-depth` Q: A B-tree stores data in fixed-size pages (commonly 4KB), each internal page holding hundreds of child references — a branching factor of {{c1::~500}} is typical. Depth therefore grows with the *logarithm* of row count, so almost every real table fits in {{c2::3–4}} levels: with 4KB pages and 500-way branching, a 4-level tree already addresses about {{c3::256 TB}}. Practical consequence: a point lookup costs at most depth page reads, and since the root and inner levels are a tiny fraction of the tree they stay cached — usually leaving {{c4::one disk read (the leaf page)}} per lookup.
- `storage-btree-clustered-vs-heap` Q: InnoDB stores the full row inside the primary-key B-tree's leaf pages (clustered); Postgres leaves rows in a heap file and every index points into it. What does each layout win and lose on the read and write paths?
  A: - **Clustered (InnoDB)**: primary-key lookups and PK-range scans are one tree traversal — the leaf *is* the row, and rows adjacent in key order are adjacent on 
- `storage-btree-latches` Q: B-trees need latches (lightweight page locks) on the read *and* write path, while an LSM engine's in-memory writes get away with almost none. What structural difference explains this, and how do B-trees keep latching cheap?
  A: B-trees mutate shared pages **in place**: a reader descending the tree can otherwise observe a page mid-modification, or follow pointers that a concurrent **pag
- `storage-btree-page-split` Q: An insert lands on a B-tree leaf page that is already full. Walk through what the engine does, and explain how this mechanism keeps the tree balanced without any rebalancing job.
  A: A **page split**: 1. Allocate a new page; move half the full page's entries into it, so both end ~half full. 2. Insert the new key into the appropriate half. 3.
- `storage-btree-wal-recovery` Q: B-trees write pages in place. Why does that force a write-ahead log, and what is the torn-page problem?
  A: In-place page writes aren't atomic: crash mid-write and the tree is inconsistent — worse, a page split touches **multiple pages**, so a crash between them can o

## storage.internals.lsm — LSM-tree Mechanics
Memtable to SSTables, compaction strategies (size-tiered vs leveled), Bloom filters, tombstones.
- `storage-bloom-filter-properties` Q: A Bloom filter's two possible answers are asymmetric: one is trustworthy, one is not. State the asymmetry, why an LSM engine is safe with the untrustworthy side, and what knob trades memory for accuracy.
  A: - **"Definitely not present"** is guaranteed: if any of the key's hashed bit positions is 0, the key was never inserted. **No false negatives, ever** — this is 
- `storage-compaction-strategies` Q: Size-tiered vs leveled compaction in an LSM engine: how does each organize SSTables, and which workload picks which?
  A: - **Size-tiered** (Cassandra STCS): wait for ~4 similar-sized SSTables, merge into one bigger; tiers of ever-larger files. Each byte is rewritten few times (**l
- `storage-lsm-range-scan` Q: Point lookups aside — why is a *range scan* (`WHERE ts BETWEEN a AND b`) structurally harder for an LSM-tree than for a B-tree, and why don't Bloom filters help here?
  A: A B-tree holds the range as **one contiguous, already-merged run of leaf pages** — descend once, walk sibling pages. An LSM-tree's range is **scattered across e
- `storage-lsm-read-path` Q: Walk the read path for a point lookup in an LSM-tree, and name the structure that keeps misses cheap.
  A: 1. Check the **memtable** (in-memory, newest data). 2. Check immutable memtables awaiting flush. 3. Check SSTables newest-to-oldest, level by level; first hit w
- `storage-lsm-write-path` Q: LSM-tree write path, in order: (1) append the write to the {{c1::WAL (sequential log, for crash recovery)}}; (2) insert it into the {{c2::memtable — an in-memory sorted structure such as a skip list or red-black tree}}; (3) when the memtable exceeds its size threshold, make it immutable, swap in a fresh one, and {{c3::flush it to disk as an SSTable (a sorted, immutable file)}}; (4) in the background, {{c4::compaction}} merge-sorts SSTables together, keeping only each key's newest version and discarding shadowed values. The user-visible write finishes after step (2) — everything that touches disk in bulk happens {{c5::sequentially}}, which is the source of LSM write throughput.
- `storage-sstable-structure` Q: What exactly makes an SSTable's *sorted* order so valuable that LSM engines pay compaction forever to maintain it? Give the three concrete capabilities sorting buys inside one file.
  A: - **A sparse index suffices.** Because keys are in order, the in-memory index needs only one entry per block (every few KB), not per key: find the two index ent

## storage.internals.tradeoffs — Engine Trade-offs
Read, write, and space amplification; when B-trees beat LSM-trees and vice versa; in-memory engines.
- `storage-amplification-triangle` Q: Storage engines juggle three amplifications you can't minimize simultaneously: {{c1::write amplification}} (bytes physically written per byte of user write — LSM compaction rewrites data many times), {{c2::read amplification}} (structures consulted per lookup — LSM reads may touch many SSTables, B-trees ~one path), and {{c3::space amplification}} (disk used vs live data — LSM holds obsolete versions until compaction; B-trees carry fragmented half-empty pages). Leveled compaction trades higher write amp for lower read/space amp; size-tiered does the reverse.
- `storage-btree-single-copy-locking` Q: "In a B-tree, each key exists in exactly one place; an LSM-tree may hold several versions of it in different files." Why does this single-copy property make B-trees the comfortable substrate for *transactional* databases?
  A: Because most transaction machinery wants a stable, unique home per record: - **Locking**: a lock manager can attach a lock to *the* place a key lives (or to a l
- `storage-btree-vs-lsm` Q: When do you pick an LSM-tree engine (RocksDB, Cassandra) over a B-tree engine (Postgres, InnoDB), and what do you pay for it?
  A: Pick LSM for **write-heavy** workloads: writes are sequential appends (memtable + WAL, flushed to sorted SSTables), so ingest throughput far exceeds a B-tree's 
- `storage-compaction-interference` Q: An LSM store benchmarks beautifully, then in production shows periodic latency spikes and, under sustained ingest, throughput collapse. Explain the compaction-interference mechanism behind both symptoms, and what engines do about it.
  A: The disk's finite bandwidth is **shared** between the foreground write path (WAL + memtable flushes) and background compaction — and the read path competes for 
- `storage-inmemory-advantage` Q: A disk database with its working set fully in OS page cache still loses to Redis. If not disk reads, what is the in-memory store's real advantage — and how does it get durability anyway?
  A: It skips the machinery of pretending memory is disk: no encoding rows into disk-page format, no buffer-pool management, and it can use structures impractical to

## storage.nosql — NoSQL Families
Key-value, document, wide-column, graph — the access patterns each one exists to serve.
- `storage-document-locality-cost` Q: Document stores sell "storage locality" — the whole record in one read. What is the write-side price of that locality, and what two modeling rules does it impose?
  A: The document is stored as one contiguous blob, so most engines must **rewrite the entire document on update** — even to flip one boolean — and if the document g
- `storage-document-to-graph-signal` Q: Your data began as neat tree-shaped documents (user → orders → items). What change in the data's *shape* signals that a graph model now fits better than documents — and why can't documents absorb the change?
  A: The signal is **many-to-many connections proliferating**: entities start linking across trees (users referencing users, items shared by orders, organizations ↔ 
- `storage-document-vs-relational` Q: When does a document store (MongoDB-style) genuinely beat relational, and what access pattern signals you chose wrong?
  A: Document wins when data is naturally an **aggregate read/written as a unit** — the whole document loads in one op, schema varies per record, and locality beats 
- `storage-graph-db-fit` Q: What query shape justifies a graph database over a relational schema with join tables?
  A: **Variable-depth, multi-hop traversals**: "friends-of-friends-of-friends", fraud rings, dependency chains — where the number of hops isn't fixed at query time. 
- `storage-keyvalue-fit` Q: A pure key-value store (DynamoDB used as KV, Redis, Riak-style) is the simplest NoSQL family. What access pattern justifies choosing it as the system of record, and what capabilities do you knowingly give up?
  A: Choose it when **every access is by primary key** and the value is opaque to the store: sessions, shopping carts, user preferences, device state, feature flags.
- `storage-schema-on-read` Q: "Schemaless" document stores still have a schema. Where does it live, and when is schema-on-read genuinely better than schema-on-write?
  A: It's **implicit in the reading code** (schema-on-read): the database enforces nothing, so every consumer must handle every historical shape ever written. Schema
- `storage-secondary-index-partitioning` Q: In a partitioned store, secondary indexes can be local (document-partitioned) or global (term-partitioned). What does each cost, and which does DynamoDB's GSI use?
  A: - **Local**: each partition indexes only its own rows. Writes stay single-partition (index updated in the same operation), but a query on the indexed field must
- `storage-tombstone-deletes` Q: Why is a delete in Cassandra actually a *write*, and what makes "using a wide-column table as a queue" a famous anti-pattern?
  A: Data lives in immutable SSTables across replicas, so a delete writes a **tombstone** — a marker that shadows older values until compaction physically removes bo
- `storage-wide-column-modeling` Q: In Cassandra/DynamoDB-style wide-column stores, how does data modeling invert compared to relational, and what do partition key vs clustering (sort) key each decide?
  A: You model **query-first**: design one table per access pattern and denormalize, instead of normalizing then joining — there are no joins. - **Partition key** → 

## storage.record-modeling — Record Modeling
Shaping the records themselves — one table with a discriminating dimension versus separate stores, and vocabulary collision as a schema hazard.
- `storage-record-discriminator-column` Q: You store several kinds of similar records — say invoices, credit notes, and refunds. Option A: one table with a `kind` discriminator column. Option B: one table per kind. What does each option make easy and each make painful?
  A: **Single table + discriminator** wins on *shared behavior*: - Queries spanning kinds ("all financial events for account X, in time order") are one indexed scan 
- `storage-sparse-attributes` Q: Products in your catalog have wildly different attributes (screen size, shoe size, caffeine content…). Compare the three standard ways to store heterogeneous sparse attributes — wide table, EAV, JSON column — on querying, indexing, and validation.
  A: - **Wide table** (a column per attribute, mostly NULL): full SQL typing, constraints, and per-column indexes — but every new attribute is a DDL change, and hund
- `storage-vocabulary-collision` Q: Two teams share a table with a `status` column. To billing, `active` means "currently paying"; to support, it means "account not banned". Name this schema hazard, describe how it corrupts data without any bug in either codebase, and give the fix that beats "agreeing on a definition."
  A: **Vocabulary collision**: one field name, two meanings — the schema silently encodes two different business concepts in the same column. How it corrupts: each t

## storage.object — Object Storage & Separation
S3-style object stores, storage-compute separation, and the modern default of parking cold and big data there.
- `storage-compute-separation` Q: Storage–compute separation (Snowflake, BigQuery, modern lakehouses): what does putting the data in object storage buy, and what latency problem does it create?
  A: Buys **independent scaling and elasticity**: spin compute to zero or burst to hundreds of nodes without moving data; multiple engines (SQL, Spark, ML) read the 
- `storage-multipart-ranged-io` Q: Objects are written and read "whole" — so how do you move a 500GB object through S3 efficiently in both directions?
  A: - **Write: multipart upload** — split into parts (5MB–5GB each, up to 10,000), upload parts **in parallel with per-part retries**, then one CompleteMultipartUpl
- `storage-object-vs-filesystem` Q: What can't you do with S3-style object storage that you can with a filesystem or block store, and why doesn't that matter for its main use cases?
  A: No **partial update**: objects are written whole (PUT replaces; no seek-and-write into the middle), listing is a paged API call rather than a cheap directory re
- `storage-s3-conditional-writes` Q: S3's consistency model changed twice in the 2020s. What do you get now, and what new class of system did conditional writes unlock?
  A: - Since 2020: **strong read-after-write consistency** — a GET/LIST after any PUT (including overwrites) sees the latest version. The old eventual-consistency ca
- `storage-s3-numbers` Q: S3-class object storage is designed for {{c1::11 nines (99.999999999%)}} of *durability* — achieved by erasure-coding/replicating across multiple availability zones — but its *availability* SLA is only around {{c2::99.9–99.99%}}, so callers must still handle 5xx/retries. Durability ≠ availability: your bytes survive, but you can't always read them right now.
- `storage-small-objects-cost` Q: Storing 1 billion 4KB objects in S3 costs far more than the same 4TB as large objects. Where does the money and latency go, and what's the fix?
  A: Object storage prices and performs **per request, not per byte**: - **Requests dominate**: writing a billion objects ≈ $5k in PUTs alone; every read is a full G

## storage.search — Search Indexes
Inverted indexes, relevance basics, and keeping a search cluster in sync with the source of truth.
- `storage-inverted-index` Q: What is an inverted index, and why can't a B-tree index on a text column do the same job?
  A: A map from **term → posting list of documents containing it** (plus positions/frequencies), built after analysis (tokenizing, lowercasing, stemming). A query in
- `storage-search-deep-pagination` Q: Why does `from=99000, size=20` melt a sharded search cluster when page 1 is instant, and what's the correct pattern for deep result access?
  A: Results come from distributed top-K: **every shard** must compute and return its own top `from+size` (99,020) scored docs, and the coordinator merges all of the
- `storage-search-not-sot` Q: Why is a search cluster the wrong system of record, even though it stores full documents?
  A: - **No real transactions or strong consistency**: writes become visible only after a refresh (near-real-time, ~1s), and multi-document updates aren't atomic. - 
- `storage-search-nrt-refresh` Q: In Elasticsearch, a document is indexed successfully but a search doesn't find it for another second. Explain the mechanism — and why durability is a *separate* knob.
  A: Searchability requires a **refresh**: buffered docs are written into a new in-memory **segment** and only then become visible to queries. Refresh runs every 1s 
- `storage-search-segments` Q: Lucene segments are immutable. What do update and delete actually do, and what background process pays the bill?
  A: - **Delete**: the doc is only *marked* in a per-segment deletion bitmap; it still occupies space and is filtered out at query time. - **Update**: delete-mark th
- `storage-search-sync` Q: How do you keep Elasticsearch/OpenSearch in sync with the primary database, and why is "write to both from the app" the wrong answer?
  A: Dual writes from the app have **no transaction spanning both stores**: a crash or failed second write leaves them silently diverged, and retries can reorder upd

## storage.encoding — Encoding & Evolution
Data formats as contracts between code versions — JSON, Protobuf, Avro; forward and backward compatibility rules.
- `storage-avro-evolution-defaults` Q: In Avro, which schema changes keep *both* backward and forward compatibility, and why does the rule hinge entirely on default values? (Contrast with how Protobuf earns the same property.)
  A: The rule: you may **add or remove only a field that has a default value**. Why defaults are the whole story — schema resolution matches writer's and reader's fi
- `storage-avro-schema-resolution` Q: Avro encodes no field names *and* no tag numbers — just values in order. How can a reader with a different schema version decode it?
  A: Decoding requires the exact **writer's schema**; the reader then performs **schema resolution** against its own **reader's schema**: fields matched **by name** 
- `storage-dataflow-modes` Q: DDIA names three modes by which encoded data flows between processes. Name all three, and for each, say who the reader is and which compatibility direction that forces you to maintain.
  A: - **Through a database** — the reader is *a future process*, possibly years away: "sending a message to your future self." Forces **backward** compatibility acr
- `storage-encoding-compat-directions` Q: Schema evolution has two directions: {{c1::backward compatibility}} means **new code can read data written by old code** (the common, easier case — new readers handle old records), while {{c2::forward compatibility}} means **old code can read data written by new code** (harder — old readers must tolerate fields they don't know about, typically by {{c3::preserving/ignoring unknown fields}} rather than erroring or silently dropping them on rewrite).
- `storage-json-contract-pitfalls` Q: JSON is the default inter-service format anyway. Name its concrete weaknesses as a *data contract*, and what teams add to compensate.
  A: - **Numbers**: no int/float distinction, and integers beyond 2^53 silently lose precision in JS-lineage parsers — why Twitter-scale IDs ship as *strings*. - **N
- `storage-language-serialization-trap` Q: Java's `Serializable`, Python's `pickle`, Ruby's `Marshal` are one line of code. Why is language-native serialization considered unacceptable for anything persisted or sent between services? Give the four standing objections.
  A: - **Security**: decoding must be able to instantiate arbitrary classes named in the byte stream — untrusted input can therefore trigger attacker-chosen code pat
- `storage-protobuf-tag-rules` Q: In Protobuf, what identifies a field on the wire, and what are the evolution rules that follow from it?
  A: The **field tag number** — the wire format carries `(tag, wire-type, value)`, never field names. Hence: - **Renaming a field is free** (names are code-only); **
- `storage-rolling-upgrade-compat` Q: Why does a rolling deploy force you to maintain *both* backward and forward compatibility at once — and why does data in a database raise the bar further?
  A: During the rollout old and new instances run side by side, and messages/RPCs flow both ways: new code reads what old code wrote (**backward**), and old code rea
- `storage-unknown-field-roundtrip` Q: During a rolling upgrade, new code adds a `nickname` field to user records. Users set nicknames — then some mysteriously revert to empty, with no errors logged anywhere. Reconstruct the bug.
  A: An **unknown-field round-trip loss**, done by *old* code that was individually forward-compatible: 1. New code writes a record including `nickname`. 2. An old i
