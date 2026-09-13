# ps12 · Hierarchical Task CSV

**Type:** phone screen（technical, unlock-next-part，4 段）· **Stage:** technical screen, ~45 min ·
**Last asked:** 2026-08-25（候选人原始报告日期）
**Frequency:** 1 名候选人第一人称报告 + PracHub 结构化重排（`parse-and-format-arbitrarily-nested-tasks-from-csv`，
id 11064）· **Confidence:** high — 候选人第一人称原始报告（`interview_round: "Technical Screen"`,
`created_at: "2026-08-25"`, `is_ai_assisted: false`）给出的前两行输入样例，与 PracHub 结构化题面
（规则、约束、worked example）逐字吻合，且候选人明确描述的 4-part 划分与结构化题面的规则集完全自洽，
未发现任何矛盾之处。本 session 于 2026-09-03 重新 `curl` 抓取原页面进行了二次核对（详见 Sources），
两次抓取内容一致。

## Context
Stripe's internal task-tracking tool stores work items as an event log rather than a live tree:
every "a task was created" or "a subtask was created" event is appended as one CSV line. To render
the current task hierarchy for a dashboard, you replay this event log and rebuild the forest of
tasks/subtasks, then print it the way a Unix `tree` command would — connectors and all. Subtasks
can nest arbitrarily deep (a subtask can itself have subtasks), and the log can be replayed in one
pass since every parent record is guaranteed to appear before any of its children's records.

## Input (stdin, for `main()`)
```
PART n
timestamp,task,task_id,task_name
timestamp,subtask,parent_id,task_id,task_name
...
```
* `PART n` — `n` ∈ {1,2,3,4}; no other params line (this problem has no numeric knobs).
* Every remaining line is a **valid CSV row** (parse it with the `csv` module — never hand-roll
  `line.split(",")`, since `task_name` may be a quoted field containing commas and
  RFC4180-escaped quotes, e.g. `"say ""hi"" now"` → the name `say "hi" now`).
* A **root** record has exactly 4 fields: `timestamp,task,task_id,task_name`.
* A **child** record has exactly 5 fields: `timestamp,subtask,parent_id,task_id,task_name` — its
  `parent_id` refers to any earlier `task_id` already seen, whether that earlier record was itself
  a root or another child (arbitrary nesting depth).
* `task_id`s are unique across the whole input. `task_name` never contains a newline. `timestamp`
  is a date string (`MM/DD/YYYY` in every known example) — **it is not a sort key**; it is present
  in every record only because it's how the real event log is formatted, and every part of this
  problem ignores it for ordering purposes (see Rules).
* Every parent record is guaranteed to appear in the input **before** any of its children's
  records (a legal replay order — you never have to buffer a child waiting for a not-yet-seen
  parent).
* `0 <= len(lines) <= 200000`.

## Output
A list of formatted tree lines (see Rules per part for exact connector behavior). Root lines have
no connector prefix; every non-root line is `<ancestor prefix><connector><task_id> <task_name>`.

## Rules

### Part 1 — parse roots only
The input for this part contains only root (`task`) records — no `subtask` lines. For each
record, in **input order**, output `task_id + " " + task_name`. (Defensive note: if a stray
`subtask` line ever appears in Part 1 input, it contributes nothing to the output — Part 1's
contract is "roots only", not "ignore subtasks I don't understand yet", but the reference solution
happens to behave that way because it only ever looks at `task` rows.)

### Part 2 — include direct subtasks (uniform connector)
The input now also contains `subtask` records, each naming a **root** as its `parent_id` — this
part's test inputs never nest a subtask under another subtask (that's Part 4). For each root, in
input order, print the root line, then each of its direct subtasks **in input order**, each
prefixed `"├─ "` — **every** subtask line uses the same connector in this part, including the
last one in the list. (This intentionally does not yet distinguish "last child" — that's exactly
what Part 3 fixes. This mirrors how the real interview unlocked the parts: Part 2's grading only
checks that subtasks appear at all, not that the very last one looks different.)

### Part 3 — fix the last subtask's connector
Same input shape as Part 2 (roots + their direct subtasks only, still one level). Now the **last**
subtask in each root's list gets `"└─ "` instead of `"├─ "`; every earlier subtask in that list
still gets `"├─ "`. A root with exactly one subtask gives that subtask `"└─ "` (it's simultaneously
first and last — "last" wins).

