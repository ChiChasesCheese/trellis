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
  "analytics.olap": ["<id shown first>", "…"],
  "analytics.warehouse": ["<id shown first>", "…"],
  "analytics.batch": ["<id shown first>", "…"],
  …
}

## analytics.olap — OLTP vs OLAP & Columnar
Why analytical scans want column layout, compression, and vectorized execution instead of B-trees.
- `analytics-column-store-writes` Q: Compressed sorted columns can't be updated in place. How do column stores accept writes anyway?
  A: The LSM move: writes land in a small **row-oriented (or unsorted) in-memory delta store**, and queries transparently merge the delta with the immutable, compres
- `analytics-columnar-compression` Q: Name the two compression tricks that make columnar storage so effective, and why sorting the column first multiplies their effect.
  A: - **Dictionary encoding**: replace repeated values with small integer codes (a `country` column becomes 1–2 bytes per row). - **Run-length / bitmap encoding**: 
- `analytics-data-cubes` Q: A dashboard slices sales by any combination of date, product, store, and promotion, and every query answers in milliseconds without scanning the fact table. What structure makes that possible, and what does it fundamentally give up?
  A: A **data cube (OLAP cube)**: a materialized grid of aggregates precomputed along the dimensions — e.g. `SUM(net_price)` for every (date, product) cell, plus sub
- `analytics-replica-analytics-limits` Q: "Why buy a warehouse? Just point the analysts at a read replica of the production database." Give the reasons this stops working as analytics grows up.
  A: - **Wrong storage layout**: the replica is still a row-store with OLTP indexes — a scan-and-aggregate over 100M rows does orders of magnitude more I/O than a co
- `analytics-row-vs-column-layout` Q: An analytical query averages one column over 100M rows. Why does a row-store (OLTP) engine do orders of magnitude more I/O than a column store, even with the same data?
  A: A row store lays each row's columns contiguously, so reading one column drags **every other column of every row** through disk and memory — and B-tree indexes d
- `analytics-star-schema` Q: Describe the star schema, and why warehouses tolerate wide, denormalized dimension tables that would be bad OLTP design.
  A: One huge **fact table** of events (sale, click, shipment) — each row a narrow record of foreign keys plus numeric measures — surrounded by **dimension tables** 
- `analytics-vectorized-execution` Q: What is vectorized execution, and what cost of the classic row-at-a-time (Volcano) model does it eliminate?
  A: Operators process **batches of a few thousand column values at a time** (a "vector") instead of pulling one row through the whole operator tree per `next()` cal

## analytics.warehouse — Warehouses & Lakehouses
Warehouse vs data lake vs lakehouse; open table formats (Iceberg/Delta) over object storage.
- `analytics-lake-vs-warehouse-vs-lakehouse` Q: Warehouse vs data lake vs lakehouse — what does each own, and what gap does the lakehouse close?
  A: - **Warehouse** (Snowflake, BigQuery): the engine owns storage *and* format — great SQL performance, transactions, governance; but data is locked to one engine 
