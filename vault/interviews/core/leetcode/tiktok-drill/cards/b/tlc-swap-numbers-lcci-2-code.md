---
id: tlc-swap-numbers-lcci-2-code
node: b.swap-numbers-lcci
type: qa
step: 2
---
## Q
**面试题 16.01 交换数字**｜写出 Python 实现

`numbers = [a, b]`，`-2147483647 <= a, b <= 2147483647`，不使用临时变量（也不用 `a, b = b, a` 的元组交换）交换两个值并返回。

## A
**思路。** 三次异或。第一步 `numbers[0]` 存 `a ^ b`；第二步 `numbers[1] ^ (a ^ b)` 抵消掉 `b` 得到 `a`；第三步 `(a ^ b) ^ a` 得到 `b`。

```python
def swap_numbers(numbers: list[int]) -> list[int]:
    numbers[0] ^= numbers[1]        # numbers[0] = a ^ b
    numbers[1] ^= numbers[0]        # numbers[1] = b ^ (a ^ b) = a
    numbers[0] ^= numbers[1]        # numbers[0] = (a ^ b) ^ a = b
    return numbers
```

运行：`[1,2]` → `[2,1]`，`[-3,5]` → `[5,-3]`，`[7,7]` → `[7,7]`，`[0,-1]` → `[-1,0]`，`[2147483647,-2147483647]` → `[-2147483647,2147483647]`。

**复杂度。** 时间 `O(1)`；空间 `O(1)`。

**写法要点。** `^=` 是就地异或赋值，三行顺序不能换；每行注释写出当前值的代数式，面试时边写边推导；Python 整数对负数按无限位补码做位运算，所以负数也能直接异或，无需掩码。
