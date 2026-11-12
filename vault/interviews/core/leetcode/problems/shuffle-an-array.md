---
slug: shuffle-an-array
---
## Q
**LC 384 打乱数组**｜Medium

设计类：`reset()` 恢复初始数组，`shuffle()` 返回随机打乱的数组，所有排列等概率。

## A
**一句话。** Fisher–Yates 洗牌：第 `i` 位从尚未定下的 `[i, n)` 里等概率挑一个换过来。

```python
class Solution:
    def __init__(self, nums):
        self.original = nums[:]     # 存副本，reset 才拿得回

    def reset(self):
        return self.original[:]

    def shuffle(self):
        arr = self.original[:]      # 每次在新列表上洗
        n = len(arr)
        for i in range(n - 1):
            j = random.randrange(i, n)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 每位都从整个数组挑（`randrange(n)`）：共 `n^n` 种选择不能被 `n!` 整除，必不均匀，`n=3` 时部分排列占 `5/27`，部分占 `4/27`。
- 在同一列表上洗并返回它：两次 `shuffle()` 的结果是同一个对象，前一次被悄悄改掉。
- `return random.shuffle(arr)`：它就地打乱并返回 `None`。

**追问。**
- 为什么均匀？：元素落在位置 `i` 的概率是 `(n-1)/n · (n-2)/(n-1) · … · 1/(n-i) = 1/n`。
- 数据是流、长度未知，等概率抽 `k` 个？：蓄水池抽样，第 `t` 个元素以 `k/t` 的概率换进池子。

**同模式。** LC 382 链表随机节点、LC 398 随机数索引、LC 528 按权重随机选择、LC 470 用 Rand7() 实现 Rand10()
