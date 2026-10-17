# Task: amazon.amz-rate-limiter

- **Leaf id**: `amazon.amz-rate-limiter`   **slug**: `amz-rate-limiter`   **kind**: cards-only   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: rate limiter asked 3× SDE I / 7× SDE II+ — LLD in C++ OOP (SDE I S3 Glacier), fixed vs sliding window vs token bucket, Redis, distributed consistency, central leasing service
- More detail: `grep -nE 'rate limiter|Rate limiter|限流' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- bank leaf problems.components.rate-limiter: [[solution-rate-limiter]] (do not re-teach; cards are the Amazon follow-up layer)

## Stages / card ladder

- cards: what to build in 45 min · window algorithm choice with numbers · per-user isolation and memory bound · distributed version (Redis counter vs leasing) · the follow-up that breaks a naive design
