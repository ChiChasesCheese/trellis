---
slug: house-robber-iii
---
## Q
**LC 337 打家劫舍 III**｜Medium

房子排成二叉树，不能偷直接相连（父子）的两间，求能偷到的最高金额。

## A
**一句话。** 树形 DP：每个节点返回（偷它的最优，不偷它的最优），偷则孩子必须不偷，不偷则孩子各取较优。

```python
def rob(root):
    def go(node):                # (偷 node, 不偷 node) 的子树最优
        if not node:
            return 0, 0
        take_l, skip_l = go(node.left)
        take_r, skip_r = go(node.right)
        take = node.val + skip_l + skip_r
        skip = max(take_l, skip_l) + max(take_r, skip_r)
        return take, skip
    return max(go(root))
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 不偷根时孩子也强制不偷：`[3,4,5,1,3,null,1]` 得 `3`，应为 `9`。
- 按层奇偶贪心：`[2,1,3,null,4]` 得 `6`，应为 `7`。
- 链状树深 `10^4` 会 `RecursionError`，要调大递归上限。

**追问。**
- 要返回具体偷了哪些？：自顶向下回溯，偷了父亲则孩子走不偷分支。
- 房子围成环（LC 213）？：断环，分别算「不含首」与「不含尾」两条链取较大。

**同模式。** LC 198 打家劫舍、LC 213 打家劫舍 II、LC 124 二叉树中的最大路径和、LC 968 监控二叉树
