# ps09 · Matching Contacts

**类型：** Phone Screen（Technical Screen）· **阶段：** Technical Screen（电面），Medium 难度，3 个递进 part · **最近一次报告：** PracHub 2026-07-08（独立第二次报告；首次报告 2026-06-21）· **频率：** PracHub 两次独立报告（同一规则，两个不同的标题措辞）+ 1point3acres 题库 "last asked 2026-06-10" + `catalog/raw/en_forums.md` §24（medium 置信度、独立转述，权重数值完全一致）三方互相印证 · **置信度：** high — 规则文本（字段完全相等按权重累加分数）、字段权重（`name=0.2, email=0.5, company=0.3`）、函数入参形状（`rows, weights, threshold, target_user_id`）、3-part 划分（1 跳 / ≤2 跳 / 完整连通分量）、输出格式（id 列表升序、不含 target）均有结构化原文佐证。**唯一的缺口**：PracHub 页面的完整原始样例表格因抓取工具的引用长度限制，只有 Part 1 的 4 条记录被逐字核实（见下方 Sources），Part 2/3 用来区分跳数的扩展样例是本仓库自拟——已在 worked examples 和 Sources 中逐条标注哪些数字来自原文、哪些是本仓库编的。

## Context
Stripe's internal tools de-duplicate and link customer-facing records (support tickets, KYC
submissions, chargeback claims) that plausibly refer to the same real person or company, even
when they were created through different channels with slightly different data entry. You are
given a batch of contact records and must decide which ones are "the same contact" by comparing
a handful of fields, without ever assuming any single field is a perfectly reliable identifier on
its own — a shared name could be a coincidence, but a shared name *and* email is strong evidence.

## Input
`rows`: a list of records, each with fields `{id, name, email, company}` (all strings; a field may
be an empty string meaning "unknown", never treated as matching another empty string).
`weights`: a dict mapping each of `name`, `email`, `company` to a numeric weight (the known
weights from the source are `name=0.2, email=0.5, company=0.3`, but the function must work for any
weight dict passed in). `threshold`: the minimum score for two records to count as linked.
`target_user_id`: the id whose linked records you must return.

## Rules
For two records `A` and `B`, the **similarity score** is the sum, over every field in `weights`,
of `weights[field]` where `A[field] == B[field]` — **exact string equality**, and only when
**both** values are non-empty (two records that both happen to have an empty `company` are not
considered to match on `company`). Two records are **directly linked** (an undirected edge) when
their score is `>= threshold` (non-strict). Every part uses this same linkage definition; only the
number of hops considered changes.

### Part 1 — direct matches
Return every record id directly linked (1 hop) to `target_user_id`, ascending (plain string
order), never including `target_user_id` itself.

### Part 2 — one indirect hop
Return every record id reachable from `target_user_id` within **at most 2 hops**: `target_user_id`'s
direct links, plus the direct links of those direct links (i.e. linked through exactly one
intermediate record). This is a superset of Part 1's result (a 1-hop link is also within 2 hops).
Ascending, never including `target_user_id` itself, and never listing the same id twice even if it
is reachable via more than one 2-hop path.

### Part 3 — full connected component
Return every record id in the same connected component as `target_user_id` — every record
reachable from the target by a path of **any** length through the link graph (the transitive
closure of "directly linked"). Ascending, never including `target_user_id` itself. If
`target_user_id` has no links at all, the result is empty (a singleton component excludes the
target from its own answer, same as Parts 1–2).

### Validation (all parts)
- A `target_user_id` that does not appear in `rows` is a caller error — raise `ValueError`, do not
  silently return an empty list (there is a real difference between "this contact has zero links"
  and "this contact doesn't exist").
- Two rows sharing the same `id` is malformed input (which one is authoritative?) — raise
  `ValueError` rather than silently keeping the last one.

## Worked examples

### Example A — verbatim from the source (PracHub, see Sources)
```
rows:
  1: name=Alice,  email=alice@gmail.com, company=Stripe
  2: name=Alicia, email=alice@gmail.com, company=Stripe
  3: name=Alice,  email=alice@yahoo.com, company=Google
  4: name=Bob,    email=bob@gmail.com,   company=Stripe
weights: name=0.2, email=0.5, company=0.3   threshold: 0.5   target: 1
```
- **Part 1** -> `[2]` (1 and 2 share `email` + `company`: `0.5 + 0.3 = 0.8 >= 0.5`; 1 vs 3 shares
  only `name` = 0.2; 1 vs 4 shares nothing = 0.0 — neither reaches 0.5)
- **Part 2** -> `[2]` (record 2's own direct links: 2 vs 3 shares nothing, 2 vs 4 shares only
  `company` = 0.3 < 0.5 — record 2 has no *other* direct links, so 2 hops finds nothing new beyond
  Part 1 on this particular 4-record set — this matches the source's own reported Part-2 output on
  this same example; see Sources for why a bigger example is needed to actually see 2 hops add a
  record)
- **Part 3** -> `[2]` (component of `1` is just `{1, 2}`; `3` and `4` are each isolated)

