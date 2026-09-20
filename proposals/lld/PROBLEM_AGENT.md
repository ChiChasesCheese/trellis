# Writing one low-level design problem — instructions for one agent

You are given a list of **problem leaves** of the `low-level-design` domain, e.g.
`problems.machines.parking-lot`. For each you produce working Python, a solution article, a drill,
cards and source readings, then pass one gate. Repository root: `/Users/chizhang/Code/trellis`. Run
every command from there, one plain command at a time. Do not run git. Do not start other agents.
Touch only the files named below for your own leaves. `WebSearch` is exhausted for this session:
use `WebFetch` on the URLs in your task brief and `gh api` for GitHub; if a page refuses the fetch,
move on — never narrate that in the article.

`<slug>` is the last segment of the leaf id (`parking-lot`). Your task brief
(`proposals/lld/tasks/<slug>.md`) gives the title, scope, the concept leaves it stands on, and the
sources the survey found. **Everything a learner reads is Chinese; all code is Python.**

## Resume rule (do this first, for every leaf)

Run `uv run python scripts/check_lld_problems.py <leaf>`. If it prints `ok`, skip the leaf. Otherwise
its output lists exactly what is missing — do only that. Never rewrite a file that already passes.

## The bar

The reader is a senior engineer preparing for low-level design / machine-coding rounds in Python.
They have seen the Java-flavoured answers in the popular repositories. **Yours must be better than
those**: a design argued against real alternatives, code that actually runs and is tested, written
the way a strong Python engineer writes it — not Java transliterated. A machine-coding round adds
requirements in stages and grades extensibility, so the design must show *where the next
requirement lands* without rewriting what exists.

Pythonic means: `@dataclass` (with `frozen=True`/`slots=True` where apt) for data, `Enum` for finite
states, `typing.Protocol` or `abc.ABC` only where there are really several implementations, plain
functions for one-method strategies unless they carry state, attributes and `@property` instead of
getters and setters, exceptions from a small custom hierarchy for failure paths, `datetime` and an
**injected clock** instead of `time.time()` inside logic, `decimal.Decimal` or integer minor units for
money, `threading.Lock` where the brief asks for thread safety (and say honestly what the GIL does
and does not give you). No singletons via `__new__`, no `get_x()`/`set_x()`, no class that only holds
a `main`, no interface with exactly one implementation "for extensibility".

**Three habits the first pilot had to fix — do not repeat them.** (1) Never return an internal
mutable collection from a property or getter: hand out a snapshot (a tuple, a frozen mapping, a
count computed under the lock). (2) An observer event carries *what happened* (a small frozen
dataclass), so subscribers update themselves from the event instead of reaching back into the
subject's storage without its lock. (3) A class that only forwards one call to another object is
a Java habit: give it a responsibility or delete it, and say which in the article.

**Length is cut by removing scope, never by compressing prose.** The gate measures lines of *code*,
so shortening a docstring buys you nothing: if the solution runs long, drop a stage-4 extra and
describe it in 扩展与追问 instead. Never delete a read-only accessor a test or a reader needs.
Landing a line under the cap means the next edit breaks the gate: aim for 250–400 and stop adding.

**A test asserts behaviour, never shape.** `assert not hasattr(obj, "cards")` and its relatives
fail a correct answer that happens to name something the same way. Pin what the design promises —
the operation is atomic, the container shrank, the invariant held — and leave "this must not be
reachable" to the article and the card. Asserting the exact set of public names is fine, because
that is a contract you designed.

**A test never reads a private attribute.** `starter.py` is filled in by a learner who may pick a
different internal representation, so a test that asserts on `_something` fails a correct answer.
When an invariant is only visible inside (a container shrank, a pointer was repaired), expose it as
a tiny read-only property on the class — `row_count`, `bucket_count` — mirror it in `starter.py`,
and assert on that.

**A defect you find is a defect you fix.** The second pilot documented, in a docstring, a call
order that crashed its LFU policy, and never noticed that emptied frequency buckets were kept
forever. Repair the invariant and add a regression test — never ship a described landmine. For
every container in your solution ask: what removes an entry when it empties, expires or is
released? Unbounded growth in a component whose job is bounded memory is a failed answer.

