---
slug: minimum-operations-to-make-a-uni-value-grid
---
## Q
**LC 2033 获取单值网格的最小操作数**｜Medium

`m x n` 整数网格和整数 `x`。一次操作可使某个元素加 `x` 或减 `x`。求让所有元素相等的最少操作数，做不到返回 `-1`。

## A
**一句话。** 所有元素模 `x` 的余数必须相同才可能；之后把全部元素排序，目标取中位数，每个元素需要 `|v - 中位数| / x` 次。

```python
def min_operations(grid, x):
    a = sorted(v for row in grid for v in row)
    if any((v - a[0]) % x for v in a):     # 余数不同，永远凑不齐
        return -1
    mid = a[len(a) // 2]                   # 中位数使绝对差之和最小
    return sum(abs(v - mid) // x for v in a)
```

**复杂度。** 时间 `O(mn log(mn))`，空间 `O(mn)`。

**易错点。**
- 目标取平均值：绝对值之和在中位数处最小，平均值不一定可达也不一定最优。
- 不检查余数：余数不同的元素永远无法相等，要提前返回 `-1`。

**追问。**
- 能不排序吗？：用快速选择找中位数，期望 `O(mn)`。

**同模式。** LC 462 最小操作次数使数组元素相等 II、LC 453 最小操作次数使数组元素相等、LC 296 最佳的碰头地点
