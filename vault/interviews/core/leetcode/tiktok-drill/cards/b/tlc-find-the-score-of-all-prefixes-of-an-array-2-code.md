---
id: tlc-find-the-score-of-all-prefixes-of-an-array-2-code
node: b.find-the-score-of-all-prefixes-of-an-array
type: qa
step: 2
---
## Q
**LC 2640 一个数组所有前缀的分数**｜写出 Python 实现

整数数组 `nums`（长度 `1..10^5`，元素 `1..10^9`）。转换数组 `conver[i] = nums[i] + max(nums[0..i])`。返回数组 `ans`，`ans[i]` 是 `nums[0..i]` 的转换数组之和。要求 `O(n)`。

## A
**思路。** 前缀最大值用 `accumulate(nums, max)` 得到；每个位置加上它自己的前缀最大值得到转换数组；再对转换数组做一次 `accumulate`（默认就是求和）。三步都是惰性的，只在最后 `list(...)` 时物化一次。

```python
from itertools import accumulate


def find_prefix_score(nums: list[int]) -> list[int]:
    prefix_max = accumulate(nums, max)                    # 前缀最大值：max(nums[0..i])
    conver = (x + m for x, m in zip(nums, prefix_max))    # 转换数组 conver[i] = nums[i] + max(nums[0..i])
    return list(accumulate(conver))                       # 前缀分数 = conver 的前缀和
```

**运行。** `[2,3,7,5,10]` → `[4, 10, 24, 36, 56]`；`[1,1,2,4,8,16]` → `[2, 4, 8, 16, 32, 64]`；`[5]` → `[10]`；`[3,3,3]` → `[6, 12, 18]`。

**复杂度。** 时间 `O(n)`，每个元素被三个迭代器各经过一次；空间：除返回的列表外只有常数个迭代器，`O(1)`。

**写法要点。** `accumulate(iterable, func)` 的第二个参数是二元函数，传 `max` 就得到前缀最大值，不传就是前缀和；生成器表达式 `(x + m for x, m in zip(...))` 不建中间列表；`zip(nums, prefix_max)` 把两个等长序列按位配对，比下标 `nums[i]`、`pm[i]` 更直接。注意 `accumulate` 返回的是**一次性迭代器**，被 `zip` 消耗完就空了，要复用必须先 `list(...)`。
