---
slug: binary-tree-right-side-view
---
## Q
**LC 199 二叉树的右视图**｜Medium

站在二叉树右侧，自上而下返回能看到的节点值。

## A
**一句话。** 层序遍历（BFS），每层取最后一个节点。

```python
def right_side_view(root):
    ans = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)      # 这一层最右的节点
        level = [kid for node in level
                 for kid in (node.left, node.right) if kid]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只沿右孩子往下走：`[1,2,3,4,null,null,null,5]` 得 `[1,3]`，应为 `[1,3,4,5]`。
- 空树不处理：`root.val` 对 `None` 报错。

**追问。**
- 左视图怎么改？：把 `level[-1]` 换成 `level[0]`。
- DFS 能做吗？：先右后左，每层第一次到达的节点就是该层最右，用深度判断是否第一次。

**同模式。** LC 102 二叉树的层序遍历、LC 515 在每个树行中找最大值、LC 637 二叉树的层平均值、LC 116 填充每个节点的下一个右侧节点指针
