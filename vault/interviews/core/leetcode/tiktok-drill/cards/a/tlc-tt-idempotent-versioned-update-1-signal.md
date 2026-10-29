---
id: tlc-tt-idempotent-versioned-update-1-signal
node: a.tt-idempotent-versioned-update
type: qa
step: 1
---
## Q
**幂等、带版本号的数据更新**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-09（面试记录）

实现内存键值存储 `VersionedStore`：`update(request_id, key, value, expected_version)` 只有当 `key` 的当前版本等于 `expected_version` 时才写入并把版本加 1，返回 `(True, 新版本)`，否则返回 `(False, 当前版本)`；同一个 `request_id` 重复调用（客户端超时重试）不能重复写，要原样返回第一次的结果；`get(key)` 返回 `(value, version)`，不存在的 key 为 `(None, 0)`。调用总数 `<= 10^5`。例：`update("r1","a","x",0)` → `(True, 1)`，重试同一调用 → `(True, 1)`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「当前版本等于期望版本才写，然后版本加 1」→ **乐观并发控制**（optimistic concurrency control）：比较并更新（compare-and-set，CAS），防止并发的读-改-写互相覆盖（丢失更新）。
- 「同一个 `request_id` 重试要原样返回」→ **幂等键**（idempotency key）：`request_id → 第一次结果` 的字典。
- 「调用总数 `<= 10^5`」→ 每次操作 `O(1)` 的字典即可，难点在语义和顺序，不在复杂度。

**推导链。**
1. 最简单：直接 `data[key] = value`。两个客户端并发读到同一版本后各自写入，后写覆盖先写。
2. 加版本比较（CAS）。新问题：第一次写成功但响应丢失，客户端重试时版本已变，得到冲突，误以为失败。
3. 加幂等表，并且**先查表再 CAS**：重试直接返回第一次的结果，不再比较版本。
4. 冲突结果也要存表：否则第一次冲突的请求重试时可能写成功，同一请求出现两种结果。每次操作 `O(1)`。

**同模式的题**：LC 981 基于时间的键值存储、LC 1146 快照数组、LC 146 LRU 缓存、LC 2502 设计内存分配器。
