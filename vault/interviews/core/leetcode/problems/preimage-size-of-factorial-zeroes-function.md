---
slug: preimage-size-of-factorial-zeroes-function
---
## Q
**LC 793 阶乘函数后 K 个零**｜Hard

`f(x)` 是 `x!` 末尾零的个数，给定 `k`，求满足 `f(x) = k` 的非负整数 `x` 的个数。

## A
**一句话。** `f` 单调不减，等于 `k` 的 `x` 是连续一段，个数 = 首个 `f >= k+1` 的位置减首个 `f >= k` 的位置。

```python
def preimage_size_fzf(k):
    def zeros(x):                # x! 里因子 5 的个数
        count = 0
        while x:
            x //= 5
            count += x
        return count

    def first_reaching(target):  # 最小 x 使 zeros(x) >= target
        lo, hi = 0, 5 * (target + 1)
        while lo < hi:
            mid = (lo + hi) // 2
            if zeros(mid) >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    return first_reaching(k + 1) - first_reaching(k)
```

**复杂度。** 时间 `O(log² k)`，空间 `O(1)`。

**易错点。**
- `f` 只数 `x//5`：漏掉 `25`、`125`，`k=5` 得 `5`，应为 `0`。
- 二分下界取 `1`：漏掉 `0!`，`k=0` 得 `4`，应为 `5`。
- 上界取 `4*target`：`k=0` 时到不了 `5`；`5*(target+1)` 一定够。

**追问。**
- 为什么答案只有 `0` 或 `5`？：`f` 只在 `5` 的倍数处增长，相同值恰占连续 `5` 个 `x`；值被跳过则为 `0`。
- 怎么列出这几个 `x`？：`range(first_reaching(k), first_reaching(k+1))`。

**同模式。** LC 172 阶乘后的零、LC 69 x 的平方根、LC 878 第 N 个神奇数字、LC 1201 丑数 III
