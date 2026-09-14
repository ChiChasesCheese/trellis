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

`skeleton/snowflake.yaml` — English (no `lang` key), 16 top-level nodes, 110 leaves, `requires` edges on most non-foundational leaves. `uv run trellis --domain snowflake validate` → 0 errors.

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
| 2026-09-14 | 1 survey | 6 outlines identified (docs TOC official) | skeleton header; this table |
| 2026-09-14 | 2 skeleton | 126 nodes / 110 leaves | `validate` 0 errors; commit 495c25c |

## Next action

1. Finish step 2's criterion: write the mapping table "outline heading → leaf id or OUT OF SCOPE (reason)" for every heading of outlines 1–3 below this section; add leaves for any unmapped heading and re-run `validate`.
2. Step 3: declare free corpora (`corpora/snowflake-paper.yaml` with the paper; `corpora/snowflake-docs.yaml` with `chapters:` URLs for the key docs pages) → `trellis ingest` → `triage` → `accept`.
3. Steps 4–8 as in the skill: digest cards leaf by leaf (≤ 3 sonnet agents, disjoint leaf ranges), readings + `clip`, one drill per top-level node linked to `../interviews/companies/snowflake/` problems (e.g. sd03, sd08, sd12) and to work cases from `distilling-work-into-domains`, zh translation, build and `anki-push`.
