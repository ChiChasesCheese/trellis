---
slug: identify-the-largest-outlier-in-an-array
---
## Q
**LC 3371 识别数组中的最大异常值**｜Medium

`n` 个数里 `n-2` 个是特殊数字，一个是它们的和，一个是异常值（下标不同，值可相同）。返回可能的最大异常值。

## A
**一句话。** 总和 `T = 2·和 + 异常值`，枚举哪个值 `v` 当「和」，异常值就是 `T - 2v`，用计数表查它是否在另一个下标上。

```python
def get_largest_outlier(nums):
    total = sum(nums)
    cnt = Counter(nums)
    ans = -inf
    for v in cnt:                 # v 扮演「和」
        out = total - 2 * v
        if out in cnt and (out != v or cnt[v] > 1):
            ans = max(ans, out)   # 同值要出现两次
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- `out == v` 时没要求出现两次：同一个下标不能既当和又当异常值。
- 枚举异常值再验证剩下的和：也行，但要判断 `(T - out)` 是偶数且 `(T - out)/2` 存在，同样注意同值。

**追问。**
- 为什么不用管哪些是特殊数字？：去掉「和」与异常值，剩下的自动就是特殊数字，它们的和必然等于 `v`。
- 值域只有 `[-1000, 1000]`？：计数表换成偏移数组，常数更小。

**同模式。** LC 1 两数之和、LC 724 寻找数组的中心下标、LC 1991 找到数组的中间位置
