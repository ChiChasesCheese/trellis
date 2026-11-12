---
slug: maximum-subarray-sum-with-one-deletion
---
## Q
**LC 1186 删除一次得到子数组最大和**｜Medium

整数数组 `arr`，选一个非空子数组并至多删掉其中一个元素（删后仍非空），求最大和。

## A
**一句话。** Kadane 加一维状态：`keep` 是以 `i` 结尾没删过的最大和，`skip` 是至多删过一个的最大和。

```python
def maximum_sum(arr):
    keep = skip = best = arr[0]
    for x in arr[1:]:
        # skip: 延续 / 删掉 x（取旧 keep）/ 从 x 重新开始
        skip, keep = (max(skip + x, keep, x),
                      max(keep, 0) + x)
        best = max(best, keep, skip)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 答案与 `0` 取 max：`[-1,-1,-1,-1]` 应为 `-1`，删后不能为空。
- 先找 Kadane 最大子数组再删最小负数：`[1,-4,1]` 应为 `2`，最大子数组 `[1]` 里没有可删的。
- 先更新 `keep` 再算 `skip`：「删 `x`」用到了含 `x` 的 `keep`，`[1,-5,1]` 得 `1`，应为 `2`。

**追问。**
- 最多删 `k` 个？：状态加一维 `dp[j]`，总 `O(nk)`。
- 前后缀怎么做？：`left[i]` 以 `i` 结尾、`right[i]` 以 `i` 开头，删 `i` 得 `left[i-1] + right[i+1]`，取与 `max(left)` 的较大者。

**同模式。** LC 53 最大子数组和、LC 152 乘积最大子数组、LC 918 环形子数组的最大和、LC 1749 任意子数组和的绝对值的最大值
