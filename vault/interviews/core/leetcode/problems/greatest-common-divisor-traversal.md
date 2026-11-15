---
slug: greatest-common-divisor-traversal
---
## Q
**LC 2709 最大公约数遍历**｜Hard

整数数组 `nums`。下标 `i`、`j` 之间可以直接走当且仅当 `gcd(nums[i], nums[j]) > 1`。问是否任意两个下标之间都存在一条路径。

## A
**一句话。** 并查集：把每个数分解质因数，同一个质数对应的下标全部并到一起；最后看是不是只有一个连通块。有 `1` 的数组（长度大于 `1`）直接返回 `False`。

```python
def can_traverse_all_pairs(nums):
    n = len(nums)
    if n == 1:
        return True
    if 1 in nums:                      # 1 与任何数的 gcd 都是 1
        return False
    fa = list(range(n))

    def find(x):
        while fa[x] != x:
            fa[x] = fa[fa[x]]
            x = fa[x]
        return x

    first = {}                         # 质数 -> 第一个含它的下标
    for i, x in enumerate(nums):
        p = 2
        while p * p <= x:
            if x % p == 0:
                fa[find(i)] = find(first.setdefault(p, i))
                while x % p == 0:
                    x //= p
            p += 1
        if x > 1:                      # 剩下的大质因子
            fa[find(i)] = find(first.setdefault(x, i))
    return len({find(i) for i in range(n)}) == 1
```

**复杂度。** 时间 `O(n √M α(n))`，空间 `O(n)`。

**易错点。**
- 两两求 `gcd`：`O(n²)` 会超时，改成"数 → 质数 → 数"的二部结构。
- 漏掉分解后剩下的大质因子：`x > 1` 时它本身是质数。
- 数组里有 `1`：`n > 1` 时无解，要先判。

**追问。**
- 如何更快？：用线性筛预处理最小质因子，分解变成 `O(log x)`。

**同模式。** LC 952 按公因数计算最大组件大小、LC 1819 序列中不同最大公约数的数目