## 1. The code — `vault/domains/low-level-design/problems/<slug>/`

- `solution.py` — the reference solution. **120–480 lines of code** — blank lines, comments and docstrings do not count, so write the
  Chinese prose your reader needs and spend the budget on design, not on words; aim for 250–400
  lines of code and stop adding scope. Standard library only, Python 3.12, fully
  type-annotated, a Chinese module docstring that states the design in five lines, Chinese
  docstrings and comments (identifiers stay English). At least three top-level classes. No `print`
  in library code; an `if __name__ == "__main__":` demo at the bottom is welcome.
- `starter.py` — **the same public API** (same class names, method signatures, enums, dataclasses,
  exceptions) with every method body `raise NotImplementedError`. It must import cleanly. This is what
  the learner fills in during a drill.
- `test_<slug with underscores>.py` — a pytest suite, at least twelve tests, covering every stage of
  the requirements, the failure paths, and the edge cases a hidden test would target. It selects the
  implementation with an environment variable, exactly like this at the top of the file:

  ```python
  import importlib
  import os

  impl = importlib.import_module(os.environ.get("IMPL", "solution"))
  ```

  and then uses `impl.ParkingLot(...)`, never `from solution import …`. Put an empty `conftest.py`
  beside it so pytest puts the folder on `sys.path`. Tests must be deterministic: inject the clock,
  seed any randomness, and for thread-safety tests use real threads with a barrier and assert an
  invariant (no oversell, counts add up), not timing.
- Check: `IMPL=solution uv run --with pytest python -m pytest vault/domains/low-level-design/problems/<slug> -q -p no:cacheprovider`
  must pass, and the same with `IMPL=starter` must fail.

## 2. The solution article — `vault/domains/low-level-design/readings/problems/solution-<slug>.md`

```
---
nodes: [<leaf id>]
tags: [solution]
---
# 设计题解：<中文题名>（<English name>）
```

No `url:` key — this article is written here. Chinese prose; terms of art in English in full-width
parentheses on first use, e.g. 策略模式（Strategy）; full-width punctuation. At least 8,000 characters
outside code blocks. Exactly these `##` sections, in this order:

1. `## 题目与澄清` — the prompt as an interviewer says it; the clarifying questions worth asking and
   what each answer changes in the design; what is out of scope.
2. `## 需求与分级` — requirements as the stages a machine-coding round reveals them: 第 1 关 (the core
   flow), 第 2 关, 第 3 关, 第 4 关 (usually concurrency, persistence or a new policy). Say which stage each
   part of the design exists for.
3. `## 核心对象与职责` — each class with its single responsibility and the invariant it owns; the
   relationships (composition vs association, who owns whose lifetime); a ```mermaid `classDiagram`.
4. `## 关键设计决策` — at least three `###` decisions, the hard ones for *this* problem. Each: the
   problem stated sharply → at least two real options, in Python, with what each costs → the choice
   and why → which pattern this is, or why no pattern is needed. Include at least one decision where
   the right answer is the simpler one and a pattern is refused.
5. `## 代码走读` — put the full solution in a managed block and nothing between the markers:

   ```
   %% code:begin solution.py %%
   %% code:end %%
   ```

   then run `uv run python scripts/lld_embed_code.py <slug>`, which fills it from the tested file.
   Around it, walk through the three or four places where the design decisions show up in the code.
   You may add further blocks for a single class: `%% code:begin solution.py ParkingLot %%`.
6. `## 测试与自检` — what the tests pin down, the invariants worth asserting, and how to demo the
   code to an interviewer in two minutes.
7. `## 扩展与追问` — the follow-ups interviewers add, grouped: 新需求 / 并发与线程安全 / 持久化与规模. For
   each: what changes, in which class, and what stays untouched — that is the evidence the design
   was extensible.
8. `## 常见错误` — the mistakes candidates actually make on this problem, including the Java-isms
   that look wrong in Python.
9. `## 45 分钟怎么分配` — a minute-by-minute plan: clarify, entities, API, code the core, test, extend;
   what to say aloud at each step; what to cut if time runs short.
10. `## 来源与延伸` — at least three links: what each source adds, and where this article disagrees
    with it. Commercial sites are linked, never quoted.

