---
id: tlc-shuffle-an-array-2-code
node: a.shuffle-an-array
type: qa
step: 2
---
## Q
**LC 384 打乱数组**｜写出 Python 实现

实现类 `Solution(nums)`（元素互不相同，长度 `1` 到 `50`）：`reset()` 返回初始数组，`shuffle()` 返回一个等概率的随机排列；两个方法最多共调用 `10^4` 次。不要直接调用 `random.shuffle`。

## A
**思路。** 构造时存一份原数组副本。`shuffle` 拷贝一份，从左到右对每个位置 `i`，在 `[i, n)` 里等概率选 `j`，交换 `arr[i]` 与 `arr[j]`。

```python
import random


class Solution:
    def __init__(self, nums: list[int]) -> None:
        self.original = nums[:]                 # 存一份副本，reset 永远拿得回初始状态

    def reset(self) -> list[int]:
        return self.original[:]

    def shuffle(self) -> list[int]:
        arr = self.original[:]                  # 每次在新列表上洗，调用方拿到的结果互不影响
        n = len(arr)
        for i in range(n - 1):
            j = random.randrange(i, n)          # 从「还没定下来」的 [i, n) 里等概率挑一个放到位置 i
            arr[i], arr[j] = arr[j], arr[i]
        return arr
```

运行：`Solution([1,2,3])`：`reset()` → `[1, 2, 3]`；`shuffle()` 返回 `[1,2,3]` 的某个排列，6 种排列的概率都是 `1/6`；连续两次 `shuffle()` 返回两个独立的列表。

**复杂度。** `shuffle` 时间 `O(n)`：一次拷贝加 `n - 1` 次交换；`reset` 时间 `O(n)`（拷贝）；空间 `O(n)`。

**写法要点。** `random.randrange(i, n)` 是左闭右开，与 `range` 一致，不像 `random.randint(i, n - 1)` 要记得减一；`nums[:]` 浅拷贝整数列表足够；`arr[i], arr[j] = arr[j], arr[i]` 用元组交换；循环到 `n - 2` 为止，最后一位只剩一个选择，换不换都一样。