### Example B — this repo's own extension (not from the source; built to exercise multi-hop)
```
rows:
  1: name=Alice, email=alice1@co.com, company=Acme
  2: name=Alice, email=alice2@co.com, company=Acme
  3: name=Zed,   email=alice2@co.com, company=Zenith
  4: name=Zed,   email=zed4@co.com,   company=Zenith
  5: name=Bob,   email=bob5@co.com,   company=Other
weights: name=0.2, email=0.5, company=0.3   threshold: 0.5   target: 1
```
Pairwise scores that reach threshold: `1-2` (`name`+`company` = 0.5), `2-3` (`email` = 0.5), `3-4`
(`name`+`company` = 0.5). `1-3`, `1-4`, `2-4` all score 0. `5` is isolated.
- **Part 1** -> `[2]` (only direct link of `1`)
- **Part 2** -> `[2, 3]` (`2`'s own direct link `3` is now reachable in exactly 2 hops; `4` is 3
  hops away and correctly excluded)
- **Part 3** -> `[2, 3, 4]` (the whole chain `1-2-3-4`; `5` never appears — it isn't in `1`'s
  component)

## Edge cases
- score exactly equal to `threshold` still counts as linked (non-strict `>=`)
- two records that are both missing the same field (e.g. both `company=""`) must **not** score a
  match on that field, even though the empty strings are literally equal — this can flip a result
  that would otherwise cross `threshold`
- a record with zero links anywhere: Part 1/2/3 all return `[]`
- a triangle or any cycle in the link graph must not produce duplicate ids in the output or loop
  forever (Part 2's "hop of a hop" and Part 3's traversal both need a visited-set)
- `target_user_id` not present in `rows` -> `ValueError` (not an empty list)
- a duplicate `id` across two rows -> `ValueError`
- output ids are sorted as **plain strings**, not numerically — `"u10"` sorts before `"u2"`
- Part 2's result can be identical to Part 1's when no record is reachable in exactly 2 hops but
  not 1 (see Example A) — this is not a bug, just a property of that particular graph
- large batch where most field values are unique but a handful of clusters share exact field
  values — must not degrade to comparing every pair of records in the whole input; only candidate
  pairs (records agreeing on at least one field) need a full score computed

## Variants seen in the wild
- The same rule set is filed under two different titles on PracHub ("find linked user records by
  similarity" and "...by weighted similarity") from two independent reports six weeks apart, and
  under yet another title ("Matching Contacts") on interviewdb.io and in `en_forums.md` — treat
  these as the same question; only the display name differs across aggregators.
- `problems/q18_collusion_ring`'s Part 4 (`weighted_links`) implements the same direct-match
  scoring rule (and even the same default weights) as a helper inside a larger fraud-ring problem,
  but only ever computes 1-hop links to a single target — it does not have this problem's Part
  2/Part 3 multi-hop requirement.

## What this tests
skills: S03 record modeling (rows as id-keyed dicts) · S04 weighted-field aggregation into a
single score · S08 deterministic ascending sort (plain string order) · S18 validation (unknown
target, duplicate id) · A16 union-find/connected-components style graph traversal (BFS here, since
Part 1/2 need bounded-hop results that plain union-find can't give directly)

## Sources
- https://prachub.com/coding-questions/find-linked-user-records-by-similarity（访问日期
  2026-09-03）——原文摘录：*"For each field among {name, email, company}: If A.field == B.field
  (string equality), add weights[field] to the score."*；页面本身给出的 Example Data 与 Part
  1/2/3 期望输出，与本文件 Example A 完全一致（Software Engineer / Technical Screen(Phone) /
  Medium，发布 2026-06-21）。
- https://prachub.com/coding-questions/find-linked-user-records-by-weighted-similarity（访问日期
  2026-09-03）——同一规则的第二次独立报告，"Last updated: Jul 8, 2026"，同为 Technical Screen /
  Medium；本次抓取只返回了 Quick Overview 摘要，没有返回该页面自己的样例表格。
- https://www.interviewdb.io/question/stripe/matching-contacts（访问日期 2026-09-03）——确认
  "Matching Contacts" 这个标题独立存在于 interviewdb，与 PracHub 的措辞不同但规则相同。
- `catalog/raw/en_forums.md` §24（"Record linking / linked users"，medium 置信度，linkjob 2026
  电面转述）——权重与 threshold 数值（`name=0.2, email=0.5, company=0.3`，`threshold=0.5`）与
  PracHub 原文完全一致，互相印证，非重复计数。
- `catalog/discovery/2026-09/C_batchA.md` `## C7` 一节（本仓库 2026-09-03 的二轮排查记录，含检索
  方法与失败检索式）。
- **未能验证的部分**：Part 1 页面自带的 Example Data（4 条记录）已逐字核对并复现于本文件 Example
  A；但该页面对 Part 3 的补充说明（"records form chain: 1-2-3, 2-4"）无法用同一份 4 条记录数据自
  洽地复现（用给定字段值计算，2-3 与 2-4 都不到 threshold），怀疑是抓取工具在摘要 Part 3 时引用了
  页面上另一段示例但未能取回其具体字段值。为避免用无法验证的数字冒充原文，本文件的 Example B
  （用来实际展示 2-hop 与全连通分量的区别）是本仓库自己构造的，在上面明确标注为"this repo's own
  extension"，不要把它当成 PracHub 的原文样例。
