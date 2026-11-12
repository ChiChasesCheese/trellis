---
slug: bitwise-and-of-numbers-range
---
## Q
**LC 201 数字范围按位与**｜Medium

求区间 `[left, right]` 内所有整数按位与的结果。

## A
**一句话。** 结果就是 `left` 和 `right` 二进制的公共前缀，同时右移到相等，再左移回去补 0。

```python
def range_bitwise_and(left, right):
    shift = 0
    while left != right:   # 一起丢掉最低位
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift   # 公共前缀补回 0
```

**复杂度。** 时间 `O(log right)`，空间 `O(1)`。

**易错点。**
- 逐个相与：`(1, 2147483647)` 要循环约 21 亿次，必然超时。
- 忘了左移回去：`(5, 7)` 在相等时直接返回 `1`，应为 `4`。

**追问。**
- 为什么只看两端点？：区间内有数在某一位从 0 变 1 的地方，该位及更低位一定出现过 0，与完都是 0。
- 另一种写法？：`right &= right - 1` 不断清掉最低位的 1，直到 `right <= left`。

**同模式。** LC 191 位 1 的个数、LC 231 2 的幂、LC 338 比特位计数、LC 190 颠倒二进制位
