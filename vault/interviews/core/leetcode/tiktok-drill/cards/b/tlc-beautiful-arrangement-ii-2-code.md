---
id: tlc-beautiful-arrangement-ii-2-code
node: b.beautiful-arrangement-ii
type: qa
step: 2
---
## Q
**LC 667 优美的排列 II**｜写出 Python 实现

给 `n`、`k`（`1 <= k < n <= 10^4`），返回 `1..n` 的一个排列，使相邻差的绝对值恰有 `k` 个不同的值，任意一个即可，要求 `O(n)`。

## A
**思路。** 用双指针 `lo = 1`、`hi = k + 1` 在 `[1, k+1]` 里交替取数：先 `lo`，再 `hi`，再 `lo`……直到两指针相遇；这 `k + 1` 个数的相邻差是 `k, k-1, ..., 1`。再把 `k+2..n` 递增追加。

```python
def construct_array(n: int, k: int) -> list[int]:
    ans: list[int] = []
    lo, hi = 1, k + 1                          # 前 k+1 个数在 1..k+1 里"一头一尾"交替取
    while lo <= hi:
        ans.append(lo)
        lo += 1
        if lo <= hi:
            ans.append(hi)
            hi -= 1
    ans.extend(range(k + 2, n + 1))            # 剩下的递增接上，只产生已有的差
    return ans
```

运行：`(3, 1)` → `[1, 2, 3]`；`(3, 2)` → `[1, 3, 2]`；`(5, 3)` → `[1, 4, 2, 3, 5]`；`(10, 4)` → `[1, 5, 2, 4, 3, 6, 7, 8, 9, 10]`；`(2, 1)` → `[1, 2]`。

**复杂度。** 时间 `O(n)`：每个数只追加一次；空间除输出外 `O(1)`。

**写法要点。** `lo += 1` 之后再判断 `lo <= hi`，这样奇数个元素时最后一个由 `lo` 单独追加，不会重复；`list.extend(range(...))` 直接把递增段接上，不需要循环；两指针从区间两端向中间收拢，是「头尾交替」类写法的通用形状。
