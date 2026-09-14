# Kafka — BUILD

> Durable record for skill `building-study-domains` (`.claude/skills/building-study-domains/SKILL.md`), started 2026-09-14 for the deepening pass.
> The domain was built earlier from corpus `kafka-2e` (Kafka权威指南 第 2 版, commercial, `lang: zh`); see PR #22.

## State (2026-09-14, `uv run trellis --domain kafka stats` / `validate`)

| Measure | Value | Skill criterion |
|---|---|---|
| Nodes / leaves | 79 / 66 | — |
| Cards | 340 (all from `kafka-2e`) | every leaf has cards → **4 leaves without cards**: `producer.schema-registry`, `consumer.kafka4-protocol-changes`, `monitoring.observability-otel`, `practice.positioning` |
| Readings | 88, link coverage 100% | ≥ 70% ✓ |
| Readable sources | **0 / 66 leaves** (all readings point at the book home page) | every leaf has a readable source ✗ |
| Drills | **0** | ≥ 1 per top-level node (13) ✗ |
| Validate | 0 errors, 2 warnings | 0 errors ✓ |

Field cross-check (ADR 0002): the skeleton was seeded from one book's outline. It has not yet been compared against the Apache Kafka documentation TOC, the KIP index, or interview question sets.

## Ledger

| Date | Step | Result | Evidence |
|---|---|---|---|
| 2026-09-14 | 5 readable sources | agent researched Apache docs / KIP / Confluent pages but stalled (600 s watchdog, network) before writing any file | no `kafka-web-*` readings exist |

## Next action

1. Step 5: for each of the 66 leaves write `readings/kafka-web-<slug>.md` pointing at a free mechanism-level page (Apache Kafka docs section, KIP on cwiki, Confluent docs or engineering blog); check `trellis/links.py` for what counts as readable; `trellis --domain kafka clip`; done when the "no archived, readable source" warning is gone.
2. Step 1–2 cross-check: map the Apache Kafka documentation TOC and KIP index onto the skeleton; add leaves for unmapped headings (KRaft, tiered storage, share groups / queues).
3. Step 4: cards for the 4 uncarded leaves via `trellis scaffold` → `trellis import` (Chinese, self-contained).
4. Step 6: one drill per top-level node (13) — predict / debug / explain; link to `../interviews/companies/snowflake/` pc03, sd05, sd18 and to work cases (pricing events) from `distilling-work-into-domains`.
