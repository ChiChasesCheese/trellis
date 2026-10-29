---
id: tlc-contiguous-array-4-followup
node: b.contiguous-array
type: qa
step: 4
---
## Q
**LC 525 连续数组**｜追问

面试官接着问：（1）要返回子数组本身怎么办？（2）条件改成「和为 `k` 的最长子数组」或「和为 `k` 的子数组**个数**」呢？（3）能不能不用字典？

## A
1. **返回子数组**：更新答案时同时记左端点，`if i - first[bal] > best: best, start = i - first[bal], first[bal] + 1`，最后返回 `nums[start : start + best]`。
2. **和为 `k`**：子数组 `(j, i]` 的和是 `pre[i] - pre[j]`，所以查 `pre - k` 而不是 `pre` 本身；最长仍只记最早下标。求**个数**（LC 560）时字典改存出现次数，每步 `count += seen[pre - k]`，再 `seen[pre] += 1`，用 `Counter` 或 `defaultdict(int)`。
3. **不用字典**：`bal` 只能在 `-n..n` 之间，开 `first = [None] * (2 * n + 1)`，用 `bal + n` 当下标。复杂度不变，常数更小；但前缀和值域大（一般整数数组）时只能用字典。

**Python 提醒**：`defaultdict(int)` 读一个不存在的键会**插入**这个键；只想查询时用 `d.get(key, 0)`，否则字典会被查询撑大。
