---
id: tlc-shuffle-an-array-0-whole
node: a.shuffle-an-array
type: qa
---
## Q
**LC 384 打乱数组**｜Medium · CodeTop 国内累计 7 次 · 最近 2026-06-19（CodeTop）

给一个元素互不相同的整数数组 `nums`，设计类 `Solution`：`Solution(nums)` 用 `nums` 初始化；`reset()` 把数组恢复到初始状态并返回；`shuffle()` 返回随机打乱后的数组，**所有排列出现的概率相等**。`1 <= nums.length <= 50`，`-10^6 <= nums[i] <= 10^6`，元素互不相同，`reset` 和 `shuffle` 最多共调用 `10^4` 次。例：`Solution([1,2,3])`，`shuffle()` 可能返回 `[3,1,2]`，`reset()` 返回 `[1,2,3]`，再 `shuffle()` 可能返回 `[1,3,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** Fisher–Yates 洗牌（Knuth shuffle）：从左到右，第 `i` 位从还没定下来的 `[i, n)` 里等概率挑一个换过来；所有随机选择共 `n!` 种、等可能，恰好一一对应 `n!` 个排列。每次 `O(n)`。

**识别。** 「所有排列等概率」→ 要的是均匀随机排列，标准答案是 Fisher–Yates。「reset」→ 必须另存一份原数组。`n <= 50`、调用 `10^4` 次 → 每次 `O(n)` 足够。

**推导。** 暴力：生成全部 `n!` 个排列再随机挑一个，`n = 50` 不可能。退一步：每次从剩余元素里随机抽一个拿出来（`pool.pop(random.randrange(len(pool)))`），结果是均匀的，但从列表中间 `pop` 是 `O(n)`，总共 `O(n^2)`。Fisher–Yates 的关键是把「剩余元素」就地放在数组后段 `[i, n)`，抽中的那个与位置 `i` 交换，`O(1)` 完成「抽出」，总共 `O(n)`。

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

**复杂度。** `shuffle` 和 `reset` 都是时间 `O(n)`（复制加一趟交换）；空间 `O(n)`：原数组副本和返回的新列表。

**易错点。**
- 每一位都从整个数组里挑（`j = random.randrange(n)`）：随机选择共 `n^n` 种，不能被 `n!` 整除，必然不均匀。`n = 3` 时 27 种选择里，`[1,2,3]`、`[3,1,2]`、`[3,2,1]` 各占 `4/27`，另外三个排列各占 `5/27`。
- 在同一个列表上就地洗并返回它：`a = s.shuffle(); b = s.shuffle()` 时 `a is b`，第一次的结果被第二次悄悄改掉。
- `random.shuffle(arr)` 就地打乱、返回 `None`，写 `return random.shuffle(arr)` 得到 `None`。

**追问。**
- 为什么均匀：元素 `x` 落在位置 `i` 的概率 = 前 `i` 步都没选中它 × 第 `i` 步选中它 = `(n-1)/n · (n-2)/(n-1) · … · 1/(n-i) = 1/n`。
- 只给 `random.random()`：`j = i + int(random.random() * (n - i))`。
- 数据是流、长度未知，要等概率抽 `k` 个：蓄水池抽样（reservoir sampling），第 `t` 个元素以 `k/t` 的概率换进池子。

**同模式。** LC 382 链表随机节点、LC 398 随机数索引、LC 528 按权重随机选择、LC 470 用 Rand7() 实现 Rand10()。