- `analytics-lakehouse-compaction` Q: A streaming pipeline commits to an Iceberg/Delta table every minute. What degrades over time, and what's the maintenance answer?
  A: **Small-file buildup**: each commit writes tiny Parquet files, so queries pay per-file overhead — metadata/footer reads, one object-store GET each (~tens of ms 
- `analytics-lakehouse-snapshot-isolation` Q: Object storage has no transactions. How do Iceberg/Delta provide snapshot isolation and atomic commits on top of it?
  A: Data files are **immutable**; a commit writes new data + a new metadata tree, then atomically swings a single **root pointer** to it — via a catalog compare-and
- `analytics-table-formats` Q: Iceberg/Delta are "just metadata over Parquet files." What do they actually add that a directory of Parquet files lacks?
  A: - **Atomic commits / snapshots**: a table version is a metadata file listing exactly which data files belong; readers never see half-written jobs (no more `_SUC
- `analytics-time-travel-retention` Q: Lakehouse time travel works because commits never delete data files — old snapshots keep referencing them. The costs are storage growth and unbounded metadata, so tables need {{c1::snapshot expiration / vacuum}} to drop snapshots past a retention window and physically delete unreferenced files. Two operational consequences: you can only roll back or audit within {{c2::the retention window}}, and GDPR-style hard deletes aren't complete until expired snapshots' files are {{c3::physically removed}}, not just dropped from the latest snapshot.

## analytics.batch — Batch Processing
MapReduce lineage to Spark; shuffles, distributed joins, idempotent reruns, and batch vs stream boundaries.
- `analytics-batch-vs-stream` Q: What is the real boundary between batch and stream processing, and how does each recover from failure?
  A: The input: batch reads a **bounded** dataset of known size (job can finish, sort, and take multiple passes); streaming reads an **unbounded** log and must produ
- `analytics-data-locality-shift` Q: MapReduce's scheduler fought to place each task on the machine that already held its input block ("move computation to the data"); modern cloud batch stacks happily read everything from S3 over the network. What made data locality worth so much then, and what changed?
  A: Then: clusters ran on **spinning disks behind ~1 Gbps links**, so reading a block over the network was dramatically slower than reading it locally, and cross-ra
- `analytics-idempotent-reruns` Q: Why are batch jobs designed so the whole run can be thrown away and re-executed, and what two properties of the job make that safe?
  A: Because failure handling *and* bug recovery both become "just run it again": a crashed job, a bad deploy, or a logic error discovered next week are all fixed by
- `analytics-intermediate-state-pipelining` Q: A classic MapReduce workflow chains five jobs, writing every intermediate result to the replicated distributed filesystem; Spark runs the same logic as one job several times faster. What exactly did dataflow engines change about intermediate state, and what new problem did that create?
  A: MapReduce's model: each job **fully materializes** its output to HDFS (replicated 3x) before the next job may start. That buys durability and clean job boundari
- `analytics-join-strategies` Q: Distributed join of a 10TB fact table with a 200MB dimension table: sort-merge join or broadcast hash join, and why?
  A: **Broadcast hash join**: ship the 200MB table to every executor, build an in-memory hash table, and stream the 10TB side through it — the big table never shuffl
- `analytics-shuffle-mechanics` Q: Walk through what a shuffle actually does in Spark/MapReduce, and why it's the step that dominates job cost.
  A: 1. Each map task **partitions its output by hash of the key** (one bucket per reducer) and spills sorted bucket files to local disk. 2. Every reduce task then *
- `analytics-skew-stragglers` Q: A 1000-task stage finishes in 5 minutes except one task still running after an hour. Give the two distinct causes and the fix for each.
  A: - **Data skew (hot key)**: hash partitioning sent one giant key (the null key, the whale customer) to one reducer. Fixes: **salt the key** (split it into `key#0

## analytics.derived — Derived Data & Materialized Views
Treating caches, indexes, and views as recomputable projections of a log — and keeping them fresh.
- `analytics-backfill-cdc` Q: You're standing up a new derived view (search index, feature store) from a database that already holds years of data. Why do you need two pipelines, and how do you stitch them without gaps or double-processing?
  A: CDC alone can't help: the log doesn't retain history back to the beginning, so you need a **backfill** (bulk load from a snapshot) *plus* the **CDC tail** for o
- `analytics-cache-as-derived` Q: Reframe cache invalidation as a derived-data problem. What does the reframing buy you over app-managed invalidation?
  A: A cache entry is a **materialized view of a query**; "invalidation" is just view maintenance. Instead of application code remembering to delete keys on every wr
- `analytics-derived-data-framing` Q: What distinguishes a "system of record" from "derived data", and why does the distinction change how you operate each?
  A: - **System of record**: the authoritative first write; if it's lost, the data is gone. Must be durable, transactional, carefully protected. - **Derived data**: 
- `analytics-derived-view-versioning` Q: A bug shipped in the transformation logic behind a derived table that consumers query in production. What's the safe repair pattern?
  A: **Build v2 side-by-side, then swap** — never patch in place: 1. Fix the logic, run it as a new derived view from the retained log / raw source, writing to a sep
- `analytics-lambda-vs-kappa` Q: Lambda architecture vs Kappa architecture for keeping derived views both fresh and correct — what does each run, and what pain made the industry drift from the first toward the second?
  A: - **Lambda**: run the same derivation **twice** — a streaming layer produces fast approximate/incremental results, a nightly batch layer recomputes authoritativ
- `analytics-materialized-view-maintenance` Q: A materialized view is stale the moment its base table changes. Compare the two maintenance strategies and when each wins.
  A: - **Full recompute on a schedule** (the classic warehouse/batch approach): simple, self-healing — every run erases previous errors — but freshness = schedule in
