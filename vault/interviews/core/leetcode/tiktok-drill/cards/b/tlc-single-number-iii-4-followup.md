---
id: tlc-single-number-iii-4-followup
node: b.single-number-iii
type: qa
step: 4
---
## Q
**LC 260 只出现一次的数字 III**｜追问

面试官接着问：（1）如果有**三个**落单数怎么办？（2）去掉空间限制，最直白的写法？（3）元素不是 32 位整数、而是任意大的整数时还成立吗？

## A
1. **三个落单数**：异或后得到 `a ^ b ^ c`，一个等式，一位也不能保证分开三个数，位运算分组不再可行。常见的退路是哈希计数（`O(n)` 空间），或排序后扫描（`O(n log n)`）。
2. **不限空间**：计数最直白，不用想位运算。
```python
from collections import Counter

def single_number_iii_counter(nums: list[int]) -> list[int]:
    return [v for v, c in Counter(nums).items() if c == 1]
```
`[1,2,1,3,2,5]` 得 `[3, 5]`。面试里先讲这个再提位运算，说明为什么能把空间降到 `O(1)`。
3. **大整数**：Python 整数任意精度，异或、`x & -x` 对任意大的整数成立，逻辑不变；在 C++ / Java 里 `x & -x` 对 `INT_MIN` 会溢出，要先转成 64 位 `long`。

**Python 提醒**：`Counter.items()` 的遍历顺序是插入顺序，返回结果的先后顺序取决于首次出现的位置，所以与位运算版的返回顺序可能不同；题目允许任意顺序，但自己写测试时要排序后再比较。
