---
id: lcp-rate-limiter-race-check-then-count
node: lcproject.lcp-rate-limiter
type: qa
step: 4
tags: [作答]
---
## Q
在 LLM 网关限流器里，某客户端的滑动窗口只剩 1 个额度，两个线程同时调用 `check`，另一个线程同时调用 `stats()`。没有锁会出什么错？你用什么机制防住，它的代价是什么？

## A
**评分点**
- 说出先检查后动作：两个线程都看到 len < limit 并都追加，窗口超限；GIL 不保护这一对操作
- 说出计数 += 1 是读、加、写三步，并发会丢更新
- 说出机制：同一把锁罩住读时钟、判定、记账、更新计数，stats 也拿这把锁
- 说出不能给判定和计数各加一把锁：stats 会读到已放行但计数还没加的瞬间
- 说出代价：所有 key 排队、吞吐受限于一次判定的速度，临界区只做字典查找和整数运算
- 说出降低办法：按 key 哈希分片，stats 按固定顺序取全部分片锁

<details class="pt"><summary>参考答案</summary>

没有锁时，两个线程都通过 `len(stamps) < limit`，各追加一个，窗口里比额度多一个；`total_allowed += 1` 也会丢更新。GIL 只保证单条字节码，不保证"检查再追加"这一对。做法是一把 `Lock` 罩住整个 `check` 与 `stats`：读时钟、判定、记账、计数同时可见。代价是全体 key 串行，临界区很短时可以接受；流量大了再分片。

</details>

**知识点：** 复合操作（Compound Actions）、同步原语（threading）、线程安全结构的写法（Thread-Safe Structures）
