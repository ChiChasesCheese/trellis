---
slug: nth-digit
---
## Q
**LC 400 第 N 位数字**｜Medium

在数字串 `123456789101112...` 中求第 `n` 位（从 1 数起）上的数字。

## A
**一句话。** 按位数分段（1 位数占 9 位，2 位数占 180 位……）先定位段，再算出是哪个数的第几位。

```python
def find_nth_digit(n):
    length, count, start = 1, 9, 1   # 本段：length 位数共 count 个
    while n > length * count:
        n -= length * count          # 整段跳过
        length += 1
        count *= 10
        start *= 10
    num = start + (n - 1) // length  # 落在哪个数
    return int(str(num)[(n - 1) % length])
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 用 `n // length` 而不是 `(n - 1) // length`：段边界上错一个数，`n=9` 应得 `9`。
- 循环条件写成 `n >= length * count`：`n` 恰为整段末尾时多跳一段，`n=9` 抛 `IndexError`。
- 位内偏移用 `n % length`：`n=10` 应得 `1`（数字 `10` 的首位）。

**追问。**
- 要返回第 `n` 位所属的整数？：`num` 就是。
- `n` 超过 64 位呢？：分段只有 `O(log n)` 次，Python 大整数照样适用。

**同模式。** LC 233 数字 1 的个数、LC 902 最大为 N 的数字组合、LC 357 统计各位数字都不同的数字个数、LC 440 字典序的第 K 小数字
