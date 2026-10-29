---
id: tlc-integer-to-roman-4-followup
node: a.integer-to-roman
type: qa
step: 4
---
## Q
**LC 12 整数转罗马数字**｜追问

面试官接着问：（1）反过来，罗马数字转整数怎么写？（2）不想用 13 项的表，能按十进制位做吗？（3）`num` 超过 3999 怎么办？

## A
1. **转整数**（LC 13）：从左到右扫，当前符号的值比右邻小就减，否则加。
```python
def roman_to_int(s: str) -> int:
    value = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    nums = [value[c] for c in s]
    return sum(-v if v < nxt else v for v, nxt in zip(nums, nums[1:] + [0]))
```
2. **按位查表**：四张 0–9 的表（千、百、十、个位），`T[0][n // 1000] + T[1][n // 100 % 10] + T[2][n // 10 % 10] + T[3][n % 10]`，结果相同，但要手写 40 个字符串。
3. **超过 3999**：标准写法需要上划线记号；只把 `M` 重复，则千位部分用 `"M" * (num // 1000)`，其余照旧。

**Python 提醒**：`zip` 以较短的序列为准，上面给 `nums[1:]` 补一个 `0`，否则最后一个符号会被丢掉。