### Part 4 — arbitrary nesting depth
Subtasks can now have their own subtasks, to any depth. The rendering rule from Part 3 generalizes
unchanged — a **non-final** child (not the last in its parent's list) gets `"├─ "` and every one of
*its own* descendants is prefixed with an extra `"│  "` per ancestor level that was itself
non-final; a **final** child gets `"└─ "` and its descendants get an extra `"   "` (three spaces)
per ancestor level that was itself final. In other words: exactly the same connector logic a Unix
`tree` command uses. **If your Part 3 implementation was already written as a general recursive
(or iterative-stack) tree render rather than hardcoded to one level, Part 4 requires no code
changes at all** — the two parts are only separated because that's how the real interview unlocked
them, not because the rule itself is different.

## Worked examples
```
# Part 1
lines = [
  "01/01/2025,task,T1,cook dinner",
  "01/01/2025,task,T2,walk the dog",
]
part1(lines) == ["T1 cook dinner", "T2 walk the dog"]

# Part 2 (uniform connector, including the last subtask)
lines = [
  "01/01/2025,task,T1,cook dinner",
  "01/01/2025,subtask,T1,T2,buy groceries",
  "01/01/2025,subtask,T1,T3,prepare meal",
]
part2(lines) == ["T1 cook dinner", "├─ T2 buy groceries", "├─ T3 prepare meal"]
# note: T3 is the LAST subtask but still gets "├─ " in Part 2 -- that's the bug Part 3 fixes.

# Part 3 (last subtask now gets "└─ ") -- this is PracHub's verbatim worked example
lines = [
  "01/01/2025,task,T1,cook dinner",
  "01/01/2025,subtask,T1,T2,buy groceries",
  "01/01/2025,subtask,T1,T3,prepare meal",
]
part3(lines) == ["T1 cook dinner", "├─ T2 buy groceries", "└─ T3 prepare meal"]

# Part 4 (T2 -- a non-final child of T1 -- itself has a child T4)
lines = [
  "01/01/2025,task,T1,cook dinner",
  "01/01/2025,subtask,T1,T2,buy groceries",
  "01/01/2025,subtask,T2,T4,buy milk",
  "01/01/2025,subtask,T1,T3,prepare meal",
]
part4(lines) == [
  "T1 cook dinner",
  "├─ T2 buy groceries",
  "│  └─ T4 buy milk",
  "└─ T3 prepare meal",
]
# T4 is T2's only (hence last) child, so it gets "└─ "; but T2 itself is a NON-final
# child of T1, so T4's line is prefixed with the continuation "│  " (not three spaces).

# Empty input, any part
part1([]) == part2([]) == part3([]) == part4([]) == []

# Quoted CSV field: comma inside the name, and an RFC4180-escaped embedded quote
lines = ['01/01/2025,task,T1,"cook dinner, tonight"', '01/01/2025,task,T2,"say ""hi"" now"']
part1(lines) == ["T1 cook dinner, tonight", 'T2 say "hi" now']
```

## Edge cases hidden tests are known to target
- Part 1: multiple roots in input order (not sorted by `task_id`); a single root; empty input
  (`[] -> []`).
- Part 2/3: a root with **zero** subtasks (no connector lines at all, just the root line); a root
  with **exactly one** subtask (Part 3: that subtask must get `"└─ "`, not `"├─ "`, even though
  it's also "first"); multiple roots, each with their own independent subtask list.
- Part 4: nesting depth of 3+ levels; a root whose *only* child itself has children (so the middle
  level's connector must be `"└─ "` for itself but still contribute `"   "`, not `"│  "`, to its
  own children's ancestor prefix); a tree where a **non-final** branch is itself deep (continuation
  bar `"│  "` must propagate through every level under it, not just the first).
- All parts: **timestamps deliberately out of chronological order relative to desired output
  order** — this is the "fake sort key" trap named in the catalog notes; a correct solution never
  looks at the `timestamp` field for anything except passing it through unused. A solution that
  accidentally sorts records by timestamp before rendering will pass examples where input order and
  timestamp order coincide and silently fail once they diverge — the perf/large test below
  deliberately shuffles timestamps to catch this.
- CSV quoting: a `task_name` containing a literal comma; a `task_name` containing an escaped
  double quote (`""` inside a quoted field); a `task_name` that is itself just plain unquoted text
  (no comma/quote) — the parser must handle both cases identically, not special-case one.
- Deep chains: a single root with a chain of nested single-child subtasks several times deeper
  than Python's default recursion limit (1000) — this rules out a naive recursive implementation
  (`RecursionError`); use an explicit stack instead. Note the ancestor-prefix string grows by 3
  characters per level, so a *fully linear* chain's total output size is `O(depth^2)` — the
  large-`n` perf case therefore uses a **wide** tree (one root, ~2×10^5 direct children) rather
  than a deep one, to stay `O(n)`; depth-safety is checked separately at a moderate (not
  maximal) depth.

## Variants seen in the wild
- The candidate's own report is explicit that they "solved 3 of 4 parts and got partway through
  the last one before running out of time" — Part 4 (arbitrary depth) is reported as the part that
  differentiates candidates under time pressure, consistent with why it's worth its own hidden-test
  category here (deep nesting + the recursion-limit trap) rather than folding it into Part 3.
- PracHub's auto-generated structured shell (built from the same candidate report) exposes a single
  public function `format_task_csv(lines)` with no `PART n` dispatch at all — i.e. the *live*
  interview environment likely only ever showed the candidate the fully-generalized Part 4 contract
  once each part unlocked, rather than four separately-named functions. This problem set's
  `part1..part4` split (mirroring every other `psNN` problem's convention) is a training-harness
  decomposition of that same rule, not evidence that the real platform exposed four distinct
  function names.

## What this tests
skills: S02 (RFC4180-quoted CSV parsing, not hand-rolled split) · S03 (parent/child records
modeled as a tree keyed by `task_id`) · S08 (strict sibling-order preservation — ignoring the
`timestamp` "fake sort key") · S09 (byte-exact tree-connector formatting: `├─ ` vs `└─ ` vs `│  `
vs three spaces, at every ancestor level) · S19 (Part 1→2→3→4 incremental design where a correctly
generalized Part 3 already *is* Part 4).

## Sources
- https://prachub.com/coding-questions/parse-and-format-arbitrarily-nested-tasks-from-csv
  （PracHub, id 11064，`curl` 直接抓取页面 HTML 内嵌的 Next.js payload，2026-09-03 access，本 session
  独立复抓核实，与 `catalog/discovery/2026-09/C_batchB.md` `## C12` 一节记录的抓取内容逐字一致）—
  候选人第一人称原始报告（`content` 字段，`created_at: "2026-08-25T00:00:00"`,
  `interview_round: "Technical Screen"`, `is_ai_assisted: false`）逐字摘录：*"The phone screen problem
  was about parsing a list of tasks and subtasks in CSV format. There were four parts: Parse the
  tasks and output the ID and task name. Parse the subtasks and include them in the output. Change
  the formatting for the last subtask in a list. Tasks can have any number of subtasks, and
  subtasks can have their own subtasks. A straightforward tree traversal. I solved 3 of 4 parts and
  got partway through the last one before running out of time... The input format was something
  like `<timestamp>,<tasks_type>,<task_id>,<task_name>` / `01/01/2025,task,T1,cook dinner` /
  `01/01/2025,subtask,T1,T2,buy groceries`"*
- 同页面 `data-seo-content="question-body"` 结构化题面（同一 `curl` 抓取，同一时间戳）——函数签名
  `format_task_csv(lines)`、连接符规则（`├─ ` / `└─ ` / `│  ` 或三空格）、`task_id + " " + task_name`
  输出格式、约束 `0 <= len(lines) <= 200000`、以及本 problem.md worked examples 中 Part 3 的样例
  （`cook dinner` / `buy groceries` / `prepare meal`）均逐字取自该结构化题面，Part 1/2/4 的样例、
  CSV 引号样例、深度嵌套样例为本套件按已确认规则自行构造的补充用例。
- `catalog/discovery/2026-09/C_batchB.md` `## C12` 一节（本轮排查记录，含失败检索式与交叉验证过程）。

## 面试官会怎么追问
1. "如果 `parent_id` 指向的任务在整个输入里根本不存在（脏数据），你的实现会怎么样？" — 引导候选人
   意识到当前实现假设"父节点保证先于子节点出现"（题面明确保证），但如果放宽这个保证，需要先做一趟
   完整性校验或改成"先收集所有边，最后再统一建树"的两遍扫描。
2. "10 万层的单链子任务，你现在的递归实现会不会栈溢出？" — 这是本题 perf 用例故意覆盖的点：期望候选人
   主动提出用显式栈（迭代 DFS）代替原生递归，而不是等 `RecursionError` 在生产环境爆出来才发现。
3. "如果 `task_id` 出现重复（脏数据/重放了同一条创建事件两次），输出应该怎么处理？" — 检验候选人是否
   意识到题面"task_id 全局唯一"的假设一旦被违反，当前实现会用哪条记录覆盖哪条是未定义行为。
4. "这份数据如果是从 Kafka 之类的消息队列增量到达的（不是一次性给你完整列表），你的树要怎么维护？"
   — 引导到"父节点保证先出现"这条题面保证在真实流式场景下往往不成立，需要额外的"孤儿节点缓冲区"。
5. "如果要支持把整棵树倒过来渲染（子节点在前、父节点在后，比如展示"这个任务被谁依赖"），你的数据
   结构要改哪里？" — 检验是否理解当前 `children` 邻接表和 `parent_id` 反向索引的关系。
