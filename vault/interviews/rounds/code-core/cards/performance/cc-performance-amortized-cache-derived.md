---
id: cc-performance-amortized-cache-derived
node: performance.amortized
type: qa
---
## Q
A derived value — a merchant's flag status, a formatted total — is expensive and read often, so you cache it. What makes the cache correct, and what makes it a bug?

## A
**A cache is correct only when every mutation path invalidates it.**

- Invalidate at the write, not at the read: the branch that changes the inputs clears or recomputes the entry.
- Prefer recompute-on-write when reads outnumber writes — it removes the stale window entirely and keeps reads O(1).
- The bug is always the *second*, rarer mutation path: a reversal, a bulk correction, a duplicate that is deliberately a no-op. It passes the worked example and fails one hidden test.
- `functools.lru_cache` is safe only for pure functions of their arguments — never wrap a method that reads mutable state.

## Q zh
一个派生值 —— 商户的标记状态、格式化好的总额 —— 计算贵而读取频繁，于是你把它缓存起来。什么让缓存正确？什么让它成为 bug？

## A zh
**只有当每一条变更路径都让缓存失效时，缓存才是正确的。**

- 在写时失效，不在读时：改动输入的那个分支负责清除或重算这一项。
- 读多于写时优先「写时重算」—— 它彻底消灭了陈旧窗口，并让读保持 O(1)。
- bug 永远出在**第二条**、更少见的变更路径上：一次冲正、一次批量更正、一个被刻意设计成空操作的重复项。它能过样例，挂在某个隐藏测试上。
- `functools.lru_cache` 只对「参数的纯函数」安全 —— 绝不要包住一个读取可变状态的方法。
