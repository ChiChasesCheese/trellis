---
id: tlc-find-maximum-non-decreasing-array-length-0-whole
node: c.find-maximum-non-decreasing-array-length
type: qa
---
## Q
**LC 2945 找出最长非递减数组的长度**｜Hard · LC TikTok 全时段热度 26/100

给你一个下标从 0 开始的整数数组 `nums`。可以执行任意次操作，每次选择一个子数组（连续非空），用它所包含元素的**和**替换这个子数组，例如 `[1,3,5,6]` 选 `[3,5]` 得到 `[1,8,6]`。返回执行任意次操作以后，可以得到的**最长非递减**数组的长度。`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^5`。例：`nums = [5,2,2]` → `1`（只能整体合成 `[9]`）；`nums = [1,2,3,4]` → `4`；`nums = [4,3,2,6]` → `3`（把 `[3,2]` 换成 `[5]` 得 `[4,5,6]`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把数组切成尽量多的连续段，使段和非递减；`f[i]` 是前 `i` 个数最多能切几段，转移时在所有「上一段和 `<=` 本段和」的分割点里取**最右**的一个，可行性随 `i` 单调，用单调队列把 `O(n²)` 降到 `O(n)`。

**识别。** 「用子数组的和替换」等价于「把数组切成连续段，每段变成它的和」，所以问题是切成段和非递减的最多段数。前缀和 + DP，并且「合法的分割点集合随右端点单调」是用单调队列的信号。

**推导。** 设前缀和 `s`，`f[i]` 为前 `i` 个数的最大段数，`last[i]` 为取到 `f[i]` 时最后一段的最小和。从 `j` 转移到 `i`（最后一段是 `nums[j:i]`，和为 `s[i] - s[j]`）需要上一段和 `last[j] <= s[i] - s[j]`，即 `s[j] + last[j] <= s[i]`。两个事实：`f` 随 `i` 不减，所以可行的 `j` 里**越大越好**（段数不少，且最后一段和更小，利于后续）；`s[j] + last[j]` 作为 `j` 的函数在队列里可保持递增，`s[i]` 又在增大，所以队首只会被弹出、不会回头。每个下标入队、出队各一次。

**简单解法。** 同样的 DP，但每个 `i` 从右往左线性找第一个可行的 `j`。

```python
def find_maximum_length_quadratic(nums: list[int]) -> int:
    n = len(nums)
    s = [0] * (n + 1)                            # 前缀和
    for i, x in enumerate(nums):
        s[i + 1] = s[i] + x
    f = [0] * (n + 1)                            # f[i]：前 i 个数最多切几段
    last = [0] * (n + 1)                         # last[i]：取到 f[i] 时最后一段的和
    for i in range(1, n + 1):
        for j in range(i - 1, -1, -1):           # 最右的可行分割点最优
            if s[j] + last[j] <= s[i]:
                f[i] = f[j] + 1
                last[i] = s[i] - s[j]
                break
    return f[n]
```

`O(n²)`，`n = 10^5` 会超时；正确性依赖「取最右的可行 `j`」。

最优解：

```python
from collections import deque
from itertools import accumulate


def find_maximum_length(nums: list[int]) -> int:
    n = len(nums)
    s = list(accumulate(nums, initial=0))        # s[i]：前 i 个数的和
    f = [0] * (n + 1)                            # f[i]：前 i 个数最多切几段
    last = [0] * (n + 1)                         # last[i]：取到 f[i] 时最后一段的最小和
    q = deque([0])                               # 候选分割点，s[j] + last[j] 严格递增
    for i in range(1, n + 1):
        while len(q) > 1 and s[q[1]] + last[q[1]] <= s[i]:
            q.popleft()                          # 次队首也可行，说明队首不是最右的可行点
        j = q[0]                                 # 最右的可行分割点
        f[i] = f[j] + 1
        last[i] = s[i] - s[j]
        while q and s[q[-1]] + last[q[-1]] >= s[i] + last[i]:
            q.pop()                              # 队尾的 key 不比 i 小：i 更靠右且 key 更小，队尾被淘汰
        q.append(i)
    return f[n]
```

运行：`[5,2,2]` → `1`，`[1,2,3,4]` → `4`，`[4,3,2,6]` → `3`；`[7]` → `1`，`[3,3]` → `2`，`[2,1]` → `1`，`[1] * 100000` → `100000`。

**复杂度。** 时间 `O(n)`（每个下标最多入队、出队各一次），空间 `O(n)`。

**拓展优化。**
- 还原具体的切法：记录每个 `i` 的前驱 `pre[i] = j`，最后从 `n` 倒着取段。

```python
def find_maximum_length_parts(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    s = list(accumulate(nums, initial=0))
    last = [0] * (n + 1)
    pre = [0] * (n + 1)                          # pre[i]：最后一段 nums[pre[i]:i] 的起点
    q = deque([0])
    for i in range(1, n + 1):
        while len(q) > 1 and s[q[1]] + last[q[1]] <= s[i]:
            q.popleft()
        pre[i] = q[0]
        last[i] = s[i] - s[pre[i]]
        while q and s[q[-1]] + last[q[-1]] >= s[i] + last[i]:
            q.pop()
        q.append(i)
    parts: list[list[int]] = []
    i = n
    while i:                                     # 从末尾倒着沿 pre 取出每一段
        parts.append(nums[pre[i]:i])
        i = pre[i]
    return parts[::-1]
```

**易错点。**
- 取最左的可行 `j` 而不是最右：段数偏少，`[1,2,3,4]` 会得到 `1`，正确是 `4`。
- 条件写成 `<` 而不是 `<=`：非递减允许相等，`[3,3]` 得到 `1`，正确是 `2`。
- 弹队首只弹一个：要 `while` 一直弹到次队首不可行为止。

**追问。**
- 严格递增（`<`）：条件改成 `s[j] + last[j] < s[i]`，其余不变。
- 最少合并次数：`n - f[n]`。

**同模式。** LC 300 最长递增子序列、LC 1425 带限制的子序列和、LC 239 滑动窗口最大值、LC 862 和至少为 K 的最短子数组、LC 1696 跳跃游戏 VI。
