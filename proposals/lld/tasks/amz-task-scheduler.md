# Task: amazon.amz-task-scheduler

- **Leaf id**: `amazon.amz-task-scheduler`   **slug**: `amz-task-scheduler`   **kind**: cards-only   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: task/job scheduler 2× SDE I, 1× SDE II+; whiteboard, changing requirements to probe OS knowledge (threads, blocking)
- More detail: `grep -nE '[Tt]ask scheduler|job scheduler' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- bank leaf problems.components.task-scheduler: [[solution-task-scheduler]]

## Stages / card ladder

- cards: delayed vs periodic tasks · heap + condition variable · cancel · worker pool · blocking task / OS follow-ups
