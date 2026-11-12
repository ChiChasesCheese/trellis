---
slug: check-completeness-of-a-binary-tree
---
## Q
**LC 958 二叉树的完全性检验**｜Medium

判断二叉树是否为完全二叉树：除最后一层外都填满，且最后一层节点尽量靠左。

## A
**一句话。** 层序 BFS 时把空孩子也入队，遇到第一个空位之后若再出现真实节点就不是完全二叉树。

```python
def is_complete_tree(root):
    q = deque([root])
    gap = False                # 是否已遇到空位
    while q:
        node = q.popleft()
        if not node:
            gap = True
            continue
        if gap:                # 空位后又出现节点
            return False
        q.append(node.left)
        q.append(node.right)
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只检查「有右孩子没左孩子」：`[1,2,3,None,None,4]` 中 `2` 是叶子、`3` 却有孩子，局部检查放过它，应返回 `False`。
- 入队前过滤 `None`：空位信息丢了。

**追问。**
- 不用空位标记行不行？：给节点堆式编号（根 `1`，左 `2i`，右 `2i+1`），完全二叉树当且仅当节点数等于最大编号。
- 完全二叉树节点数怎么 `O(log^2 n)` 求？：比较左右最左路径高度，一侧满就用公式（LC 222）。

**同模式。** LC 102 二叉树层序遍历、LC 222 完全二叉树的节点个数、LC 919 完全二叉树插入器、LC 662 二叉树最大宽度
