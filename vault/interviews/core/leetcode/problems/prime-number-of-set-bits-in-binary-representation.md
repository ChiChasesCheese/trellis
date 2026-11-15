---
slug: prime-number-of-set-bits-in-binary-representation
---
## Q
**LC 762 二进制表示中质数个计算置位**｜Easy

给整数区间 `[left, right]`，统计其中有多少个数的二进制表示里 `1` 的个数是质数。

## A
**一句话。** 数值不超过 `10⁶`（不到 20 位），置位数最多 19，把 20 以内的质数存成集合，逐个数查 `popcount` 是否在里面。

```python
def count_prime_set_bits(left, right):
    primes = {2, 3, 5, 7, 11, 13, 17, 19}   # 20 位以内的质数
    return sum(x.bit_count() in primes
               for x in range(left, right + 1))
```

**复杂度。** 时间 `O(right - left)`，空间 `O(1)`。

**易错点。**
- 把 `1` 当质数：`1` 不是质数，集合里不能有。
- 置位数用字符串 `bin(x).count('1')`：能对但慢；`bit_count()` 或 `x &= x - 1` 更快。
- 区间右端点漏掉：`range(left, right + 1)`。

**追问。**
- 怎么再快？：把质数集合压成一个位掩码，查 `mask >> popcount & 1`，免去哈希。
- 区间很大时呢？：按位数 DP，统计置位数为每个值的个数，再对质数求和。

**同模式。** LC 191 位1的个数、LC 338 比特位计数、LC 461 汉明距离、LC 204 计数质数