Link the concept leaves it stands on with wikilinks to their map notes by node id and title, e.g.
`[[patterns.strategy|策略模式与可替换算法（Strategy）]]` (your task brief lists them). The article speaks
to the learner, never about how it was written: no mention of these instructions, of fetching, or of
pages you could not reach.

## 3. Source readings (pointers)

One file per source you actually used, at least two:
`vault/domains/low-level-design/readings/problems/src-<site>-<slug>.md`

```
---
nodes: [<leaf id>]
url: https://…
tags: [no-archive]      # REQUIRED for commercial sites; omit for MIT/CC/GPL repositories, docs.python.org, papers
---
# <The page's own title>
值得读：<两三句中文：它讲了什么、用什么语言、哪里和本题解不同>
```

Commercial sites (always `no-archive`): hellointerview.com, educative.io, designgurus.io,
algomaster.io, codemia.io, workat.tech, refactoring.guru, leetcode.com, tryexponent.com, udemy.com.
**Mirrors of paid material are not sources**: `tssovi/grokking-the-object-oriented-design-interview`
republishes a paid course — read it to orient yourself if you like, never link it. Repositories with
no LICENSE file may be linked (a link is not a copy) but tag them `no-archive` too. Note names must
be unique in the whole vault, so keep the `src-<site>-<slug>` pattern.

## 4. Cards — six to eight, Chinese, self-contained

1. `uv run trellis grow --leaf low-level-design:<leaf id> --count 8 -o proposals/lld/<slug>.prompt.md`
2. Read that prompt: it carries the card format and this domain's language rules. Follow it.
3. Write `proposals/lld/<slug>.cards.json`, distilled from **your own article and code**. The mix: the
   entity/responsibility split and the invariant that decides it; the central design decision and the
   option refused; the pattern used and the Python form it takes; the data structure that makes the
   key operation fast; the thread-safety question; the extension that proves the design; the most
   common mistake. Code in cards is Python, ≤ 15 lines, and must parse.
4. `uv run trellis grow --import proposals/lld/<slug>.cards.json --leaf low-level-design:<leaf id>`

Every question must make sense alone, months later: name the system ("在停车场设计里，…"); never say
"本文", "上面", "这个设计", "上一张卡". Card ids start with `problems-<slug>-`. No translation sections:
this domain is Chinese-native.

## 5. The drill — `vault/domains/low-level-design/drills/problems/design-<slug>.md`

If your task brief says a drill already exists for this problem, rewrite that file in this format
(keep its file name) instead of creating a second one.

```
---
nodes: [<leaf id>, <the concept leaves it exercises>]
tags: [problem]
---
# Drill：<中文题名>

<两三句：场景与规模。>

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：…
- 第 2 关（约 15 分钟）：…
- 第 3 关（约 15 分钟）：…
- 第 4 关（选做）：…

**怎么练**：把 `vault/domains/low-level-design/problems/<slug>/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/<slug> -q`。

**评分点**
- <一个强答案会做到什么>（[[problems-<slug>-…]]、[[problems-<slug>-…]]）
- …至少四条，每条链接承载该知识的卡片…

**题解**：[[solution-<slug>]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
```

Grading-point links must be real card ids (yours, or existing concept cards).

## 6. Card order

Write `proposals/steps/low-level-design/problems-<slug>.json` as
`{"<leaf id>": ["<card id shown first>", …]}` with every card of the leaf exactly once, then
`uv run trellis --domain low-level-design steps --import proposals/steps/low-level-design/problems-<slug>.json`.

## 7. The gate

`uv run python scripts/check_lld_problems.py <leaf id>` must print `ok` (it runs your tests against
both `solution` and `starter`), and `uv run trellis --domain low-level-design validate` must show no
error naming one of your files (other agents work in parallel; ignore errors about files that are
not yours).

## Before you report

Re-read the article and the code once as a skeptical interviewer. Does the code do what the article
says? Is every class earning its place, or is one of them a Java habit? Would adding the stage-4
requirement really leave the earlier classes untouched? Are the tests asserting behaviour or just
calling methods? Fix what you find.

## Report

One line per leaf: `<leaf id>: ok` copied from the gate, the number of tests, the solution's line
count, the article's character count, the number of cards — and **the three things in your design
you are least sure of**, so they can be checked.
