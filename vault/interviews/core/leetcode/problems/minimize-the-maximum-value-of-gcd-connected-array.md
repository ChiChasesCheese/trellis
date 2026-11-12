---
slug: minimize-the-maximum-value-of-gcd-connected-array
---
## Q
**LC 4098 最小化 GCD 连通数组的最大值**｜Medium

构造长为 `n` 的严格递增正整数数组，满足 `nums[index] = value` 且相邻元素 `gcd > 1`。求末元素的最小值，无解返回 `-1`。

## A
**一句话。** 左右互不干扰：偶数 `value` 两边步长都是 `2`，奇数先跳到偶数（`±p`，`p` 为最小质因子）再步长 `2`。

```python
def minimize_max_gcd_connected(n, index, value):
    left, right = index, n - 1 - index
    if value == 1:
        return -1
    p = 2                   # value 的最小质因子
    while p * p <= value and value % p:
        p += 1
    if p * p > value:
        p = value
    if value % 2 == 0:
        if left > value // 2 - 1:   # 最多放到 2
            return -1
        return value + 2 * right
    if left > (value - p) // 2:     # 先到 value-p，再每步 -2
        return -1
    if right == 0:
        return value
    return value + p + 2 * (right - 1)   # 第一步 +p 变偶数
```

**复杂度。** 时间 `O(√value)`，空间 `O(1)`。

**易错点。**
- 奇数的第一步写成 `+2`：`gcd(15,17)=1`，`(2,0,15)` 得 `17`，应为 `18`。
- 左边容量只数 `p` 的倍数：`value=15` 应为 `(15-3)/2 = 6`，只数 `3` 的倍数得 `4`，会误判 `-1`。

**追问。**
- `value` 是奇质数且 `index > 0` 呢？：左边没有可放的公倍数，返回 `-1`，如 `(2,1,3)`。

**同模式。** LC 2709 最大公约数遍历、LC 952 按公因数计算最大组件大小、LC 1819 序列中不同最大公约数的数目
