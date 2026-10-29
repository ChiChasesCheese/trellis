---
id: tlc-maximum-lcci-4-followup
node: a.maximum-lcci
type: qa
step: 4
---
## Q
**面试题 16.07 最大数值**｜追问

面试官接着问：（1）三个数、一个数组的最大值怎么求？（2）最小值呢？（3）在 Java/C++ 里这个写法有什么坑？

## A
1. **多个数**：两两归约，`reduce(maximum, nums)`。
```python
from functools import reduce

def maximum_of(nums: list[int]) -> int:
    return reduce(maximum, nums)
```
2. **最小值**：`a + b - maximum(a, b)`。
3. **Java/C++**：`a - b` 可能溢出 `int`，符号位就错了。做法一是先转 `long`（差不会溢出 64 位）；做法二是分别取 `a`、`b` 的符号位，同号时用差的符号，异号时直接看谁是负数。右移位数要按位宽写（`>> 63`），且 Java 要用算术右移 `>>` 而不是 `>>>`。

**Python 提醒**：`bool` 是 `int` 的子类，`True * 5 == 5`，所以「布尔值当 0/1 开关」是合法的，但这里的开关只能来自位运算，不能来自比较。
