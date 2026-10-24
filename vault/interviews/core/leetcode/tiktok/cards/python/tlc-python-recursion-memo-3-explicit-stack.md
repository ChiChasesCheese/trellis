---
id: tlc-python-recursion-memo-3-explicit-stack
node: python.recursion-memo
type: qa
step: 3
---
## Q
**Python 递归｜二叉树的前序、中序、后序改成显式栈**

深度 `10^5` 的树不能递归，三种遍历怎样用显式栈写？后序有什么常用的简化技巧？

## A
```python
def preorder(root: TreeNode | None) -> list[int]:
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append(n.val)
        if n.right: st.append(n.right)     # 后进先出：先压右，再压左，左先出
        if n.left: st.append(n.left)
    return out
def inorder(root: TreeNode | None) -> list[int]:
    out: list[int] = []; st: list[TreeNode] = []; cur = root
    while cur or st:
        while cur:                          # 一路向左压栈
            st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val) # 左到底了，访问
        cur = cur.right                     # 转向右子树
    return out
def postorder(root: TreeNode | None) -> list[int]:
    out, st = [], [root] if root else []
    while st:                               # 做「根、右、左」的前序，再整体反转
        n = st.pop(); out.append(n.val)
        if n.left: st.append(n.left)
        if n.right: st.append(n.right)
    return out[::-1]
t = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
print(preorder(t), inorder(t), postorder(t))
# [1, 2, 4, 5, 3] [4, 2, 5, 1, 3] [4, 5, 2, 3, 1]
```

- 三种写法在 `10^5` 深度的单链树上都能正常返回（显式栈放在堆上，没有递归深度上限）。
- 后序「反转的前序」技巧：后序是「左、右、根」，把它反过来是「根、右、左」，只需把前序里左右的压栈顺序对调；比用 `(node, visited)` 标记短，但只适用于只要访问序的场合。
- 需要在后序时**用到子树的返回值**（树形 DP，如 LC 124、543）：显式栈里压 `(node, 已处理标记)`，第二次弹出时子节点的结果已经算好，放进字典 `res[node]`。
- 通用规则：递归调用 = 压栈；递归返回 = 弹栈；需要「回来之后还要做事」的递归，用带标记的栈元素。
