---
slug: fair-candy-swap
---
## Q
**LC 888 公平的糖果交换**｜Easy

Alice 和 Bob 各拿出一盒糖果互换，使两人总数相同。给两人各盒的糖数，返回要换的两盒（保证有解）。

## A
**一句话。** 总数相等得 `y = x - (sumA - sumB) / 2`，Bob 的盒子进集合，枚举 Alice 的 `x` 查 `x - delta`。

```python
def fair_candy_swap(aliceSizes, bobSizes):
    delta = (sum(aliceSizes) - sum(bobSizes)) // 2
    bob = set(bobSizes)
    for x in aliceSizes:
        if (y := x - delta) in bob:
            return [x, y]
```

**复杂度。** 时间 `O(n + m)`，空间 `O(m)`。

**易错点。**
- 符号写反成 `x + delta`：`[1,1]` 与 `[2,2]` 得空，应为 `[1,2]`。
- 用 `/` 代替 `//`：答案变成 `[1, 2.0]`。
- Bob 的列表不转集合：每次线性查找，退回 `O(nm)`，超时。

**追问。**
- 想要 `O(1)` 额外空间？：两个数组排序后双指针，按总和差移动。
- 不保证有解时？：先看 `(sumA - sumB) % 2`，奇数直接无解。

**同模式。** LC 1 两数之和、LC 532 数组中的 k-diff 数对、LC 1010 总持续时间可被 60 整除的歌曲、LC 560 和为 K 的子数组
