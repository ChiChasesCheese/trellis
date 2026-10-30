---
id: tlc-implement-rand10-using-rand7-4-followup
node: p3.implement-rand10-using-rand7
type: qa
step: 4
---
## Q
**LC 470 用 Rand7() 实现 Rand10()**｜追问

面试官接着问：（1）怎样把 `rand7()` 的期望调用次数压得更低？（2）反过来，用 `rand10()` 造 `rand7()`？（3）任意由 `randN` 造 `randM`？分别怎么写。

## A
1. **复用被拒的格子**：丢掉的 `41..49` 其实是 `1..9` 上的均匀数，白白扔掉浪费了随机性。让状态保存「`v` 在 `[0, size)` 上均匀」，每次拼一次 `rand7()` 把 `size` 乘 `7`，攒到 `size >= 10` 就取最大的 `10` 的倍数 `limit`，`v < limit` 就输出，否则 `v` 和 `size` 减去 `limit`，余下的继续用：

```python
def rand10_reuse() -> int:
    v, size = 0, 1                       # v 在 [0, size) 上均匀
    while True:
        v = v * 7 + (rand7() - 1)
        size *= 7
        if size >= 10:
            limit = size - size % 10
            if v < limit:
                return v % 10 + 1
            v, size = v - limit, size - limit   # 被拒的格子仍然均匀，留着复用
```

格子数依次是 `7 → 49 → 9 → 63 → 3 → 21 → 1`，期望调用 `329/150 ≈ 2.193` 次（基础版是 `2.45`）；`2 × 10^5` 次调用的实测平均是 `2.1931`。代价是代码更复杂，面试里先写基础版，被问「再少」时再讲这个。
2. **`rand10()` 造 `rand7()`**：`while True: x = rand10(); if x <= 7: return x`。保留 `7/10`，期望 `10/7 ≈ 1.43` 次。
3. **任意 `randM` 由 `randN`**：同样的状态机，`v = v * N + (src() - 1)`，`size *= N`，`size >= M` 时取 `limit = size - size % M`，`v < limit` 返回 `v % M + 1`，否则 `v -= limit; size -= limit`。`M = 3, 10, 20, 100`（源为 `rand7`）各抽 `5000 × M` 次，每个值的次数都在期望值 `5000` 附近。

**Python 提醒**：`random.randint(a, b)` 两端都包含，`random.randrange(a, b)` 不含右端；要复现一串随机输出，用 `random.seed(...)` 固定种子。
