---
id: hl-c13-cas-loop
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 4
---
## Q
写出无锁的「更新最大值」`update_max(std::atomic<long>& m, long v)`。CAS 循环的原理是什么？`weak` 和 `strong` 的区别？

## A
```cpp
void update_max(std::atomic<long>& m, long v) {
    long cur = m.load(std::memory_order_relaxed);
    while (cur < v &&
           !m.compare_exchange_weak(cur, v, std::memory_order_relaxed)) {
        // 失败时 cur 已被刷新为当前值，循环重新检查 cur < v
    }
}
```
- **CAS 循环**是无锁算法的积木：读当前值 → 计算 → `compare_exchange` 仅在值未变时写入；失败说明别人先改了，`cur` 被刷新，重来。
- `_weak` 允许**伪失败**（在 LL/SC 架构上更快），放在循环里用；`_strong` 不会伪失败。
