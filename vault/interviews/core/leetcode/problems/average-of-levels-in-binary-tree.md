---
slug: average-of-levels-in-binary-tree
---
## Q
**LC 637 二叉树的层平均值**｜Easy

返回二叉树每一层节点值的平均值。

## A
**一句话。** BFS 每层开始前记下队列长度 `size`，恰好弹出 `size` 个节点求和，平均值是和除以 `size`。

```python
def average_of_levels(root):
    ans, q = [], deque([root])
    while q:
        size = len(q)       # 此刻队列里恰好是一整层
        total = 0
        for _ in range(size):
            node = q.popleft()
            total += node.val
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        ans.append(total / size)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 边弹边入队时反复读 `len(q)`：队列长度在变，相邻两层混在一起，`size` 必须先存下来。
- 用整数除法 `//`：`[3,9,20,15,7]` 得 `[3,14,11]`，应为 `[3.0,14.5,11.0]`。

**追问。**
- Java / C++ 要注意什么？：节点值是 32 位整数，一层的和会溢出 `int`，累加要用 `long` 或 `double`。
- 想用 DFS？：带深度参数，用两个数组分别累加每层的和与个数。

**同模式。** LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 103 二叉树的锯齿形层序遍历、LC 515 在每个树行中找最大值
