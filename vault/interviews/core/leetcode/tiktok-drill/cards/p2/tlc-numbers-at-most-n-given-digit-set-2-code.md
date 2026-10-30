---
id: tlc-numbers-at-most-n-given-digit-set-2-code
node: p2.numbers-at-most-n-given-digit-set
type: qa
step: 2
---
## Q
**LC 902 最大为 N 的数字组合**｜写出 Python 实现

`digits` 是按非递减顺序排列的字符数组（`1 <= digits.length <= 9`，元素是 `'1'` 到 `'9'` 且互不相同），每个数字可无限次使用。返回能拼出的、`<= n` 的正整数个数，`1 <= n <= 10^9`。

## A
**思路。** 设 `L` 是 `n` 的位数，`d = len(digits)`。位数少于 `L` 的数各位随便选，个数 `Σ d^len`。位数等于 `L` 的数逐位贴着 `n`：第 `i` 位选更小的数字，后面随便选；选等于 `n[i]` 才能继续贴着，`n[i]` 不在 `digits` 里就停下；全部贴住则 `n` 自己也可写，加 `1`。

```python
from bisect import bisect_left


def at_most_n_given_digit_set(digits: list[str], n: int) -> int:
    s, size = str(n), len(digits)
    total = sum(size ** length for length in range(1, len(s)))   # 位数比 n 少的：随便填
    for i, ch in enumerate(s):                                   # 位数和 n 相同：逐位贴着 n 走
        total += bisect_left(digits, ch) * size ** (len(s) - 1 - i)   # 这一位选比 ch 小的，后面随便填
        if ch not in digits:
            return total                                         # 贴不住了，后面没有“等于 n”的数
    return total + 1                                             # 每一位都贴住：n 自己也能写
```

运行：`(["1","3","5","7"], 100)` → `20`，`(["1","4","9"], 10**9)` → `29523`，`(["7"], 8)` → `1`，`(["7"], 77)` → `2`，`(list("123456789"), 10**9)` → `435848049`，`(["3"], 1)` → `0`。

**复杂度。** 时间 `O(L · d)`：`L <= 10` 位，每位一次 `bisect_left` 和一次成员检查（列表长度至多 `9`）；空间 `O(L)`（字符串 `s`）。

**写法要点。** `bisect_left(digits, ch)` 直接返回“比 `ch` 小的数字有几个”，前提是 `digits` 有序且是等长单字符，字符串比较与数值比较一致；`enumerate(s)` 同时拿下标与字符；`size ** length` 是精确整数幂，没有浮点误差；`for` 里提前 `return` 表示贴不住，循环自然跑完才加 `1`，不需要布尔标记。
