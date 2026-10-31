---
id: tlc-tt-subarray-max-min-plus-max-4-followup
node: p4.tt-subarray-max-min-plus-max
type: qa
step: 4
---
## Q
**长度至少为 2 的子数组，最大化 min + max**｜追问

面试官接着问：（1）先把暴力解写出来；（2）长度下界改成 `k >= 3`，还能线性吗；（3）数据是流，一个一个到达。

## A
1. **暴力解**：固定左端点，向右扩，滚动维护最小、最大，`O(n^2)`。把下界写成参数 `k`，也正好回答第二问。

```python
def at_least_k(nums: list[int], k: int) -> int:
    best = -(10**18)
    for i in range(len(nums)):
        lo = hi = nums[i]
        for j in range(i + 1, len(nums)):          # 区间 [i, j]，滚动维护最小/最大
            lo, hi = min(lo, nums[j]), max(hi, nums[j])
            if j - i + 1 >= k:
                best = max(best, lo + hi)
    return best
```

`at_least_k([5,12,9,6,4], 2)` → `21`，`at_least_k([5,12,9,6,4], 3)` → `18`，`at_least_k([1,5,1,5,1], 3)` → `6`。
2. **`k >= 3`**：相邻对的论证失效（上面第二个例子里 `k = 3` 的答案是 `18`，不是 `21`），没有这样的化简。要做到比 `O(n^2)` 更快，需要更重的结构，例如对固定长度的窗口用两个单调队列同时给出窗口最小、最大，但「长度至少 `k`」要覆盖所有更长的窗口，面试里通常给出 `O(n^2)` 的滚动解并说明为什么 `k = 2` 特殊就够了。
3. **流式**：只需要保存上一个元素，每来一个新元素就和它相加，更新当前最大和，`O(1)` 空间，每个元素 `O(1)`。

**Python 提醒**：`-(10**18)` 或 `float("-inf")` 都能做最大值的初值；用 `float("-inf")` 时返回类型会混入 `float`，而数据全是整数时，用足够小的整数更干净。暴力解是 `O(n^2)`，`n = 10^5` 时约 `5 * 10^9` 次内层迭代，靠常数优化救不回来。
