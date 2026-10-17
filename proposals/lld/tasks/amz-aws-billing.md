# Task: amazon.amz-aws-billing

- **Leaf id**: `amazon.amz-aws-billing`   **slug**: `amz-aws-billing`   **kind**: problem   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: SDE I AWS loop (2026-08, offer): 'Design a billing service for AWS for a single user where the usage and rate of all the services used are given' — best round, many follow-ups
- More detail: `grep -nE 'billing service|Billing|账单' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- research/companies/amazon/lld_kit_source/pricing_billing.md §2.5/§2.6 and code RatePlan / BillingService — adapt
- link [[solution-amz-discount-engine]] for the Money value object

## Stages / card ladder

- 1 usage × rate per service, monthly bill · 2 tiered pricing (marginal, not whole) and free tier · 3 duplicate usage records (at-least-once delivery → idempotency) · 4 multiple currencies or mid-month price change
