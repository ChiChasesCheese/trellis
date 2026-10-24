---
id: tlc-patterns-math-bit-sim-4-bits
node: patterns.math-bit-sim
type: qa
step: 4
---
## Q
**数学、位运算与模拟｜位运算工具箱：lowbit、异或、位掩码子集、原地标记**

`n & (n - 1)` 和 `n & -n` 各做什么？位掩码怎样枚举子集？怎样不用额外空间找数组中出现两次的数？

## A
```python
print(12 & (12 - 1), 12 & -12, (12).bit_count(), bin(12))   # 8 4 2 0b1100
```

| 表达式 | 作用 |
|---|---|
| `n & (n - 1)` | 清掉最低位的 1（`12 = 1100` → `1000`） |
| `n & -n` | 只保留最低位的 1（lowbit，`12` → `4`） |
| `n > 0 and n & (n - 1) == 0` | 判断是不是 2 的幂 |
| `a ^ a = 0`，`a ^ 0 = a` | 成对的数异或抵消，剩下只出现一次的数 |
| `mask >> i & 1` | 取第 `i` 位 |

**位掩码枚举子集**（元素数 `<= 20`）：

```python
def subsets_mask(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]
print(subsets_mask([1, 2, 3]))   # [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

**原地标记找重复（LC 442）**：数组长 `n`，值在 `1..n`，每个数出现一次或两次。把值 `x` 对应的下标 `x - 1` 处的数取负；再次遇到该位置已是负数，说明 `x` 出现了第二次。

```python
def find_duplicates(nums: list[int]) -> list[int]:
    res: list[int] = []
    for x in nums:
        i = abs(x) - 1                     # 值 x 对应下标 x - 1（取绝对值：这个位置可能已被标记）
        if nums[i] < 0:
            res.append(abs(x))
        else:
            nums[i] = -nums[i]
    return res
print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]), find_duplicates([1, 1, 2]))   # [2, 3] [1]
```

- 时间 `O(n)`，额外空间 `O(1)`（修改了输入）。
- 异或求单个数 `reduce(xor, nums)`：`[4,1,2,1,2]` → `4`。
- Python 整数是任意精度，右移不会有符号位问题；`~n` 是 `-n - 1`，不是"按位取反的 32 位无符号数"。
