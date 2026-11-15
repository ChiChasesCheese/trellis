---
slug: sort-integers-by-the-number-of-1-bits
---
## Q
**LC 1356 根据数字二进制下 1 的数目排序**｜Easy

把整数数组 `arr` 按二进制表示中 `1` 的个数从小到大排序；个数相同的按数值从小到大。

## A
**一句话。** 排序键用 `(1 的个数, 数值)`，`bit_count()` 直接数出二进制里的 1。

```python
def sort_by_bits(arr):
    return sorted(arr, key=lambda x: (x.bit_count(), x))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只按 `1` 的个数排：个数相同时没有按数值再排，要放进元组第二位。
- 用 `bin(x).count("1")`：也行，`bit_count()` 更快更清楚。

**追问。**
- 不用内置怎么数 1？：`x &= x - 1` 每次消去最低位的 1，循环次数就是 1 的个数。
- 值域小时怎么更快？：预处理 `bits[i] = bits[i >> 1] + (i & 1)`，计数排序。

**同模式。** LC 338 比特位计数、LC 191 位 1 的个数（Number of 1 Bits）、LC 461 汉明距离
