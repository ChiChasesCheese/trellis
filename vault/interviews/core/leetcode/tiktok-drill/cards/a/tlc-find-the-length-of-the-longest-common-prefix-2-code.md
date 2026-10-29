---
id: tlc-find-the-length-of-the-longest-common-prefix-2-code
node: a.find-the-length-of-the-longest-common-prefix
type: qa
step: 2
---
## Q
**LC 3043 最长公共前缀的长度**｜写出 Python 实现

两个正整数数组 `arr1`、`arr2`（长度各 `1..5 * 10^4`，元素 `1..10^8`）。求 `arr1` 的一个数与 `arr2` 的一个数的最长公共前缀（按位数计）的长度，没有公共前缀返回 `0`。

## A
**思路。** 用整数除法逐位去掉末位得到前缀。先把 `arr1` 所有数的所有前缀放进集合；再对 `arr2` 的每个数，从自己开始逐位缩短，第一个在集合里的前缀就是最长的，记录它的位数。

```python
def longest_common_prefix(arr1: list[int], arr2: list[int]) -> int:
    prefixes: set[int] = set()
    for x in arr1:
        while x and x not in prefixes:     # 已经在集合里说明它的更短前缀也都在，可以提前停
            prefixes.add(x)
            x //= 10                       # 去掉最后一位 = 取前一个前缀
    best = 0
    for y in arr2:
        while y and y not in prefixes:     # 从最长的前缀往短处找第一个命中的
            y //= 10
        if y:
            best = max(best, len(str(y)))
    return best
```

运行：`([1,10,100], [1000])` → `3`，`([1,2,3], [4,4,4])` → `0`，`([123], [129])` → `2`，`([5655359], [56554])` → `4`，`([10**8], [10**8])` → `9`；两个数组各 `5 × 10^4` 个随机数约 `20 ms`。

**复杂度。** 时间 `O((n + m) · L)`，`L <= 9` 是最大位数；空间 `O(n · L)`。

**写法要点。** `while x and x not in prefixes` 一个条件同时处理“到 `0` 结束”和“提前结束”；`x //= 10` 把循环变量就地缩短，因为 `x` 只是循环里的副本，不改变数组；`len(str(y))` 只在命中时算一次；`if y` 区分“命中了一个非零前缀”和“被除到 `0`”，后者表示没有公共前缀。
