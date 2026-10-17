# Task: amazon.amz-pizza-order

- **Leaf id**: `amazon.amz-pizza-order`   **slug**: `amz-pizza-order`   **kind**: problem   **priority**: no priority label
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- 1p3a question bank row `pizza-restaurant-ood` (onsite coding + onsite SD, 5 sources, 2026-04-08..2026-09-24) in /Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/qbank.json
- older reports in research/companies/amazon/catalog/raw/forums.md (grep the keywords): pizza order — crust, size, toppings customisation, compute total
- More detail: `grep -nE 'pizza|Pizza|披萨' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- research/companies/amazon/lld_kit_source/pricing_billing.md §2.4/§2.7 and research/companies/amazon/lld_kit_source/code/pricing_billing.py (PizzaMenu, PizzaBuilder) — our own code, adapt
- LLD leaf amazon.amz-discount-engine (link [[solution-amz-discount-engine]]; the pizza total reuses its discount rules)

## Stages / card ladder

- 1 build a pizza from a data-driven menu and price it · 2 validation (incompatible choices, limits) with a Builder · 3 discounts / combos via the discount engine's rule objects · 4 order of several pizzas + concurrency or persistence
