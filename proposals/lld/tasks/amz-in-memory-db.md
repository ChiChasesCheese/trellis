# Task: amazon.amz-in-memory-db

- **Leaf id**: `amazon.amz-in-memory-db`   **slug**: `amz-in-memory-db`   **kind**: problem   **priority**: no priority label
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- Chi was asked this himself in a past interview and could not finish it — first-hand; LeetCode 2408 Design SQL is the coding-round core (ins/rmv/sel/exp)

## Reuse

- research/companies/amazon/lld_kit_source/in_memory_database.md (104k chars, the full lecture) and research/companies/amazon/lld_kit_source/code/in_memory_database.py + in_memory_database_45min.py — our own, adapt into the bank format. solution.py must fit the gate (120–480 code lines): make it the 45-minute-plus version (typed tables + CRUD + WHERE with 3-valued NULL + ORDER BY + hash join + a tiny SQL parser). Indexes/planner, GROUP BY and transactions go to 扩展与追问 as prose and short snippets — never link a research/ path from a learning page.

## Stages / card ladder

- 1 LC 2408: tables, insert/delete/select by id · 2 typed columns, WHERE predicates with NULL semantics, ORDER BY · 3 JOIN (nested loop → hash) · 4 a SQL text front end (tokenizer + recursive descent); indexes/transactions as follow-ups
