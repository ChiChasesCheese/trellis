---
slug: largest-number-after-digit-swaps-by-parity
---
## Q
**LC 2231 按奇偶性交换后的最大数字**｜Easy

正整数 `num`。可以交换任意两位数字，只要它们奇偶性相同（可以交换任意多次）。求能得到的最大数。

## A
**一句话。** 奇数位和偶数位互不干扰：各自从大到小排；遍历原数的每个位置，按该位是奇还是偶取对应堆里剩下的最大数字。

```python
def largest_integer(num):
    s = list(map(int, str(num)))
    even = sorted(d for d in s if d % 2 == 0)   # 升序，pop 取最大
    odd = sorted(d for d in s if d % 2 == 1)
    return int(''.join(str((odd if d % 2 else even).pop())
                       for d in s))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 全局排序：奇偶位置的格局必须保持，只在同奇偶的位置里换。
- 升序排序却取队首：升序列表要从末尾 `pop()` 才是最大的。

**追问。**
- 需要最小值怎么改？：两个列表改成降序排序，仍用 `pop()` 取最小。

**同模式。** LC 670 最大交换、LC 179 最大数、LC 402 移掉 K 位数字
