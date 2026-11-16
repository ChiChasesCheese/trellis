# LeetCode Project (`lcproject` branch of low-level-design) — instructions for one agent

LeetCode Project (leetcode.com/project, launched 2026-10) is a set of 45–75 minute projects done **together with a coding
agent in a real workspace**: build a component from an interface, repair a broken service, or handle a production
incident. Every project is graded on hidden tests plus how the candidate directs and verifies the agent. The `lcproject`
branch of `skeleton/low-level-design.yaml` holds one leaf per project. In Anki the cards become the deck
`低层设计（LLD）::28 LeetCode Project（实战项目）`.

Chi does not want to read answers first. **Every card of this branch is an answer card**: he writes his own answer to the
front into the card's Note field, then turns the card; a daily job grades the Note against the card's 评分点 and sends
what he missed back to the knowledge tree. So the back of a card is a grading key, not an essay.

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
6. **The cards: 8–10 answer cards plus one per REFLECTION question, every one with a `step`, in this ladder.** Tag every card `作答`.

   | step | the front asks (a concrete situation, then one question) | the back |
   |---|---|---|
   | 1 | the project in three sentences, then 「开工前你会先定下哪几条规则？」 | the 4–6 rules a hidden test pins and a careless reading misses |
   | 2 | 「要存哪些状态？哪条不变量最要紧？」 | the state, the structure for each part, the invariant, and what breaks it |
   | 3 | 「你给编程智能体的第一条指令写什么？哪些决定你自己留着？怎么验证它的改动？」 | decomposition, the context it needs (the rules, the failing test), the decisions kept, the verification cadence |
   | 4–7 | one hard decision each: a race between two calls, a retried request, a batch that fails half-way, a tie, a boundary value, an error that must win over another | what goes wrong, the mechanism that prevents it, the cost of the other option |
   | 8 | a 6–15 line excerpt with one realistic defect (from `starter.py` for a repair project, or plausible agent output for a build project): 「哪里错了？怎么修？哪个测试能抓住它？」 | the defect, the fix, the test |
   | 9 | 「只能写五个测试，你写哪五个？」 | the five, each with the rule it pins |
   | 10 (optional) | the stage-4 follow-up an interviewer adds | where it lands in the design and what stays untouched |
   | 11+ | one card per question in `REFLECTION.essay`, restated in Chinese | what a strong written answer covers |

   The back of every card has exactly this shape:

   ```
   **评分点**
   - <短语>：<为什么，一句>
   - …（3–6 条，按重要性排序；每条都是 Chi 的答案里可以「有或没有」的一件事）

   <details class="pt"><summary>参考答案</summary>

   <≤ 220 个汉字的完整作答，可带一个 ≤ 15 行的 Python 代码块>

   </details>

   **知识点：** <1–3 个 LLD 叶子的中文标题，用「、」隔开>
   ```

   The 评分点 are what the daily grader checks a written answer against, so each must be decidable from a short answer:
   「说出用一把锁保护"检查余额+扣款"整个复合操作」 is gradable; 「理解并发」 is not. The 知识点 line names existing
   leaves of `skeleton/low-level-design.yaml` by their title (the knowledge an answer that missed a 评分点 should go back
   to); `points.json` (below) carries their ids.
   Every front is self-contained and names the system (「在 LLM 网关限流器里，…」); never 「本题」「上一张卡」.
7. **`points.json`** beside the code: the project's exam points, which the grader maps misses through.
   `[{"point": "<中文短语>", "cards": ["<card id>", …], "leaves": ["<leaf id>", …]}]`, 5–10 points, every card in at least
   one point, every leaf id real (`grep -n "id: <leaf id>$" skeleton/low-level-design.yaml`).
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
