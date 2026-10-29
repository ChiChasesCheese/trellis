---
id: tlc-longest-subarray-of-1s-after-deleting-one-element-4-followup
node: b.longest-subarray-of-1s-after-deleting-one-element
type: qa
step: 4
---
## Q
**LC 1493 删掉一个元素以后全为 1 的最长子数组**｜追问

面试官接着问：（1）改成**最多删 `k` 个**元素？（2）数据以流的形式逐个到达，只能 `O(1)` 空间？（3）要返回被删元素的下标？分别怎么改。

## A
1. **最多删 `k` 个**：删 `1` 没有意义，所以等价于「窗口里至多 `k` 个 `0`」，删掉它们后窗口里剩下的 `1` 就是答案。把阈值改成 `k`，答案取 `窗口长度 - zeros`：

```python
def longest_ones_after_deleting(nums: list[int], k: int) -> int:
    left = zeros = best = 0
    for right, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1 - zeros)   # 窗口里 1 的个数
    return best
```

   这里是「至多」删 `k` 个，`k = 1` 且数组全是 `1` 时返回 `n`；原题「必须删」才多减 `1`。
2. **流式 `O(1)` 空间**：只记上一段连续 `1` 的长度 `prev` 和当前段 `cur`，遇到 `0` 时 `prev, cur = cur, 0`，每步用 `prev + cur` 更新答案；最后若整个数组没有 `0`，答案是 `n - 1`。
3. **返回下标**：窗口里最多一个 `0`，用一个变量 `zero_at` 记录窗口内 `0` 的位置；取得新最大值时一并记下，没有 `0` 时任选一个下标。

**Python 提醒**：`zeros += x == 0` 依赖 `bool` 是 `int` 子类，`True + 0 == 1`；若 `nums` 来自 `numpy` 布尔数组，写成 `int(x == 0)` 更稳妥。
