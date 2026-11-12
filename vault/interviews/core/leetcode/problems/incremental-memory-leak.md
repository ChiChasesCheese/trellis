---
slug: incremental-memory-leak
---
## Q
**LC 1860 增长的内存泄露**｜Medium

两个内存条剩余 `memory1`、`memory2`。第 `i` 秒分配 `i` 位给剩余较多的那个（相等给第一个）；两个都不足 `i` 位时崩溃。返回 `[崩溃秒数, 剩余1, 剩余2]`。

## A
**一句话。** 直接模拟，每秒把 `i` 分给较大的那条，步数只有 `O(√(m1+m2))`。

```python
def mem_leak(memory1, memory2):
    i = 1
    while max(memory1, memory2) >= i:
        if memory1 >= memory2:    # 相等给第一条
            memory1 -= i
        else:
            memory2 -= i
        i += 1
    return [i, memory1, memory2]
```

**复杂度。** 时间 `O(√(m1+m2))`，空间 `O(1)`。

**易错点。**
- 平局写成 `memory1 > memory2`：`(2,2)` 得 `[3,0,1]`，应为 `[3,1,0]`。
- 崩溃条件写成“某一条不足”：要两条都不足才崩，用 `max` 判断。

**追问。**
- 内存上限到 `10^18` 怎么办？：模拟太慢，先用等差和加 `isqrt` 求出较大者降到与较小者持平的步数，再按奇偶规律推进。
- 三条或更多内存条？：用最大堆取剩余最多的，`O(t log k)`。

**同模式。** LC 1535 找出数组游戏的赢家、LC 1823 找出游戏的获胜者、LC 2073 买票需要的时间
