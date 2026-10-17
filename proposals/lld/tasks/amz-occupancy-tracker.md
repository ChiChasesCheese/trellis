# Task: amazon.amz-occupancy-tracker

- **Leaf id**: `amazon.amz-occupancy-tracker`   **slug**: `amz-occupancy-tracker`   **kind**: problem   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: US L4 NG offer — 'Design a system to track how many people are in the office at any given time' (data model + timestamp queries)
- More detail: `grep -nE 'occupancy|people are in the office|人数' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- research/companies/amazon/lld_kit_source/occupancy_tracker.md and research/companies/amazon/lld_kit_source/code/occupancy_tracker.py — adapt

## Stages / card ladder

- 1 enter/exit events, current count · 2 count at any past time (prefix sums + binary search) · 3 per-floor / per-building, late or duplicate events · 4 the same model in SQL; append-only segment tree for many queries
