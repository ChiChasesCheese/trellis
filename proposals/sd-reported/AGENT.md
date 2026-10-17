# Reported system-design write-ups — instructions for one agent

Folder: `vault/interviews/core/system-design/amazon/` (index `sd-index.md`; gate `python3 scripts/check_sd.py`). Each write-up is one file
`sdNN-<slug>.md` for a system-design question that Amazon candidates reported between 2026-09-16 and 2026-10-16.
Reader: Chi, payments data-infrastructure engineer (PayPal), Amazon onsite 2026-10-20/21, **prepared to the senior /
staff bar** (Chi: 「不要调整 bar」). Repository root `/Users/chizhang/Code/trellis`. Do not run git; do not start agents;
touch only your own `sdNN-*.md` files.

> **`proposals/WRITING_RULES.md` overrides everything below** (Chi, 2026-10-16): provenance only in the last section, textbook voice to the reader, cause → effect, self-contained, diagrams `flowchart TB` that fit the page. `scripts/plain_style.py` enforces it inside the gate.

## Inputs (read-only)

- Your problem's brief below (quotes, dates, confidence).
- Hello Interview pages Chi's membership unlocks, saved as text: `/Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_sd/*.txt`
  (bitly, gopuff, dropbox, ticketmaster, ad-click-aggregator, metrics-monitoring, flash-sale, notification-system,
  job-scheduler, patterns dealing-with-contention / large-blobs / multi-step-processes / scaling-writes,
  deep-dive change-data-capture, numbers-to-know). URL = `https://www.hellointerview.com/learn/system-design/<problem-breakdowns|patterns|deep-dives|core-concepts>/<name>`.
  **Reuse rule (Chi: "reuse hellointerview materials if overlap")**: where a HI page covers your problem, follow its
  skeleton (requirements → entities → API → high-level → deep dives) and adopt its strongest trade-off points, credited
  inline as 「（对照 Hello Interview《Bitly》）」, then go past it at the staff level. **The repo is public and HI is paid:
  never copy a sentence, a diagram or a number table from it; paraphrase, link, and say where you disagree.**
- This repo's general solutions: `vault/domains/system-design/readings/problems/solution-<name>.md` (link them by
  wikilink `[[solution-url-shortener]]`; don't re-teach what they cover — write the Amazon delta and the senior depth).
- The Amazon kit: `vault/interviews/companies/amazon/sd/` (DDIA refresh, how to run the round, AWS data-service designs),
  `catalog/raw/forums.md` §3–4 (what Amazon SD rounds look like). Chi's resume: `vault/interviews/core/resume/resume.tex`.

## The write-up — exactly these `##` sections, in order (the gate checks)

1. `## 题目` — the system in plain words (what it is, who uses it, what makes it hard), then the prompt as an
   interviewer would give it to you. No sources, dates or labels here.
2. `## 澄清问题` — 6–8 questions, each with what the answer changes in the design.
3. `## 需求` — functional (3–5, ranked), non-functional with numbers (latency p99, availability, durability,
   consistency per operation), explicitly out of scope.
4. `## 容量估算` — QPS, storage, bandwidth, the one number that drives the design; every result computed (show the
   formula and the result; run `python3 -c` yourself — never type an arithmetic result from memory).
5. `## 核心实体与 API` — entities with keys; REST/gRPC signatures; idempotency keys where writes retry.
6. `## 高层架构` — a ```mermaid `flowchart LR` of the whole system, then a walk through the two main flows; at least
   one ```mermaid `sequenceDiagram` of the critical path.
7. `## 深挖` — at least three `###` deep dives, the hard ones for *this* problem (e.g. ID generation and collision,
   hot keys, cross-region consistency, contention on the last unit of inventory). Each: the problem sharply → 2–3 real
   options with costs → choice and why → failure mode. At least one more mermaid diagram in here (state diagram,
   data flow, or partition layout). Use AWS building blocks where natural (DynamoDB, S3, SQS/SNS, Kinesis, Aurora,
   Step Functions) and say what each guarantees — this is an AWS Data Services loop.
8. `## Staff 视角：权衡、故障与演进` — what breaks first at 10×, the blast radius of each component's failure, multi-
   region story, cost drivers, migration/rollout, operability (metrics, alarms, runbooks). This is what separates
   senior from staff — be concrete.
