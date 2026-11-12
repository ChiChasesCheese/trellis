---
slug: minimum-operations-to-write-the-letter-y-on-a-grid
---
## Q
**LC 3071 在矩阵上写出字母 Y 所需的最少操作次数**｜Medium

`n×n`（`n` 为奇数）矩阵，值为 `0/1/2`。Y 由两条到中心的对角线和中心向下的竖线组成。每次可改任一格，使 Y 上的值全相同、其余格全相同且两值不同，求最少操作数。

## A
**一句话。** 分别统计 Y 内外各值的个数，枚举 `a != b` 的 6 种组合，取 `总格数 - 内a - 外b` 最小。

```python
def minimum_operations_to_write_y(grid):
    n = len(grid)
    mid = n // 2
    iny, outy = Counter(), Counter()
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            on = (r <= mid and c in (r, n - 1 - r)) \
                 or (r > mid and c == mid)
            (iny if on else outy)[v] += 1
    return min(n * n - iny[a] - outy[b]
               for a, b in permutations(range(3), 2))
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`。

**易错点。**
- 允许 `a == b`：全 `1` 的 `3×3` 得 `0`，应为 `4`。
- 竖线画成整条中线：中心上方被算进 Y，示例 2 得 `10`，应为 `12`。
- 下半部分继续用 `c == r` 判对角线：会把不属于 Y 的格子算进去，对角线只到中心行。

**追问。**
- 值域扩到 `k` 种怎么办？：每个区域只需考虑出现次数最多的前两个值，常数个组合。
- 要输出具体改法？：记下取最小的 `(a, b)`，再扫一遍。

**同模式。** LC 73 矩阵置零、LC 48 旋转图像、LC 2132 用邮票贴满网格图
