---
slug: fruit-into-baskets
---
## Q
**LC 904 水果成篮**｜Medium

数组 `fruits[i]` 是第 `i` 棵树的水果种类，两个篮子各装一种。从任意一棵树起向右连续采摘，求最多能摘几个。

## A
**一句话。** 求最多含两种数字的最长连续子数组：滑动窗口加 `Counter`，种类超过 2 就收缩左端。

```python
def total_fruit(fruits):
    count = Counter()                # 窗口内 种类 -> 数量
    best = left = 0
    for right, kind in enumerate(fruits):
        count[kind] += 1
        while len(count) > 2:        # 超过两个篮子，收缩
            gone = fruits[left]
            count[gone] -= 1
            if count[gone] == 0:
                del count[gone]      # 必须删键
            left += 1
        best = max(best, right - left + 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 计数减到 0 不删键：`len(count)` 不回落，`left` 越界，`[1,2,3,2,2]` 报 `IndexError`。
- 遇到第三种就清空重来：`[1,2,3,2,2]` 只得 `3`，漏了 `[2,3,2,2]` 的 `4`。
- `max` 写在收缩前：此刻窗口含三种，会高估答案。

**追问。**
- 最多 `k` 种？：把 `2` 换成 `k`，代码不变（LC 340）。
- 要返回具体区间？：更新最优时记 `start = left`，返回 `fruits[start:start+best]`。

**同模式。** LC 3 无重复字符的最长子串、LC 340 至多包含 K 个不同字符的最长子串、LC 424 替换后的最长重复字符、LC 1004 最大连续 1 的个数 III
