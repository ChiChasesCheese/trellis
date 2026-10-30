---
id: tlc-tt-removable-timestamp-task-scheduler-1-signal
node: p4.tt-removable-timestamp-task-scheduler
type: qa
step: 1
---
## Q
**可删除任务的时间戳调度器（popTask）**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-20（面试记录）

实现任务调度器：`addTask(taskId, timestamp)` 加入任务；`removeTask(taskId)` 删除尚未被取走的任务；`popTask(num)` 返回时间戳最早的 `num` 个任务并把它们从调度器中移除，时间戳相同的任务按 `taskId` 字典序先后。任务不足 `num` 个时返回全部剩余任务；对已存在的 `taskId` 再次 `addTask` 视为更新时间戳。操作总数不超过 `10^5`。例：`(a,5)`、`(b,3)`、`(c,3)` 后 `popTask(2)` → `['b','c']`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「总是取时间戳最早的 `num` 个」→ 优先队列（`heapq` 最小堆）。
- 「还能删除尚未取走的任务」→ 堆不支持按值删除，信号是懒删除（lazy deletion）或有序集合。
- 「`popTask` 要真的移除」→ 取走即从所有结构里消失，不能只是查看。
- 「并列要确定」→ 比较键里带上 `taskId`，用元组 `(timestamp, taskId)`。
- 操作数 `10^5`：每次 `O(n)` 的扫描会变成 `10^10`，必须对数级。

**推导链。**
1. 暴力：任务放列表，每次 `popTask` 排序取前 `num` 个，`O(n log n)` 一次。
2. 堆加真删除：要先在堆里线性找到位置，`O(n)` 一次，仍然慢。
3. 浪费：删除并不需要让堆立刻变干净，只要弹出时不返回已删除的任务。
4. 洞察：用字典 `alive[taskId] = timestamp` 表示任务当前有效的时间戳；堆里的条目 `(ts, id)` 有效当且仅当 `alive.get(id) == ts`。删除只改字典；更新时间戳时旧条目自动失效。
5. 最优：弹出时跳过失效条目，每个条目最多被丢弃一次，摊还 `O(log n)`。

**同模式的题**：LC 1834 单线程 CPU、LC 2336 无限集中的最小数字、LC 703 数据流中的第 K 大元素、LC 355 设计推特。
