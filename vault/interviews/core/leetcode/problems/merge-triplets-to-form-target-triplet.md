---
slug: merge-triplets-to-form-target-triplet
---
## Q
**LC 1899 合并若干三元组以形成目标三元组**｜Medium

可把两个三元组按分量取 max 合并。问能否得到 `target`。

## A
**一句话。** 取 max 只会变大，所以任一分量超过目标的三元组丢弃，剩下的每个分量都要有一个恰好等于目标值。

```python
def merge_triplets(triplets, target):
    good = [t for t in triplets
            if all(a <= b for a, b in zip(t, target))]
    return all(any(t[i] == target[i] for t in good)
               for i in range(3))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 不过滤就全体取 max：示例一得 `[2,8,5]`，应能得到 `[2,7,5]`。
- 只看有没有整个等于目标的三元组：`[5,5,5]` 要靠合并得到，会被漏判。

**追问。**
- 为什么不用考虑合并顺序？：max 满足交换律、结合律，且只增不减。
- 能一趟扫完吗？：能，维护三个布尔标志，扫描时遇到合格三元组就更新。

**同模式。** LC 55 跳跃游戏、LC 134 加油站、LC 763 划分字母区间、LC 678 有效的括号字符串
