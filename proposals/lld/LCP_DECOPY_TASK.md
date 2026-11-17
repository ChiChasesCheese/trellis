# LeetCode Project leaves: take the workspace's words out of the public vault

The repository is public; LeetCode's workspace files (README, template, provided modules, tests, REFLECTION) are
Premium content and live only in `sources/local/lc-project/workspaces/<slug>/files/`. Some committed leaves copied from
them. `uv run python scripts/lcp_overlap.py --show <slug>` lists every copied line (signatures, dataclass fields,
imports and SQL column definitions are exempt: they are the API the solution must keep). Make each of your projects
print `ok`.

Repository root: `/Users/chiserver/sessions/trellis`. Edit only the leaf's own files:
`vault/domains/low-level-design/problems/lcp-<slug>/`, `readings/problems/solution-lcp-<slug>.md`,
`drills/problems/design-lcp-<slug>.md`, `cards/lcproject/lcp-<slug>-*.md`. No git, no other agents. Python 3.11 runs go
through `uv run --no-project --python 3.11 --with pytest …` in /tmp; never touch the repo `.venv`.

## How to rewrite

- **Docstrings, comments, error texts** that match: reword in your own Chinese or English. Keep an error string only if
  a public test asserts it (then it is API; tell me which).
- **Provided helpers** (an inventory, a location service, a fake clock, a fake database) that our solution or tests
  re-implement: write our own version — our own internal names, structure and comments, the same public methods. A
  formula (haversine) may stay, written your way.
- **Repair projects' `starter.py`**: it is our rewrite of the broken service, with the same API and the same *kinds* of
  defects as the workspace code, not a copy of it. Rewrite its body so it reads as our code, keeping each defect.
- **README examples and test data** (names, ids, cities, amounts, sample prompts): replace with our own values, then
  recompute every expected output by running our solution. Never edit an expected value by hand.
- **The article** embeds `solution.py`: after editing the code, rerun `uv run python scripts/lld_embed_code.py` (or the
  way the article's code block was produced; check its header) so the two agree, and fix any prose example you changed.

## Checks, all must pass

1. `uv run python scripts/lcp_overlap.py <slug>` prints `ok`.
2. Our own suite passes on 3.11; the official public tests still pass with `solution.py` copied into a /tmp copy of
   the workspace under the template's file name (the same way LCP_AGENT.md §4 says).
3. For a repair project, the starter still fails the tests that pin each defect (run it; list which fail).
4. `uv run python scripts/check_lld_problems.py --branch lcproject lcproject.lcp-<slug>`,
   `python3 scripts/plain_style.py <article and cards>`, `python3 scripts/phone_diagrams.py <article and cards>`.

Report per project: copied lines before → after, what you rewrote, the test results, and anything you kept as API.

## Defects found in earlier batches

- A last hand edit after the test run left an `IndentationError` in `solution.py` and the article: run every check
  **after the last edit**, and re-embed the article code with `lld_embed_code.py` rather than editing it by hand.
- Do not start database servers (mongod, postgres) for a check; where the official tests need one, say so in the report.
- Expected values in tests come from running our solution on the new data, never set by hand.
- Table names and column layout are API (a hidden test may open the database file): never rename them to pass the
  overlap check; `lcp_overlap.py` exempts table definitions.
