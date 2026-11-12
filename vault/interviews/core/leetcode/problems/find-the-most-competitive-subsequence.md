---
slug: find-the-most-competitive-subsequence
---
## Q
**LC 1673 找出最具竞争力的子序列**｜Medium

数组 `nums` 和正整数 `k`，返回长度为 `k` 的字典序最小的子序列。

## A
**一句话。** 单调栈，新数比栈顶小且还有丢弃额度（`n-k`）就弹栈，最后取前 `k` 个。

```python
def most_competitive(nums, k):
    drop = len(nums) - k    # 还能丢几个
    stack = []
    for x in nums:
        while drop and stack and stack[-1] > x:
            stack.pop()
            drop -= 1
        stack.append(x)
    return stack[:k]        # 额度没用完就截掉末尾
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 没有丢弃额度的限制：`[3,1]`、`k=2` 会弹掉 `3`，只剩 `[1]`，长度不够。
- 忘了截取到 `k`：`[1,2,3,4]`、`k=2` 一个也不弹，栈里是 `[1,2,3,4]`。
- 弹栈用 `>=`：`[0,0,1]`、`k=2` 得 `[0,1]`，应为 `[0,0]`，要严格 `>`。

**追问。**
- 要字典序最大呢？：比较反过来，`stack[-1] < x`。
- 去重加限制（LC 316）？：加 `in_stack` 集合和「后面是否还有」的计数。

**同模式。** LC 402 移掉 K 位数字、LC 316 去除重复字母、LC 321 拼接最大数、LC 84 柱状图中最大的矩形
