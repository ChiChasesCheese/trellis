---
id: tlc-house-robber-4-followup
node: p2.house-robber
type: qa
step: 4
---
## Q
**LC 198 打家劫舍**｜追问

面试官接着问：（1）房屋围成一圈，首尾相邻（LC 213）？（2）要输出具体偷了哪几间房？（3）房屋排成二叉树（LC 337）？

## A
1. **环形。** 首尾不能同时偷：分成“不偷第一间”和“不偷最后一间”两个线性问题，取较大者；只有一间房时单独返回。
```python
def rob_circle(nums: list[int]) -> int:
    def line(a: list[int]) -> int:
        skip = take = 0
        for x in a:
            skip, take = max(skip, take), skip + x
        return max(skip, take)

    if len(nums) == 1:
        return nums[0]
    return max(line(nums[1:]), line(nums[:-1]))
```
`[2,3,2]` → `3`，`[1,2,3,1]` → `4`，`[5]` → `5`。
2. **输出方案。** 从右往左填 `dp[i] = max(dp[i+1], nums[i] + dp[i+2])`（多开两格哨兵），再从左往右回溯：若 `nums[i] + dp[i+2] == dp[i]` 就选 `i` 并跳到 `i + 2`，否则 `i + 1`。`[2,7,9,3,1]` 得到总额 `12`、下标 `[0, 2, 4]`。
3. **二叉树。** 后序遍历，每个节点返回二元组 `(偷该节点的最优, 不偷该节点的最优)`：偷它则两个孩子都只能取“不偷”，不偷它则两个孩子各自取两者较大。时间 `O(n)`。

**Python 提醒**：切片 `nums[1:]`、`nums[:-1]` 会复制一份列表（`O(n)` 空间），数组很大时可以让 `line` 接收 `lo, hi` 下标避免复制；另外记忆化递归版本用 `functools.cache` 一行就能加上，递归深度等于 `n`，`n = 100` 时没有问题。