9. `## 面试官追问` — 6–10 follow-ups an Amazon interviewer asks, each with a 2–4 sentence answer.
10. `## 60 分钟怎么分配` — minute table: what to draw/say, what to cut when short (Amazon rounds often spend 10–15
    minutes on LP first, so give the 45-minute version too).
11. `## 自测` — 5 questions, answers in `<details>`.
12. `## 延伸阅读` — study links only: the repo's general solution as a wikilink, docs or tutorial pages with a neutral
    label. **No provenance anywhere on the page** (WRITING_RULES §1): never where/when the question was reported, no
    confidence, no 「（重建）」 — the brief's facts are for you only.

Chinese prose, English terms in full-width parentheses on first use; ≥ 9,000 characters outside code. Diagrams: valid
mermaid, `flowchart TB` only, ≤ 12 nodes and ≤ 16-char labels each — draw the write path and the read path as two
diagrams rather than one big one. No 「本题」「这道题」, no process talk
(「我验证过」「对拍」), no lodely / vervecopilot. Wikilinks must resolve to an existing note name.

## Gate

`python3 scripts/check_sd.py sdNN` must print `ok`. Then re-read once as a skeptical
staff interviewer: is every number derived, is each deep dive a real decision, would the design survive the first
follow-up?

## Report (≤ 12 lines)

Per file: the gate line, prose characters (from the gate or `wc`), mermaid count, and the three claims you are least sure of.

## Briefs

### SD01 `sd01-url-shortener.md` — 短链接服务（URL Shortener）
- 1p3a 1193105 (posted 2026-10-14; SDE II, in-person onsite 2026-10-02, four rounds) summary: "task and course scheduling,
  URL shortener design, and Amazon Locker LLD"; OP's reply 2026-10-15: 「都是dry run，不用跑。System Design连图都没画」
  https://www.1point3acres.com/bbs/thread-1193105-1-1.html [high for the name; body hidden].
- Hello Interview `url-shortener-design`: 12 Amazon reports 2022-09..2026-09 (latest 2026-09-01 senior USA); 2025-09-20
  mid EMEA: "Asked at Amazon. Exact same question. But I didn't had much time, since some portion of the interview was LP."
  https://www.hellointerview.com/community/questions?company=Amazon [medium].
- HI overlap: `hi_sd/bitly.txt`. Repo: [[solution-url-shortener]], drill design-url-shortener. Senior depth: ID
  scheme trade-offs (counter + base62 vs hash + collision), 301 vs 302 and analytics, hot links and caching tiers,
  custom aliases, expiry and deletion, abuse/malware, multi-region read path, DynamoDB key design.

### SD02 `sd02-amazon-lockers.md` — Amazon Lockers 投递系统（Amazon Lockers Delivery）
- Hello Interview `amazon-lockers-delivery`: 14 Amazon reports 2024-01..2026-09 (latest 2026-09-10 senior). Prompt:
  "a package delivery system that integrates with e-commerce platforms, allowing customers to select locker locations
  during checkout and securely retrieve their packages using authentication codes." 2025-12-20 senior EMEA: "design for
  drop and pickup for delivery and return of the item"; 2025-01-10: "Design from Point of Sale to Locker Delivery".
- 1p3a 1193105 (2026-10-02 onsite) asked the LLD version — the LLD lives in `[[solution-amazon-locker]]` (low-level-design
  bank) and leaf `amazon.amz-locker-onsite`; this write-up is the distributed system around it.
- HI overlap: ticketmaster (reserve a slot without double-booking), notification-system, multi-step-processes (delivery
  saga), dealing-with-contention. Depth: capacity reservation at checkout vs at delivery, reservation TTL, the locker
  device as an edge client with intermittent connectivity (offline codes), code security, returns flow, carrier
  integration, per-site sharding.

### SD03 `sd03-dc-stock-state.md` — 配送中心库存状态服务（Distribution Center Stock State）
- 1p3a question bank row `distribution-center-stock-state-service` (onsite-system-design, reported 2026-09-18, 1 source;
  tags: distributed-systems, data-modeling, ingestion, sharding, idempotency) — body locked [medium for name and tags;
  the prompt is （重建） from the tags: ingest stock events from many DCs, serve current stock state per SKU per DC].
- Related older reports: HI `warehouse-inventory-architecture` (2025-03), 1p3a bank `perishable-goods-tracking-system`
  (phone, 2026-06-24), `fulfillment-center-inventory-transfer` (onsite coding, 2026-07-22).
