---
id: tlc-single-number-2-code
node: p3.single-number
type: qa
step: 2
---
## Q
**LC 136 只出现一次的数字**｜写出 Python 实现

整数数组 `nums`（长度 `1..3 * 10^4`，元素 `-3 * 10^4..3 * 10^4`），一个元素出现一次，其余各出现两次，返回出现一次的那个，线性时间、常数空间。

## A
**思路。** 异或满足交换律和结合律，`x ^ x = 0`，`0 ^ x = x`。从 0 开始把所有数依次异或，成对的数相互抵消，最后剩下落单的数。

```python
def single_number(nums: list[int]) -> int:
    ans = 0
    for x in nums:
        ans ^= x                                     # a ^ a == 0，0 ^ x == x，与顺序无关
    return ans
```

运行：`[2,2,1]` → `1`，`[4,1,2,1,2]` → `4`，`[1]` → `1`，`[-3,5,-3]` → `5`。

**复杂度。** 时间 `O(n)`，一遍扫描；空间 `O(1)`，只有一个整数 `ans`。

**写法要点。** 循环写法最清楚地展示「异或累积」；等价的 `functools.reduce(operator.xor, nums)` 用 `operator.xor` 而不是 `lambda a, b: a ^ b`，少一层 Python 函数调用。Python 的整数是任意精度，负数按无限位补码参与位运算，异或的抵消规律照样成立，不用像 C++ / Java 那样担心 32 位溢出。
