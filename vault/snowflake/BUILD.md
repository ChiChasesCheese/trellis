# Snowflake Internals — BUILD

> Durable record for skill `building-study-domains` (`.claude/skills/building-study-domains/SKILL.md`).
> A new session resumes from **Next action**.

## Source survey (step 1)

| # | Outline | URL | Licence | Covers |
|---|---|---|---|---|
| 1 | Official docs guides TOC | https://docs.snowflake.com/en/guides | free online | architecture, micro-partitions & clustering, warehouses, caching, query profile, search optimization, time travel / fail-safe / cloning, loading / Snowpipe / streams / tasks / dynamic tables, security, sharing, cost |
| 2 | SIGMOD 2016 "The Snowflake Elastic Data Warehouse" (Dageville et al.) | https://dl.acm.org/doi/10.1145/2882903.2903741 | paper (free author PDF widely mirrored) | multi-cluster shared-data architecture, Cloud Services, storage format, pruning, execution engine, time travel, security |
| 3 | SnowPro Core certification exam guide | https://learn.snowflake.com/en/certifications/snowpro-core/ | free | exam domains: architecture, account & security, performance, loading & transformation, data protection & sharing |
| 4 | Snowflake-Labs/awesome-snowflake | https://github.com/Snowflake-Labs/awesome-snowflake | free (270★, last push 2024-04) | curated tools, docs and learning links across the platform |
| 5 | Snowflake engineering blog | https://www.snowflake.com/en/engineering-blog/ | free | FoundationDB metadata, execution internals, adaptive join optimization |
| 6 | Interview kit material | `../interviews/companies/snowflake/study/20-cards/snowflake_internals.md` · `study/00-prereq/04-snowflake-primitives.md` · `study/00-essentials/05-sd-framework-snowflake-primitives.md` | own | what interviewers probe; primitives referenced by SD answers |

**Gap in step 1**: the survey agent stalled before writing this file; the table above was reconstructed from the skeleton header. The per-heading **outline → leaf mapping** required by step 2's completion criterion is not written yet (see Next action).

## Skeleton (step 2)

`skeleton/snowflake.yaml` — Chinese (`lang: zh`, translated 2026-09-14, ids and `requires` verified unchanged), 16 top-level nodes, 110 leaves, `requires` edges on most non-foundational leaves. `uv run trellis --domain snowflake validate` → 0 errors.

| Node | Leaves |
|---|---:|
| architecture · Core Architecture | 6 |
| storage · Storage Engine & Micro-partitions | 8 |
| metadata · Metadata & Cloud Services | 6 |
| warehouse · Virtual Warehouses | 7 |
| query · Query Compilation & Execution | 8 |
| pruning · Pruning & Query Optimization | 6 |
| cache · Caching Layers | 5 |
| txn · Transactions & Concurrency Control | 6 |
| continuity · Time Travel, Fail-safe & Cloning | 7 |
| semistructured · Semi-structured Data | 4 |
| ingestion · Data Loading & Ingestion | 7 |
| pipelines · Streams, Tasks & Dynamic Tables | 11 |
| security · Security & Governance | 10 |
| sharing · Data Sharing & Collaboration | 4 |
| openplatform · Open Formats & Workload Expansion | 7 |
| cost · Cost, Metering & Observability | 8 |

## Ledger

| Date | Step | Result | Evidence |
|---|---|---|---|
| 2026-09-14 | 1 survey | 6 outlines identified (docs TOC official) | skeleton header; table above |
| 2026-09-14 | 2 skeleton | 126 nodes / 110 leaves; translated to Chinese | `validate` 0 errors; id/requires comparison script equal |
| 2026-09-14 | 3 corpus | `corpora/snowflake-docs.yaml`: 36 docs URLs, 35 ingested (fail-safe page skipped as too short); triage 34 readings (Chinese) + 1 gap; 77/110 leaves have a reading | `proposals/snowflake-docs.json`; `stats` readable sources 77/110 |
| 2026-09-14 | 4 cards (in progress) | group C done: pruning, security, sharing, openplatform, cost — 35 leaves, 174 cards (24 digest, 11 grow); groups A and B relaunched on opus after the sonnet session limit | `validate` 0 errors, no self-containment warnings |
| 2026-09-14 | 4 cards | group B done: cache, txn, continuity, semistructured, ingestion, pipelines — 40 leaves (38 this run: 29 digest, 9 grow), 196 cards this run | `validate` 0 errors; stats full leaf coverage per B node |
| 2026-09-14 | 4 cards | group A done: architecture, storage, metadata, warehouse, query — 32 leaves this run (19 digest, 13 grow), 158 cards; step 4 complete: 110/110 leaves, 553 cards | `stats` every node full; `validate` 0 errors |
| 2026-09-14 | 4 dedupe | `warehouse.resource-monitors` and `cost.resource-monitors-and-budgets` came from the same doc page: 5 duplicate cards removed → 548 cards; the cost leaf keeps 2 cards and needs Budgets cards | question-by-question comparison |
| 2026-09-14 | 2 skeleton fix | cards contradicted the skeleton: `txn.snapshot-isolation` retitled to READ COMMITTED; `txn.optimistic-concurrency-conflicts` summary now says UPDATE/DELETE/MERGE take table locks | docs: transactions page; ids unchanged |

## Gaps from triage

- `security.end-to-end-client-side-encryption` (proposed leaf): TLS in transit plus client-side encryption with a customer-held master key, distinct from `security.encryption-key-hierarchy`.

## Grown cards to review (step 5)

Written by `grow` without a source; check these claims first:
- `openplatform.snowflake-postgres`: the product is new, every card.
- `cost.ai-token-metering`: the `CORTEX_FUNCTIONS_*` view names.
- `security.encryption-key-hierarchy`: key rotation about every 30 days, rekeying of keys older than a year.
- `security.trust-center-posture`: scanner details.
- Thin-source digest leaves: the three sharing leaves shared one short intro page (marketplace listings, reader-account billing added from general knowledge); `openplatform.external-engine-commit-protocol` follows the Iceberg spec rather than its page.
- Group B (grow, no source): `continuity.clone-storage-billing` (`RETAINED_FOR_CLONE_BYTES`), `semistructured.schema-evolution-tables` (allowed column changes: add column, drop NOT NULL), 7-day Fail-safe on the continuity cards.
- `ingestion.datastream-kafka-compatible`: product announced at Summit 2026, private preview; cards carry no numbers.
- Task graph size limit left out of the pipelines cards (skeleton says 100, source silent).
- Group A (grow, no source): `metadata.execution-anchor` (weakest: 4 general cards), FoundationDB limits (~5 s and 10 MB per transaction, 100 KB per value), EXPLAIN output formats, JoinFilter and CartesianJoin operator names.
- Link coverage is low for metadata (15%) and query (26%): step 6 should add the SIGMOD 2016 paper and engineering-blog readings there first.

## Next action

1. Add Budgets cards to `cost.resource-monitors-and-budgets` (grow).
2. Step 5 review of the grown-card list above, then step 6 readings for the 33 leaves without one (SIGMOD 2016 paper, engineering blog), then step 7 drills per top-level node linked to `../interviews/companies/snowflake/` (sd03, sd08, sd12).
3. Still owed from step 2: the outline heading → leaf mapping table for outlines 1–3.
