---
slug: adding-two-negabinary-numbers
---
## Q
**LC 1073 负二进制数相加**｜Medium

两个以 `-2` 为基数的数用 0/1 数组表示（高位在前，无前导零），返回它们的和的同样表示。

## A
**一句话。** 像二进制竖式从低位相加，进位改为 `-(x >> 1)`，最后去前导零。

```python
def add_negabinary(arr1, arr2):
    out, carry = [], 0      # 进位只会是 -1、0、1
    for a, b in zip_longest(reversed(arr1), reversed(arr2),
                            fillvalue=0):
        x = a + b + carry
        out.append(x & 1)   # 本位
        carry = -(x >> 1)   # 同位的 2 = 高一位的 -1
    while carry:
        out.append(carry & 1)
        carry = -(carry >> 1)
    while len(out) > 1 and out[-1] == 0:   # 去前导零
        out.pop()
    return out[::-1]
```

**复杂度。** 时间 `O(max(m, n))`，空间 `O(max(m, n))`。

**易错点。**
- 照搬二进制进位 `x >> 1`：`[1] + [1]` 得 `[1,0]`（`-2`），应为 `[1,1,0]`（`2`）。
- 忘了去前导零：`[1,1] + [1]` 得 `[0,0]`，应为 `[0]`。
- 用 `%` 和 `/` 处理负进位：C++/Java 里 `-1 % 2 == -1`，会出错；位运算对负数成立。

**追问。**
- 十进制转负二进制（LC 1017）？：反复取 `n & 1`，`n = -(n >> 1)`，直到 `n == 0`。
- 任意负基数 `b`？：本位取非负余数 `d = x mod |b|`，进位 `(x - d) / b`。

**同模式。** LC 67 二进制求和、LC 415 字符串相加、LC 2 两数相加、LC 1017 负二进制转换