- HI overlap: gopuff (availability across DCs), flash-sale (last-unit contention), deep-dive change-data-capture.
  Depth: event-sourced ledger vs mutable counters, idempotent ingestion (dedupe keys, out-of-order events), sharding by
  (dc, sku) and hot SKUs, read model for "where can I fulfil from", reservations vs on-hand, reconciliation with cycle
  counts. Chi's payments-ledger background maps directly: say so.

### SD04 `sd04-fs-replication.md` — 文件系统跨区域数据复制（File System Replication）
- Hello Interview `file-system-replication` 2026-10-01 mid: "1. Interviewer didn't care about how the data is uploaded.
  2. Design only the replication part. How does data transfer from region 1 to region 2 efficiently?" [medium].
- HI overlap: dropbox (chunking, dedupe), patterns/large-blobs, deep-dive change-data-capture. Repo [[solution-file-sync]],
  [[solution-object-storage]]. Depth: change log / CDC as the replication source, chunk-level dedupe and delta transfer,
  ordering and conflict (single-writer per file vs multi-master + LWW/vector clocks), replication lag SLO, bandwidth
  budgeting and backpressure, S3 Cross-Region Replication as the managed comparison, repair/anti-entropy (Merkle).

### SD05 `sd05-vaccine-booking.md` — 疫苗资格与预约（Vaccine Eligibility & Booking）
- Hello Interview `vaccine-eligibility-booking` 2026-09-10 senior: "a vaccine distribution system that manages dynamic
  inventory replenishment and configurable eligibility rules, allowing eligible users to book vaccine appointments by
  location and date." [medium; no candidate notes].
- HI overlap: ticketmaster (slot reservation, waiting room), patterns/dealing-with-contention. Repo
  [[solution-ticket-booking]], [[solution-hotel-reservation]]. Depth: rules engine for eligibility (versioned, data-driven,
  evaluated at booking and re-checked at the appointment), slot inventory with dose inventory as a second constraint,
  surge on opening day (queue, fairness), replenishment changing capacity under live bookings, PII handling.

### SD06 `sd06-agent-security.md` — Agentic AI 安全事件平台，1 TB/天（AI Agent Security Telemetry）
- 1p3a 1192714 (2026-10-11, L5, three 1-hour phone rounds, AWS agentic-AI security product team, Austin): site summary
  "graph and topological-sort problems, AI agent security system design for 1 TB/day, and behavioral questions"; visible
  「我面的是这个是 Agentic AI的 security prosuct 组在AWS下面」 https://www.1point3acres.com/bbs/thread-1192714-1-1.html
  [medium; the prompt beyond "AI agent security system, 1 TB/day" is （重建）: ingest agent actions / tool calls / prompts,
  detect policy violations, alert, investigate].
- HI overlap: ad-click-aggregator and metrics-monitoring (stream ingestion + aggregation), patterns/scaling-writes.
  Repo [[solution-ad-click-aggregation]], [[solution-metrics-monitoring]]. Depth: 1 TB/day → events/s and bytes/s
  (compute it), Kinesis/Kafka partitioning by tenant/agent, real-time rules vs batch detection, hot path vs cold path
  (S3 + Athena/OpenSearch), multi-tenant isolation, PII/prompt redaction, alert dedupe, late events and watermarks.

### SD07 `sd07-external-sort.md` — 大文件外部排序，200 GB / 8 GB 内存（External Sort）
- Hello Interview `external-sorting-system` 2026-09-10 mid: "you have files over 200gb which just contain numbers. these
  files can be present on multiple computers. Your server has a total disc memory = 500gb, and you have 8gb ram. How will
  you sort all the numbers? (you cant do any .sort() function …)" — the candidate called it "LLD ish" [medium].
- No HI breakdown; cite HI patterns/large-blobs only if it helps. Depth: run generation (replacement selection gives runs
  ≈ 2× memory), k-way merge with a heap and buffer sizing (compute fan-in from 8 GB and the I/O block size), passes needed,
  disk budget (200 GB input + runs within 500 GB), distributed version (range partition by sampled splitters → each
  machine sorts its range → concatenate; that is TeraSort / MapReduce shuffle), integer-specific tricks (counting /
  radix when the value range is bounded), failure and restart of a long merge. Include a short runnable Python sketch
  of the k-way merge in a code block (not counted as prose).


## Batch 2 (2026-10-17) — files go in `vault/interviews/core/system-design/amazon/`

