---
id: tlc-k-th-smallest-in-lexicographical-order-2-code
node: p4.k-th-smallest-in-lexicographical-order
type: qa
step: 2
---
## Q
**LC 440 字典序的第 K 小数字**｜写出 Python 实现

整数 `n`、`k`，`1 <= k <= n <= 10^9`。返回 `[1, n]` 内按字典序排序后的第 `k` 个数。要求时间远小于 `O(k)`。

## A
**思路。** 当前数 `cur` 从 `1` 开始，还要再走 `k - 1` 步。`count(prefix)` 计算以 `prefix` 为根的子树里有多少个不超过 `n` 的数。若 `count(cur) <= k`，目标不在这棵子树里，`k` 减去它，`cur` 变成右邻 `cur + 1`；否则目标在子树里，`k` 减 1（走过 `cur` 自己），`cur` 变成 `cur * 10`。

```python
def find_kth_number(n: int, k: int) -> int:
    def count(prefix: int) -> int:               # 以 prefix 为根的十叉树子树里，落在 [1, n] 的数有几个
        lo, hi, total = prefix, prefix + 1, 0    # 每一层的区间是 [lo, hi)，下一层是 [lo*10, hi*10)
        while lo <= n:
            total += min(n + 1, hi) - lo         # 最后一层可能被 n 截断
            lo, hi = lo * 10, hi * 10
        return total

    cur = 1                                      # 当前停在第 1 小的数：1
    k -= 1                                       # 还要再往后走 k-1 步
    while k:
        size = count(cur)
        if size <= k:                            # 第 k 小不在 cur 的子树里：整棵跳过，去右邻兄弟
            k -= size
            cur += 1
        else:                                    # 在子树里：走进第一个孩子 cur*10，消耗 cur 自己这 1 步
            k -= 1
            cur *= 10
    return cur
```

**运行。** `(13, 2)` → `10`；`(1, 1)` → `1`；`(13, 13)` → `9`；`(100, 100)` → `99`；`(10**9, 10**9)` → `999999999`；`(10**9, 500000000)` → `549999998`。

**复杂度。** 时间 `O(log^2 n)`：外层至多约 `9 · 10` 次循环，每次 `count` 至多十层；空间 `O(1)`。

**写法要点。** 内部函数 `count` 只读外层的 `n`，不用传参；`lo, hi = lo * 10, hi * 10` 元组同时更新，两个端点永远同步；`while k:` 把"还要走几步"直接当循环条件，`k` 减到 `0` 时 `cur` 就是答案；`min(n + 1, hi) - lo` 利用半开区间避免 `+1 / -1` 的边界错误。
