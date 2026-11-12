---
slug: closest-prime-numbers-in-range
---
## Q
**LC 2523 范围内最接近的两个质数**｜Medium

在 `[left, right]` 内找两个质数 `a < b`，使 `b - a` 最小，并列取 `a` 最小的一对；凑不出返回 `[-1, -1]`。

## A
**一句话。** 埃氏筛筛出质数，最优一定是相邻质数对，扫一遍取差最小、先出现的。

```python
def closest_primes(left, right):
    sieve = bytearray([1]) * (right + 1)
    sieve[:2] = b"\x00\x00"           # 0 和 1 不是质数
    for p in range(2, isqrt(right) + 1):
        if sieve[p]:
            cnt = len(range(p * p, right + 1, p))
            sieve[p * p::p] = bytes(cnt)   # 从 p*p 划倍数
    primes = [p for p in range(left, right + 1) if sieve[p]]
    if len(primes) < 2:
        return [-1, -1]
    # min 遇并列取第一个，即 a 最小的一对
    a, b = min(pairwise(primes), key=lambda t: t[1] - t[0])
    return [a, b]
```

**复杂度。** 时间 `O(R log log R)`，空间 `O(R)`。

**易错点。**
- 忘清 `0` 和 `1`：`left=1, right=3` 会返回 `[1, 2]`，应为 `[2, 3]`。
- 质数不足两个：要返回 `[-1, -1]`，不是空列表。

**追问。**
- `right` 到 `10^12` 但区间很短？：分段筛，只开区间长度的数组，用 `<= √right` 的数当筛子。
- 能提前结束吗？：扫到差 `<= 2` 的一对就可直接返回，不可能更小。

**同模式。** LC 204 计数质数、LC 762 二进制表示中质数个数的数字、LC 866 回文质数
