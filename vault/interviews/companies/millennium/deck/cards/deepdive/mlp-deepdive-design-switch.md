---
id: mlp-deepdive-design-switch
node: deepdive.design
type: qa
step: 3
---
## Q
**静态拆分还是更聪明的回退**｜项目深挖

“How did you decide between the two designs in the data-source switch? What does the procedure do?”

## A
这一题问的是“为什么选这个而不是那个”，以及过程里的细节手法。

- **方案 A：** 把现有“哪个视图有数就用哪个”的动态回退做聪明，它已经有粘性状态、三个 CTE 和条件选源，维护负担在涨。
- **方案 B（选）：** 按费用类型静态划分，interchange 固定走 settlement，其余固定留在原来的视图；整体由一个功能开关控制。理由：收入路径上的数据源应该是事实，不是运行时的决定。
- **幂等 `MERGE`：** 合成键是前缀加发票号，任务每小时重跑不会重复计费；幂等在数据的唯一性里，不在外部状态机里。
- **窗口化 `ON`：** 目标表只增不清理，等值条件会扫全部历史，加一个月的窗口让 zone map 剪枝，扫描量恒定。代价：隔一个月以上才重处理的同一记录会绕开去重，这是写在注释里的已知风险。
- **trigger-status 连接：** 上游没校验完，这个连接一行都不返回，“上游可信”成了硬条件。
- **不重复计费：** 旧任务在开关打开时显式排除 interchange，两个任务互补，靠来源过滤而不是 `MERGE` 去重。

**英文答法。**
- Option A was to make the **fallback** smarter; I chose option B, a **static split by fee type** behind a toggle: **the source of truth should be a fact, not a runtime decision**.
- The `MERGE` is **idempotent** on a synthetic key built from the invoice number, so the hourly task can rerun safely.
- A **time-windowed `ON` clause** keeps the scan to the last month and **preserves zone-map pruning**; the trade-off is a record reprocessed a month later bypasses dedup — a documented risk.
- The old task **excludes interchange only when the toggle is on**, so the two paths **can never double-count**.

**追问。**
- **Why not dual-write?** Two tasks gated by one toggle in opposite directions is the mutual exclusion; dual-write without it is how you double-charge.
- **Reusable?** The backfill SQL became the team's CDC table-backfilling template.
