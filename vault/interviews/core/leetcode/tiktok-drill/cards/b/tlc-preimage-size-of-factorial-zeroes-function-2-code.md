---
id: tlc-preimage-size-of-factorial-zeroes-function-2-code
node: b.preimage-size-of-factorial-zeroes-function
type: qa
step: 2
---
## Q
**LC 793 阶乘函数后 K 个零**｜写出 Python 实现

`f(x)` 是 `x!` 末尾零的个数（`0! = 1`）。给定整数 `k`（`0 <= k <= 10^9`），返回满足 `f(x) = k` 的非负整数 `x` 的个数。

## A
**思路。** 先写 `zeros(x)`：反复整除 `5` 并累加商。再写 `first_reaching(target)`：在 `[0, 5 * (target + 1)]` 上二分，找最小的 `x` 使 `zeros(x) >= target`。答案是 `first_reaching(k + 1) - first_reaching(k)`。

```python
def preimage_size_fzf(k: int) -> int:
    def zeros(x: int) -> int:                   # x! 末尾 0 的个数 = x! 里因子 5 的个数 = x//5 + x//25 + ...
        count = 0
        while x:
            x //= 5
            count += x
        return count

    def first_reaching(target: int) -> int:     # 最小的 x，使得 zeros(x) >= target
        lo, hi = 0, 5 * (target + 1)            # zeros(5 * (target + 1)) >= target + 1，上界一定够
        while lo < hi:
            mid = (lo + hi) // 2
            if zeros(mid) >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    return first_reaching(k + 1) - first_reaching(k)    # zeros 单调不减：等于 k 的 x 是一段连续区间
```

**运行。** `k = 0` → `5`；`k = 5` → `0`；`k = 3` → `5`；`k = 6` → `5`；`k = 30` → `0`；`k = 10^9` → `5`。

**复杂度。** 时间 `O(log^2 k)`（外层二分约 `33` 轮，每轮 `zeros` 约 `14` 次除法）；空间 `O(1)`。

**写法要点。** `while x: x //= 5; count += x` 是数因子 `5` 的惯用写法：每一轮的商就是「含这一层 `5` 的幂的倍数个数」，累加即得总数；两个二分共用一个 `first_reaching`，用「`>= target` 的最小 `x`」这种统一的左边界写法（`zeros(mid) >= target` 时 `hi = mid`，否则 `lo = mid + 1`），避免写两遍边界；Python 整数没有溢出，`x` 到 `5 * 10^9` 也不用担心。
