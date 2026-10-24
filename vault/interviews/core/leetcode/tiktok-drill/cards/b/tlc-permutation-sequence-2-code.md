---
id: tlc-permutation-sequence-2-code
node: b.permutation-sequence
type: qa
step: 2
---
## Q
**LC 60 排列序列**｜写出 Python 实现

`[1,2,...,n]` 的全部排列按字典序编号，`1 <= n <= 9`，`1 <= k <= n!`。返回第 `k` 个排列，类型是字符串。

## A
**思路。** 保存还没用的数字（升序）。把 `k` 减一变成 `0` 开始的名次。对每一位：后面还剩 `remaining - 1` 位，块大小是 `(remaining-1)!`；`divmod` 得到商 `q`（这一位取剩余数字里第 `q` 小的）和余数（块内名次）；取出该数字并从列表删除。

```python
from math import factorial


def get_permutation(n: int, k: int) -> str:
    digits = list(range(1, n + 1))            # 还没用的数字，始终升序
    k -= 1                                    # 改成 0-based 的名次
    out: list[str] = []
    for remaining in range(n, 0, -1):
        block = factorial(remaining - 1)      # 固定首位后，后面 remaining-1 位的全排列数
        q, k = divmod(k, block)               # q：首位是剩余数字里的第 q 小；k：块内名次
        out.append(str(digits.pop(q)))
    return "".join(out)
```

运行：`(3, 3)` → `"213"`，`(4, 9)` → `"2314"`，`(3, 1)` → `"123"`，`(1, 1)` → `"1"`，`(9, 362880)` → `"987654321"`，`(9, 1)` → `"123456789"`。

**复杂度。** 时间 `O(n^2)`，空间 `O(n)`。

**写法要点。** `math.factorial` 直接调用，`n <= 9` 不需要预处理阶乘表；`q, k = divmod(k, block)` 同时更新商和余数，元组赋值先算右边再赋值，用旧的 `k` 求值；`digits.pop(q)` 一步完成「取出并删除」，保证数字不重复；`range(n, 0, -1)` 里循环变量 `remaining` 就是还没确定的位数；字符串用列表收集再 `"".join`，不在循环里反复拼接。
