---
id: cc-chrono-windows-per-key-state
node: chrono.windows
type: qa
---
## Q
A window is kept per client and 10^6 clients appear over a day, most of them exactly once. Name the two problems and the fix.

## A
**Per-key window state must be created lazily and evicted deliberately.**

- Creation: `w = self.windows.get(k)` then insert on miss — never pre-allocate a slot for every id the input might mention, and never use a `defaultdict` if a mere probe would then create state ([[cc-toolbox-hash-defaultdict-read-creates]]).
- Memory: one deque per client that never returns is a leak. Expose a `cleanup(now, idle)` that drops clients whose last event is older than `idle` **and** whose window is already empty — dropping a client whose window still holds events changes the answer.
- Boundary: "idle for at least `idle_ms`" evicts at exactly `idle_ms`. Say whether `==` evicts and return the count if the spec asks for it.
- Never sweep every key on every request; sweep on an explicit command or amortize it.

## Q zh
每个客户端一个窗口，一天里出现 10^6 个客户端，其中大多数只出现一次。指出两个问题和解法。

## A zh
**按 key 的窗口状态必须惰性创建、有意识地驱逐。**

- 创建：先 `w = self.windows.get(k)`，miss 时再插入 —— 不要为输入可能提到的每个 id 预分配槽位，也不要用会让一次探测就建出状态的 `defaultdict`（[[cc-toolbox-hash-defaultdict-read-creates]]）。
- 内存：为一个再也不回来的客户端保留一个 deque 就是泄漏。提供 `cleanup(now, idle)`，丢掉最后事件早于 `idle` **且**窗口已空的客户端 —— 丢掉窗口里还有事件的客户端会改变答案。
- 边界：「空闲至少 `idle_ms`」在恰好 `idle_ms` 时驱逐。说明 `==` 是否驱逐，spec 要求时返回被驱逐的数量。
- 绝不要在每个请求上扫描所有 key；用显式命令触发清理，或者摊销它。
