# LeetCode Project (`lcproject` branch of low-level-design) — instructions for one agent

LeetCode Project (leetcode.com/project, launched 2026-10) is a set of 45–75 minute projects done **together with a coding
agent in a real workspace**: build a component from an interface, repair a broken service, or handle a production
incident. Every project is graded on hidden tests plus how the candidate directs and verifies the agent. The `lcproject`
branch of `skeleton/low-level-design.yaml` holds one leaf per project. In Anki the cards become the deck
`低层设计（LLD）::28 LeetCode Project（实战项目）`.

Chi learns these like vocabulary (2026-11-16): most of a project is ten-second tap cards, one per fine-grained point,
written in a later pass from your `points.json` (proposals/lld/LCP_QUICK_AGENT.md); a miss sends him back to the
point's knowledge-tree leaves. Your leaf adds 3–5 longer synthesis cards (tag 作答): he answers in his head, turns, and
grades himself against a dense, structured back with a diagram and code. No typing anywhere.

> **`proposals/WRITING_RULES.md` overrides everything below**: textbook voice, cause → effect, self-contained, no
> provenance on a learning page. `scripts/plain_style.py` enforces part of it inside the gate.

**Follow `proposals/lld/PROBLEM_AGENT.md` in full, with the changes below. Where the two disagree, this file wins.**

## Changes to PROBLEM_AGENT.md

0. **Paths and tools.** The repository root is `/Users/chiserver/sessions/trellis` (not `/Users/chizhang/Code/trellis`).
   Run every command from there, one plain command at a time. `WebSearch` and `WebFetch` are available. leetcode.com
   refuses most fetches; do not retry it more than once.
1. **Leaf ids and slugs.** Leaves are `lcproject.lcp-<name>`; the slug is `lcp-<name>`; the folder
   `vault/domains/low-level-design/problems/lcp-<name>/`, the article `readings/problems/solution-lcp-<name>.md`, the
   drill `drills/problems/design-lcp-<name>.md`. **Card ids start with `<slug>-`.** The gate is
   `uv run python scripts/check_lld_problems.py --branch lcproject <leaf id>`; the article's last section is `## 延伸阅读`.
2. **The real workspace is your source.** `sources/local/lc-project/workspaces/<name>/files/` holds the project's whole
   workspace as LeetCode hands it to the candidate: `README.md` (the exact product rules), `OVERVIEW.md`, the template
   file(s) to fill in, the public tests, `REFLECTION.essay` (written questions the candidate must answer, JSON), and
   whatever else the project ships (a server, an HTTP adapter, migrations, a database, buggy code to repair). Read every
   file before designing anything. `export.log` beside it lists the file tree as the IDE showed it. The hidden tests
   are not available: the README and the public tests are the contract, and your own tests go beyond them.
3. **LeetCode's material stays local.** The repository is public and these files are LeetCode Premium content: never
   copy README text, template code or test code into the vault, and never commit anything under `sources/local/`.
   Everything in `vault/` is yours: the rules restated in your own words in Chinese, your own solution, your own tests.
   The product rules go into `starter.py`'s module docstring, numbered and testable (the README's contract restated:
   inputs, outputs, error precedence, boundaries, rounding, ordering, what a failure leaves behind), and into the
   article's `## 题目与澄清`. `starter.py` keeps the workspace's public API (class, method and function names and
   signatures, return shapes) so the solution drops into the real workspace unchanged.
4. **Prove the solution against the official tests.** Make a scratch copy:
   `cp -R sources/local/lc-project/workspaces/<name>/files /tmp/lcp-<name>-official`, put your `solution.py` in it under
   the template's file name (e.g. `rate_limiter.py`; adapt nothing but the import surface), and run the public tests the
   way the README says (`python3 -m pytest` or `python3 -m unittest`) with `uv run --with pytest` and any dependency in
   `requirements.txt` that the tests need. Every public test must pass; paste the summary line into your report. Your own
   suite in the vault (≥ 12 tests, deterministic, real threads with a barrier where the README asks for thread safety)
   covers every README rule, including the ones the public tests skip. For a *repair* project, `starter.py` is your own
   rewrite of the broken service's behaviour (same API, the same kinds of defects the workspace code has, written by you,
   not copied) and `solution.py` the fixed one; for an *incident* project add an idempotent data-repair function with a
   dry-run mode, and test it run twice. Where the workspace uses PostgreSQL, MongoDB or an ORM, the vault version uses
   `sqlite3` and the article says what differs.
