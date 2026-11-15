---
slug: complete-binary-tree-inserter
---
## Q
**LC 919 完全二叉树插入器**｜Medium

用一棵完全二叉树初始化，实现 `insert(val)`：在保持完全二叉树的前提下插入新结点并返回其父结点的值；`get_root()` 返回根。

## A
**一句话。** 按层序维护一个队列，装「还有空孩子位」的结点；队首就是下一个插入的父亲，左右都满后弹出。

```python
class CBTInserter:
    def __init__(self, root):
        self.root = root
        self.q = deque()     # 层序里还没满的结点
        bfs = deque([root])
        while bfs:
            node = bfs.popleft()
            if node.left:
                bfs.append(node.left)
            if node.right:
                bfs.append(node.right)
            if not (node.left and node.right):
                self.q.append(node)

    def insert(self, val):
        node = TreeNode(val)
        parent = self.q[0]
        if not parent.left:
            parent.left = node
        else:
            parent.right = node
            self.q.popleft()     # 左右都满了
        self.q.append(node)      # 新结点也有两个空位
        return parent.val

    def get_root(self):
        return self.root
```

**复杂度。** 初始化 `O(n)`，`insert` 摊还 `O(1)`，空间 `O(n)`。

**易错点。**
- 插入左孩子时也弹出队首：父结点还有右孩子位，会被跳过。
- 新结点不入队：之后永远不会挂在它下面。

**追问。**
- 不用队列怎么找位置？：把结点按层序编号，新结点编号 `k` 的父亲是 `k // 2`，用编号的二进制路径从根走下去，`O(log n)`。
- 为什么队里只有末尾附近的结点？：完全二叉树里「没满」的结点在层序上是连续的最后一段。

**同模式。** LC 958 二叉树的完全性检验、LC 222 完全二叉树的节点个数、LC 662 二叉树最大宽度
