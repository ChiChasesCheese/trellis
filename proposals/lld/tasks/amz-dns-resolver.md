# Task: amazon.amz-dns-resolver

- **Leaf id**: `amazon.amz-dns-resolver`   **slug**: `amz-dns-resolver`   **kind**: cards-only   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: SDE II+ — DNS resolver with health checks, TTL, fast reads
- More detail: `grep -nE 'DNS' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- bank leaf problems.components.ttl-cache: [[solution-ttl-cache]]

## Stages / card ladder

- cards: resolver objects · TTL cache with lazy + active expiry · upstream health check and failover · read-mostly concurrency (copy-on-write / RW lock) · negative caching