5. **Python 3.11.** LeetCode runs these in Python 3.11: no `type X = …`, no PEP 695 generics, no 3.12-only APIs.
6. **The long cards: 3–4 synthesis cards only** (Chi, 2026-11-16: most study is ten-second tap cards, written in a
   separate pass from your `points.json`; a few longer cards are welcome). Tag them `作答`, give each a `step`:
   step 1 「开工前你会先定下哪几条规则？」 (the 4–6 rules a hidden test pins), step 2 「要存哪些状态？哪条不变量最要紧？」,
   then one card per REFLECTION question, asked as a concrete situation in your own words. Chi answers them in his
   head and grades himself, so the 评分点 are short phrases he can tick off at a glance.

   The back of every synthesis card has this layout (Chi, 2026-11-16: dense, structured, a picture, code over prose,
   no filler; the layout itself shows the outline):

   ```
   **<结论：一句话，≤ 30 字>**

   - **<短语>**：<为什么或怎么做，一句>
   - …（3–6 条，按重要性；每条是 Chi 想答案时可以打勾的一件事）

   ```mermaid
   flowchart TB / stateDiagram-v2 / sequenceDiagram …（流程、状态或结构，≤ 8 个节点，手机竖屏放得下）
   ```

   ```python
   # ≤ 15 行：这件事的最小正确代码，名字和参考解一致
   ```

   <details class="pt"><summary>延伸</summary>一两句：规模变大、换成数据库或分布式时怎么变。</details>

   **知识点：** <1–3 个 LLD 叶子的中文标题，用「、」隔开>
   ```

   The diagram or the code may be left out only when the point has no structure or no code; most cards have both. No
   paragraph of prose longer than two lines anywhere on the card. The mermaid block follows rule 12 of
   WRITING_RULES (`python3 scripts/phone_diagrams.py` passes).
   Every front is self-contained and names the system (「在 LLM 网关限流器里，…」); never 「本题」「上一张卡」.
7. **`points.json`** beside the code: the project's exam points, fine-grained, because each becomes one ten-second
   card. `[{"point": "<中文短语>", "cards": ["<card id>", …], "leaves": ["<leaf id>", …]}]`, 15–40 points: every README
   rule, boundary and error-precedence choice, each defect of a repair project, each mechanism of the solution, each
   decision with its refused alternative, the agent-workflow habits this project needs. `cards` may be empty; every
   leaf id real (`grep -n "id: <leaf id>$" skeleton/low-level-design.yaml`). The drill's 评分点 link only real cards.
8. **The drill** follows PROBLEM_AGENT.md §5, and adds a `**和编程智能体一起练**` paragraph: open `starter.py` with a coding
   agent (Claude Code or the workspace agent), give it the rules and one failing test at a time, keep the design
   decisions yourself, and run the tests after every change.
9. **Reuse what the repository has.** A classic problem of the same name (`problems/rate-limiter`, `pub-sub`,
   `ttl-cache` …) is linked by wikilink and its code may be adapted; the LeetCode project usually adds the parts the
   classic one skips (per-key isolation, statistics, snapshots, atomic batches, idempotency, HTTP contracts).

## Defects found in earlier branches (each is a rule)

- 「本题」「这道题」「上一张卡」 on a card: name the system every time.
- Process talk (「我验证过」「对拍通过」「推断」「重建」) on a learning page: show the input and output instead.
- Numbers typed from memory: every bound, example output and count is computed by running code.
- A 评分点 that only a long essay could satisfy: split it or cut it.

## Report (≤ 12 lines)

Per leaf: the gate line, tests, solution code lines, article characters, cards — and the three claims or rules you are
least sure of (especially product rules you had to decide that the hidden tests might decide differently). Do not run
git; do not start agents; touch only your leaves' files.

## Defects found in this branch (each is a rule)

- `uv run --python 3.11` inside the repository replaces the project's `.venv`. Run 3.11 with
  `UV_PROJECT_ENVIRONMENT=/tmp/venv311 uv run --python 3.11 …` or `uv run --no-project --python 3.11 --with pytest …`.
- A REFLECTION card that translates LeetCode's question (the essay file carries an official Chinese version) copies
  their text into a public file. Ask it as a concrete situation in your own words ("流量涨十倍时…", "开四个进程时…")
  that needs the same answer.
- State that remembers "the parameters of the last call" must be per key: a sweep, an eviction or a refill that reads
  the parameters of whichever request triggered it applies one client's limits to every other client.
- A workspace that audits SQL by substring ("the request value must not appear in any statement") also catches
  constants you spelled inline when a request can send the same value ('active' in `IN ('active','termed')`), and even
  placeholder names or aliases that contain it (`$active`). Bind constants as parameters under neutral names. Read the
  workspace's own test fixtures for audits like this before writing SQL.
- When running the official tests, the tests often compare against the workspace's own classes (`models.Decision`,
  `models.ServiceError`): import those instead of your copies, and put the solution into the file the tests import.
