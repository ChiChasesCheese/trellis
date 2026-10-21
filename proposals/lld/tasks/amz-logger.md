# Task: amazon.amz-logger

- **Leaf id**: `amazon.amz-logger`   **slug**: `amz-logger`   **kind**: cards-only   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: logger / logging framework 1× SDE I, 4× SDE II+; follow-ups: several message formats, string parsing
- More detail: `grep -nE '[Ll]ogger|logging framework' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- bank leaf problems.components.logger: [[solution-logger]]

## Stages / card ladder

- cards: core objects · formatter/appender split · levels and routing · slow sink must not block (async queue, back-pressure) · parsing log lines follow-up
