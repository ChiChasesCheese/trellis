---
id: tlc-largest-number-2-code
node: a.largest-number
type: qa
step: 2
---
## Q
**LC 179 最大数**｜写出 Python 实现

`nums` 有 `1` 到 `100` 个非负整数（每个至多 `10^9`），把它们重新排列后拼接，使得到的数最大，以字符串形式返回。

## A
**思路。** 先全部转成字符串。比较两个串 `a`、`b` 时，若 `a + b` 大于 `b + a`，就让 `a` 排在前面。用 `cmp_to_key` 把比较函数变成 `sorted` 能用的键。排好后拼接；若最前面的串是 `"0"`，说明全是 `0`，只返回 `"0"`。

```python
from functools import cmp_to_key

def largest_number(nums: list[int]) -> str:
    def compare(a: str, b: str) -> int:
        return (b + a > a + b) - (b + a < a + b)     # a+b 更大时 a 排前面，返回负数

    strs = sorted(map(str, nums), key=cmp_to_key(compare))
    return "0" if strs[0] == "0" else "".join(strs)  # 最大的是 0，说明全是 0
```

运行：`[10,2]` → `"210"`，`[3,30,34,5,9]` → `"9534330"`，`[1]` → `"1"`，`[0,0]` → `"0"`，`[3,30]` → `"330"`，`[121,12]` → `"12121"`。

**复杂度。** 时间 `O(n log n · L)`：排序做 `O(n log n)` 次比较，每次拼接比较 `O(L)`（`L <= 10`）；空间 `O(n · L)`。

**写法要点。** Python 3 的 `sorted` 没有 `cmp` 参数，要用 `functools.cmp_to_key`；`(x > y) - (x < y)` 是 Python 里经典的三路比较写法，布尔相减得到 `-1 / 0 / 1`；`map(str, nums)` 惰性转换；`strs[0] == "0"` 只看第一个就够：如果最大的串是 `"0"`，所有数都是 `0`。
