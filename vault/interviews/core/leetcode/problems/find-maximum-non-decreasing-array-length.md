---
slug: find-maximum-non-decreasing-array-length
---
## Q
**LC 2945 找出最长非递减数组的长度**｜Hard

可以多次把一个连续子数组替换成它的和。求能得到的最长非递减数组的长度。

## A
**一句话。** 切成段和非递减的最多段：`f[i]` 取最右可行分割点，用单调队列优化到线性。

```python
def find_maximum_length(nums):
    n = len(nums)
    s = list(accumulate(nums, initial=0))
    f = [0] * (n + 1)      # f[i]：前 i 个数最多切几段
    last = [0] * (n + 1)   # 取到 f[i] 时最后一段的最小和
    q = deque([0])         # s[j]+last[j] 严格递增
    for i in range(1, n + 1):
        while len(q) > 1 and s[q[1]] + last[q[1]] <= s[i]:
            q.popleft()    # 次队首也可行，队首不是最右
        j = q[0]
        f[i] = f[j] + 1
        last[i] = s[i] - s[j]
        key = s[i] + last[i]
        while q and s[q[-1]] + last[q[-1]] >= key:
            q.pop()        # i 更靠右且 key 更小
        q.append(i)
    return f[n]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 取最左的可行 `j`：段数偏少，`[1,2,3,4]` 得 `1`，应为 `4`。
- 条件写成 `<`：非递减允许相等，`[3,3]` 得 `1`，应为 `2`。
- 队首只弹一次：要 `while` 弹到次队首不可行为止。

**追问。**
- 为什么只看最右的可行点？：段数随 `j` 单调不降，且越靠右，最后一段和越小，对后面越有利。
- 改成严格递增？：条件改成 `s[j] + last[j] < s[i]`，其余不变。

**同模式。** LC 300 最长递增子序列、LC 239 滑动窗口最大值、LC 862 和至少为 K 的最短子数组、LC 1696 跳跃游戏 VI