Titles of low-priority write-ups end with `（low priority）` in the H1 (WRITING_RULES §8). Facts below are for you only.
More detail for any of them: `grep -n "<keyword>" research/companies/amazon/catalog/raw/forums.md`.

### SD13 `sd13-employee-directory.md` — 员工目录与 DynamoDB 分区键（Employee Directory） — recent, no label
- Phone screen 2026-09: "Design an Employee Directory for Amazon ... Search by name/email/employee ID ... ~1M employees ...
  Read-heavy"; follow-ups on the DynamoDB schema and partition key; what if a person changes name/team. Depth: access
  patterns first → table + GSIs, hot keys, prefix search (name) via an index service, org-chart queries, cache, freshness.

### SD14 `sd14-kindle-sync.md` — Kindle 阅读进度同步（Kindle Sync）（low priority）
- Bar Raiser round L5 2026-07 and SDE II 2025-07: "Design Kindle reader" — offline, multi-device reading progress,
  idempotent API, conflict resolution; download ebooks to devices. Depth: per-(user, book) position with vector of
  device clocks vs LWW + furthest-read rule, offline queue + idempotent sync, annotations merge, DRM-light download/CDN.

### SD15 `sd15-artifact-repository.md` — 制品仓库（Artifact Repository）（low priority）
- AWS Dublin SDE2 2026-08: "Design Artifact Repository (like JFrog, adding an artifact and fetching an artifact)" —
  probed scalability, metrics monitoring, reliability, extensibility (malicious artifact). Depth: content-addressed blobs
  in S3 + metadata DB, immutable versions, upload sessions, scanning pipeline before publish, read path via CDN, quotas.

### SD16 `sd16-lambda-execution.md` — Lambda 式代码执行（Serverless Code Execution）（low priority）
- SDE II US 2025-09 and Hello Interview (3 reports): "Design AWS Lambda, especially focus on the Worker Nodes on
  how/where the code will be executed", sync and async invocations. Depth: placement on worker fleet, warm/cold sandboxes
  (microVM), concurrency limits per function, async queue + retries + DLQ, isolation/multi-tenancy, scaling the fleet.

### SD17 `sd17-sensor-platform.md` — 传感器与天气数据平台（Sensor / Weather Platform）（low priority）
- Hello Interview: weather system with thousands of sensors (4 reports, latest 2026-02), smart-city sensors computing
  hourly averages (3), temperature sensors every 10 km² over 10M km² with real-time and historical views (2). Depth:
  ingestion (IoT protocol, batching), time-series storage + downsampling/rollups, hourly aggregates (streaming windows),
  spatial queries (geohash tiles), late/duplicate readings, sensor health.

### SD18 `sd18-catalog-search-cdc.md` — 影视目录搜索与 CDC（Catalog Search with CDC）（low priority）
- L5 2026-05: "Design Netflix" with "movie search using a reverse index db like OpenSearch and a CDC pipeline". Depth:
  source of truth DB → CDC (DynamoDB Streams / Debezium) → indexer → OpenSearch; ordering and idempotent index updates,
  backfill/reindex with aliases, search relevance basics, freshness SLO, failure of the indexer.

### SD19 `sd19-device-fleet.md` — 设备管理平台（Device Fleet Management）（low priority）
- AWS (security-flavoured) onsite 2026-07, HM round: "a system to manage thousands of devices". Depth: device registry,
  desired vs reported state (shadow), config rollout in waves with health gates and rollback, command delivery to
  offline devices, certificates/identity, fleet queries.

### SD20 `sd20-db-backup.md` — 数据库备份系统（Backup: full / diff / log）（low priority）
- India 2026-04: "Design backup system with three different backup types (full, diff, log)". Depth: full + differential
  + log backups and the restore chain (PITR), scheduling and retention, storage in S3 with lifecycle, consistency of a
  backup (snapshot vs WAL), verification by test restores, RPO/RTO numbers computed.

## Batch 2b — the five AWS data-service designs already in the folder (`problems/*.md`)

Convert each into the 12-section write-up format, keeping its content, as `sd08-cdc-replication-pipeline.md`,
`sd09-data-lake-ingestion-catalog.md`, `sd10-managed-db-control-plane.md`, `sd11-metrics-timeseries-store.md`,
`sd12-serverless-query-over-s3.md` (in `amazon/`, not `amazon/problems/`), then delete the old file by overwriting it
with nothing and reporting it. No priority label (they target the AWS data-services team).
