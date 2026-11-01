---
slug: bitwise-and-of-numbers-range
---
## Q
**LC 201 数字范围按位与**｜Medium

给你两个整数 `left` 和 `right`，表示区间 `[left, right]`，返回此区间内所有数字按位与的结果（包含 `left`、`right` 端点）。`0 <= left <= right <= 2^31 - 1`。例：`left = 5, right = 7` → `4`；`left = 0, right = 0` → `0`；`left = 1, right = 2147483647` → `0`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 位运算：区间内所有数按位与等于 `left` 和 `right` 的二进制公共前缀。

**一句话。** 把 `left` 和 `right` 同时右移，直到它们相等，剩下的就是公共前缀，再左移回去，后面补 0。

**识别。** 「一个连续区间的按位与」：区间长度可达 `2^31`，不能逐个与；连续整数的低位会来回翻转，只有高位的公共前缀能保留。

**推导。** 暴力 `for x in range(left, right + 1): ans &= x` 是 `O(right - left)`，最坏 `2^31` 次，超时。看区间内的数在二进制上的变化：从 `left` 增大到 `right`，只要 `left` 和 `right` 有一位不同，在这一位及其右边，区间里一定出现过 0 和 1 的所有变化（包括低位全 0 / 全 1 的数），按位与后这些位都是 0。只有最高的不同位之前的公共前缀，区间内所有数都一样，会被保留。所以结果是 `left` 与 `right` 的公共前缀，后面全补 0。

```python
def range_bitwise_and(left: int, right: int) -> int:
    shift = 0
    while left != right:           # 还没找到公共前缀：两个数一起丢掉最低位
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift           # 公共前缀补回被丢掉的 0
```

运行：`(5, 7)` → `4`，`(0, 0)` → `0`，`(1, 2147483647)` → `0`，`(12, 15)` → `12`，`(6, 7)` → `6`。

**复杂度。** 时间 `O(log right)`（最多 31 次移位），空间 `O(1)`。

**拓展优化。**
- Brian Kernighan：不断清掉 `right` 最低位的 1（`right &= right - 1`），直到 `right <= left`，剩下的就是公共前缀，不需要 `shift`：

```python
def range_bitwise_and_kernighan(left: int, right: int) -> int:
    while right > left:
        right &= right - 1         # 清除最低位的 1；每次把 right 向 left 靠近
    return right
```

**易错点。**
- 逐个相与：`(1, 2147483647)` 要循环约 21 亿次，必然超时。
- 忘了左移回去：`(5, 7)` 在 `left == right == 1` 时直接返回 `1`（正确 `4`）。
- 把结果当成 `left & right`：`(5, 7)` 恰好是 `5 & 7 = 5`，不等于 `4`；中间的 `6` 也要参与，`5 & 6 & 7 = 4`。

**同模式。** LC 191 位 1 的个数、LC 231 2 的幂、LC 338 比特位计数、LC 190 颠倒二进制位。
