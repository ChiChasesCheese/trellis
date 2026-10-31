---
id: tlc-find-the-most-competitive-subsequence-4-followup
node: b.find-the-most-competitive-subsequence
type: qa
step: 4
---
## Q
**LC 1673 找出最具竞争力的子序列**｜追问

面试官接着问：（1）改成字典序**最大**的子序列？（2）两个数组各取一部分拼成最大的 `k` 位数（LC 321）？（3）能不能用另一种弹栈条件，不预先算额度？

## A
1. **最大**：弹栈条件改成 `stack[-1] < x`，其余不变。
2. **LC 321**：枚举从第一个数组取 `i` 个、第二个取 `k - i` 个；每个数组各用上面的单调栈求「长度固定的最大子序列」，再把两个序列按字典序**贪心合并**（比较剩余部分，而不是只比较当前元素），所有切分里取最大，复杂度约 `O(k · (m + n + k))`。
3. **不预先算额度**：弹栈条件写成 `stack and stack[-1] > x and len(stack) + (n - i) > k`，意思是「弹掉之后，剩下的元素还够凑满 `k` 个」；入栈时加 `if len(stack) < k`，保证长度不超过 `k`。结果与预算版相同，不需要最后截取，写法更接近 LC 官方题解。

**Python 提醒**：`stack[:k]` 会新建一个列表（`O(k)`）；如果必须原地，可以 `del stack[k:]`。`while drop and stack and stack[-1] > x` 中 `drop` 是整数，`0` 为假，这是 Python 里「计数器兼开关」的常用写法。
