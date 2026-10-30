---
id: tlc-tt-largest-number-below-n-from-digits-2-code
node: p2.tt-largest-number-below-n-from-digits
type: qa
step: 2
---
## Q
**用给定数字拼出小于 N 的最大数**｜写出 Python 实现

写 `largest_below(n, digits)`：`n` 是正整数（`1 <= n <= 10^18`），`digits` 是数字列表（元素 `0` 到 `9`，每个可重复使用，`1 <= len(digits) <= 10`）；返回由这些数字拼出的、**严格小于** `n` 的最大整数，整数不能有前导零（`0` 本身除外），拼不出返回 `-1`。

## A
**思路。** 先数出 `n` 能被 `digits` 拼出的前缀长度 `p`。同位数时，从共享前缀长度 `min(p, 位数 - 1)` 往 `0` 试：在第 `i` 位用二分找比 `n` 的这一位小的最大数字，找到就把后面全填最大数字并返回。全失败就返回少一位的全最大数字。

```python
from bisect import bisect_left


def largest_below(n: int, digits: list[int]) -> int:
    """由 digits 中的数字（可重复使用）拼出严格小于 n 的最大非负整数，没有则返回 -1。"""
    allowed = sorted(set(digits))
    top = allowed[-1]
    s = str(n)
    length = len(s)
    usable = set(allowed)
    p = 0                                            # n 的前 p 位都能用 allowed 拼出来
    while p < length and int(s[p]) in usable:
        p += 1
    for i in range(min(p, length - 1), -1, -1):      # 共享前缀 s[:i] 从长到短试
        j = bisect_left(allowed, int(s[i]))          # allowed[:j] 是比 s[i] 小的数字
        if j and (allowed[j - 1] or i or length == 1):   # 多位数的首位不能是 0
            return int(s[:i] + str(allowed[j - 1]) + str(top) * (length - i - 1))
    if length > 1:                                   # 同长度没有解：少一位，全取最大数字（只有 0 时就是 0）
        return int(str(top) * (length - 1))
    return -1
```

运行：`(23415, [2, 4, 9])` → `22999`，`(2000, [3, 5])` → `555`，`(2311, [2, 3])` → `2233`，`(22222, [2])` → `2222`，`(23, [2, 3])` → `22`，`(100, [0, 1])` → `11`，`(10, [0])` → `0`，`(5, [0])` → `0`，`(1, [1])` → `-1`，`(5, [5])` → `-1`，`(10**18, [1, 9])` → `999999999999999999`。

**复杂度。** 时间 `O(L log |digits|)`，`L` 是 `n` 的位数，最多 `19`；空间 `O(L)`。

**写法要点。**
- `sorted(set(digits))`：先去重再排序，`allowed[-1]` 是最大数字，`allowed` 可直接二分。
- `bisect_left(allowed, d)` 的返回值 `j` 恰好是「比 `d` 小的数字个数」，`allowed[j - 1]` 就是其中最大的，一次二分代替线性扫描。
- 按字符串拼接再 `int()`：`str(top) * k` 重复数字，比循环累加简洁；数位题用字符串处理比反复 `// 10`、`% 10` 更直观。
- `for i in range(min(p, length - 1), -1, -1)`：上界取到 `length - 1`，保证严格小于，不会把 `n` 本身当成候选。
