---
id: tlc-adding-two-negabinary-numbers-4-followup
node: a.adding-two-negabinary-numbers
type: qa
step: 4
---
## Q
**LC 1073 负二进制数相加**｜追问

面试官接着问：（1）把一个十进制整数转成负二进制（LC 1017）？（2）推广到任意基数 `b`，包括负基数？（3）你怎么确认结果是对的？

## A
1. **十进制转负二进制**：反复取最低位、再除以 -2。`n & 1` 是最低位，`n = -(n >> 1)` 是 `(n - 最低位) / -2`。`n = 0` 时返回 `[0]`。

```python
def to_negabinary(n: int) -> list[int]:
    if n == 0:
        return [0]
    digits: list[int] = []
    while n:
        digits.append(n & 1)
        n = -(n >> 1)                  # (n - 最低位) / (-2)
    return digits[::-1]
```

运行：`2` → `[1,1,0]`，`3` → `[1,1,1]`，`-3` → `[1,1,0,1]`。

2. **任意基数 `b`**：本位取非负余数 `d = x % abs(b)`，进位 `(x - d) // b`（整除）。`b = -2` 时就是上面的公式；`b = 10` 时就是普通竖式加法。
3. **确认结果**：写一个 `to_int(arr)`，从高位起 `v = v * -2 + d`，检查 `to_int(结果) == to_int(arr1) + to_int(arr2)`，再检查没有前导零。

**Python 提醒**：Python 的 `%` 和 `//` 向下取整，`-1 % 2 == 1`、`-1 // 2 == -1`；C++ / Java 向零截断，`-1 % 2 == -1`。把这类进位公式移植到其他语言时，要先把余数调成非负。
