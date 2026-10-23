# 盲区期（2026-06 → 2026-09）一手材料 — Reddit 收割

> 1p3a 镜像停在 2026-06-01，`catalog/CATALOG.md` 冻结于 2026-08-25。这四个月是我们唯一的
> 结构性盲区，而它正好是用户面试前的窗口。
> 本轮用 `tools/harvest.py` 从 Reddit RSS 取到 **8 篇**该窗口内的一手 Stripe 帖（正文 + 全部评论）。
> 原始数据：`catalog/discovery/harvest/reddit_blindspot_2026-06_to_09.json`

## 收割统计

- 索引 **418 帖**（r/leetcode + r/cscareerquestions × 20 个检索式）
- 标题含 `stripe` 的 **83 帖**；其中盲区期（2026-06 起）**12 帖**
- 成功取到全文 **8 篇**（4 篇因 429 未取到，可重跑补齐）
- 另有已取全文 89 帖 / 2852 条评论存于 `reddit_2026-09-03.json`，尚未逐条分析

Reddit 搜索**召回宽、精度低**：418 帖里只有 83 帖标题真的提到 Stripe，其余是泛面试帖
（Meta / Google / Amazon）。筛选必须做，别把索引数当 Stripe 材料数。

---

## 1. AI Programming Exercise —— 从"存疑"升级为**已确认**

来源：`Stripe's New AI Programming Exercise Interview - What It's Actually Like`，
r/leetcode，**2026-06-13**，正文 1989 字 + 23 条评论。

原文要点（英文照抄关键句）：

- 环境：**"runs in HackerRank, but it's not the standard coding setup. There's a built-in AI chat
  window (kind of like a lightweight Cursor)"** —— 可以让它读 README、出计划、写代码、加测试、调试
- 题目：**"a list of transactions and a list of rules. Each rule says whether to accept or block a
  transaction, followed by an if condition"** —— 解析规则、判断交易是否匹配
- 递进：**"starts pretty straightforward (mostly keyword/string matching), but later parts get
  trickier with boolean logic (AND/OR) and build on previous sections"**
- 时长：**"the actual coding portion is apparently only around 30 minutes"**
- 期望：**"trying to hand-code everything yourself may not be realistic. The expectation seems to be
  that you lean heavily on the AI."**
- 有效打法：让 AI 读完整 README → 让它总结需求 → 要一份实现计划**并且真的去 review 它** →
  让它写代码 → **自己加测试和边界用例** → 跑、调

### 对我们的意义

**这与本仓库 `cd07_transactions_rules_ai` 的重建高度吻合**——题材（transactions + rules）、
递进（关键词匹配 → AND/OR 布尔逻辑）、时长（30 min）、评分点（指挥 AI 但自己写测试）全部对上。
这道重建题可以从"重建"上调置信度。

同时**部分回答了上一轮标为"存疑"的那条**（有 Senior+ 候选人说"两轮电面都是 AI 辅助"）：
本帖描述的是 **onsite loop 里新增的一轮**，不是电面。两条不矛盾，但仍不足以断定 AI 轮的总数，
维持"按一轮准备、可能更多"的说法。

---

## 2. Intern 完整流程（2026-07-17）—— 两轮 coding，不是一轮

来源：`Stripe intern interview experience`，r/leetcode，正文 2207 字 + 38 条评论。
申请 2025-08/09，OA 在 2025-10。

| 轮次 | 内容（原文摘录） |
|---|---|
| **OA** | **45 分钟**，1 题 4 part。"mostly string manipulation mixed with a transaction-flow/**LRU cache** style design, where you had to implement 3–4 functions"。**19 个测试用例，他过了 15 个** |
| **Round 1 · Coding 45 min** | Senior SDE 面。"parsing a **CSV file provided as a string**. After parsing it correctly, you had to answer multiple **queries** based on the data"，4 part。他做完 2 part，第 3 part 讲了思路没时间写 |
| **Round 2 · Coding 45 min** | "a combination of **graphs + strings**, somewhat similar to the logic behind a **Splitwise** application"，多 part |
| 后续（未进行） | Debugging round + HR/Behavioral |

### 三条可直接行动的结论

1. **实习生 loop 里有两轮独立的 coding**，不是一轮。我们 `LOOP_GUIDE` §0 的总图把校招/实习写成
   "Programming Exercise + Integration（+ Bug Squash）"，**没有体现 coding 可能是两轮**。
2. **Round 2 "Splitwise-like" = 多人债务最小化 = LC 465 = 我们的 `q32` / `qA08`。**
   镜像里也有 `multiple_people_debt_minimization`（2026-01-24）。两个独立来源指向同一题族，
   **这道题的优先级应该上调**。
3. **OA 的 19 个测试用例、过 15 个仍进下一轮** —— 佐证 catalog 里"partial credit can advance"的记载。

---

## 3. 其余 6 篇（信息量较小，逐条记录）

| 日期 | 标题 | 要点 |
|---|---|---|
| 2026-08-26 | Stripe API integration Round | 正文 279 字 + 2 评论，确认 integration 轮仍在用 |
| 2026-08-05 | Stripe MLE Interview | MLE 赛道，本题库不覆盖 |
| 2026-07-04 | Stripe mobile interview | 移动端岗位，不覆盖 |
| 2026-06-30 | Stripe Recruiter Speed | 流程时间线类 |
| 2026-06-08 | Stripe interview feedback | 841 字 + 12 评论，反馈类 |
| 2026-06-01 | BCG VS STRIPE | offer 比较，非技术 |

**未取到的 4 篇（429 限流）**，值得重跑补齐：
`Stripe newgrad virtual onsite`（2026-08-07）· `Stripe and Meta new AI interview experience`（2026-07-31）·
`Stripe Interviews`（2026-06-17）· `STRIPE Interview Experience: Android`（2026-06-08）

补齐命令：
```bash
python3 tools/harvest.py reddit --sub leetcode --q "stripe onsite" --sort new
python3 tools/harvest.py reddit-post <post_id> --sub leetcode
```

---

## 4. 盲区结论

**盲区期没有出现"我们完全没见过的题型"。** 8 篇里能辨认出的题目全部落在已覆盖的题族里
（transactions+rules → cd07；CSV 解析+查询 → q20/ps12 族；Splitwise → q32/qA08；LRU → q26）。

这**弱化了上一轮"4 个月盲区约有 50 道没见过的题"的担忧**——那个 50 本来就建立在被推翻的
"每月 13 道新题"之上（见 `coverage_analysis.md` 的更正块）。

但样本只有 8 篇，**不足以证明盲区期没有新题**，只能说"在这 8 篇能看到的范围内没有"。
剩下 4 篇 + 89 帖已取全文 + 2852 条评论尚未逐条分析，是下一轮最便宜的增量。
