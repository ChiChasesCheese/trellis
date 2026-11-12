---
slug: find-largest-value-in-each-tree-row
---
## Q
**LC 515 在每个树行中找最大值**｜Medium

返回二叉树每一层节点值的最大值，从上到下。

## A
**一句话。** 层序遍历，每次取整层的 `max`，再用推导式生成下一层的所有非空孩子。

```python
def largest_values(root):
    ans = []
    level = [root] if root else []
    while level:
        ans.append(max(node.val for node in level))
        level = [c for node in level
                 for c in (node.left, node.right) if c]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(w)`。

**易错点。**
- 每层最大值初值写 `0`：`[-3,-5]` 得 `[0,0]`，应为 `[-3,-5]`，要对整层取 `max`。
- 空树调用 `max` 抛 `ValueError`：入口判空返回 `[]`。

**追问。**
- 用 DFS 怎么做？：带深度，`depth == len(ans)` 时追加，否则 `ans[depth] = max(ans[depth], val)`。
- 同一框架还能做什么？：右视图（LC 199，取每层最后一个）、层平均值（LC 637）。

**同模式。** LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 637 二叉树的层平均值、LC 111 二叉树的最小深度
