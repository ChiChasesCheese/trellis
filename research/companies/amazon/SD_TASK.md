# Task — data-intensive system design + LLD layer (senior bar)

Read `AGENT_RULES.md` (especially "Bar: senior") and, when it exists, `catalog/raw/forums.md` (design prompts reported for AWS).
Reuse before writing: the system-design domain `vault/domains/system-design/` (DDIA-2-structured map, cards, readings,
47-problem bank in `drills/problems/`) and the LLD bank `vault/domains/low-level-design/problems/` (45 problems incl.
`design-amazon-locker.md`, `design-in-memory-file-system.md`, `design-parking-lot.md`). Link them; never copy them.

You own `sd/` and `lld/` in the Amazon kit.

1. `sd/00_ddia_refresh.md` — textbook-mode refresher of the DDIA ideas an AWS data-services design round leans on,
   for someone who has forgotten most of it: storage engines (B-tree vs LSM, compaction, write/read amplification),
   replication (leader/follower, multi-leader, leaderless/quorums, replication lag anomalies), partitioning (hash vs range,
   hot keys, rebalancing, secondary indexes), transactions & isolation (read committed → snapshot → serializable, anomalies
   with tiny examples), consensus & leases (Raft in plain words, fencing tokens), stream processing (log, CDC, exactly-once
   = idempotency + transactions, watermarks), batch vs stream, encoding & schema evolution. Each concept: what / why /
   how (ASCII diagram) / which AWS service embodies it (DynamoDB, Aurora, S3, Kinesis, Redshift, Glue — cite AWS papers or
   docs: Dynamo 2007, DynamoDB 2022 USENIX ATC, Aurora SIGMOD 2017, S3 ShardStore SOSP 2021) / the domain card or reading
   to review (link by path). End with self-check questions.
2. `sd/00_how_to_run_the_round.md` — a 45–60 min senior design round: requirements → API → data model → high level →
   deep dives → bottlenecks/failure → operations (on-call, metrics, deployment safety: Amazon's one-box / cell-based
   architecture / shuffle sharding — cite AWS Builders' Library). Include back-of-envelope estimation from zero.
3. `sd/problems/` — 5 AWS-data-flavoured problems **not already in the domain bank**, each with prompt / requirements /
   estimation / model answer at senior depth / deep-dive follow-ups with answers / rubric (strong vs ok vs weak):
   CDC replication pipeline (DMS-like), data-lake ingestion + catalog (Glue/Lake Formation-like), managed time-series or
   metrics store with downsampling, serverless query over S3 (Athena-like: partition pruning, columnar formats),
   multi-tenant control plane for a managed database (provisioning, backups, failover). Plus `sd/route.md`: which
   existing domain-bank problems to do and in what order (KV store, object storage, message queue, metrics monitoring,
   job scheduler, ad-click aggregation, distributed cache, top-k), each with the Amazon-specific twist to practise.
4. `lld/route.md` + `lld/` — Amazon's favourite OOD prompts (from the research file if available: Amazon Locker,
   Unix `find` / file search with filters, parking lot, …): for each, link the existing bank file if present; for any
   missing one, write a full textbook-mode solution in Python (classes, SOLID choices, extension follow-ups) with
   runnable code + asserts in `lld/code/` (run them with `python3 -I`).
Final reply ≤ 12 lines: files and line counts (wc), which papers/docs you actually fetched, weakest claims.
