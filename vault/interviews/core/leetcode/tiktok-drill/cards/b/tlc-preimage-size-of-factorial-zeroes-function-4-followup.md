---
id: tlc-preimage-size-of-factorial-zeroes-function-4-followup
node: b.preimage-size-of-factorial-zeroes-function
type: qa
step: 4
---
## Q
**LC 793 阶乘函数后 K 个零**｜追问

面试官接着问：（1）为什么答案只可能是 `0` 或 `5`？（2）要列出这些 `x`？（3）和「求 `n!` 末尾有几个零」（LC 172）是什么关系？

## A
1. **只能是 `0` 或 `5`。** `f(x)` 只在 `x` 是 `5` 的倍数时才可能增长（`x = 5m` 才多出因子）。所以 `f(5m) = f(5m + 1) = ... = f(5m + 4)`，每个值要么对应一整段 `5` 个 `x`，要么在 `f` 一次增加 `>= 2` 时被跳过（`f(24) = 4`，`f(25) = 6`，值 `5` 被跳过）。因此只需判断 `k` 是否被跳过，被跳过返回 `0`，否则 `5`。
2. **列出这些 `x`。** 直接用 `bisect_left` 对 `range` 做二分：

```python
from bisect import bisect_left


def factorials_with_zeros(k: int) -> range:
    def zeros(x: int) -> int:
        count = 0
        while x:
            x //= 5
            count += x
        return count

    top = 5 * (k + 1)
    lo = bisect_left(range(top + 1), k, key=zeros)          # 第一个 zeros(x) >= k
    hi = bisect_left(range(top + 1), k + 1, key=zeros)      # 第一个 zeros(x) >= k + 1
    return range(lo, hi)                                    # 长度就是答案：0 或 5
```

`factorials_with_zeros(3)` 是 `range(15, 20)`，`factorials_with_zeros(5)` 是 `range(25, 25)`（空）。
3. **LC 172。** LC 172 是正向：已知 `n`，直接算 `f(n)`，也就是这里的 `zeros`；LC 793 是反向：已知 `f` 的值，求 `x` 的个数。把正向函数写对，再对单调的正向函数二分，就是「反函数」问题的通用做法。

**Python 提醒**：`bisect_left(range(N), target, key=f)` 需要 Python 3.10+，`range` 对象不占内存，`key` 只对被探测的下标调用，所以只算约 `log N` 次 `f`；若用 `bisect_left([f(x) for x in range(N)], ...)` 会先构造 `N` 个元素的列表，直接超时或爆内存。
