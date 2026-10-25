---
id: tlc-flatten-binary-tree-to-linked-list-2-code
node: b.flatten-binary-tree-to-linked-list
type: qa
step: 2
---
## Q
**LC 114 二叉树展开为链表**｜写出 Python 实现

二叉树节点数在 `[0, 2000]`，值在 `[-100, 100]`。原地展开成单链表：`right` 指向下一个节点，`left` 全为 `null`，顺序与先序相同。要求 `O(n)` 时间、`O(1)` 额外空间，函数无返回值。

## A
**思路。** 从根开始，沿 `right` 向下走。遇到有左子树的节点 `cur`：沿左孩子的右链走到末端 `pred`，把 `cur.right` 接到 `pred.right`，再把 `cur.left` 搬到 `cur.right`，`cur.left` 置空。没有左子树就直接走向右。

```python
def flatten(root: TreeNode | None) -> None:
    cur = root
    while cur:
        if cur.left:
            pred = cur.left                # 从左孩子出发，沿右链走到头
            while pred.right:
                pred = pred.right
            pred.right = cur.right         # 先把原右子树接在右链末端
            cur.right = cur.left           # 再把左子树整体搬到右边
            cur.left = None
        cur = cur.right
```

运行：`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`，`[]` → `[]`，`[0]` → `[0]`；深度 2000 的左链展开后，沿 `right` 数到 `2000` 个节点且每个 `left` 都是 `None`。

**复杂度。** 时间 `O(n)`：每个节点至多被「沿右链找末端」的内层循环经过一次（搬到主链之后，它只能经 `right` 到达，不会再出现在别的节点的左子树里）；空间 `O(1)`，只有两个指针。

**写法要点。** `while cur:` 同时处理 `root` 为空；`if cur.left` 用节点对象的真值判断非空；两步赋值的顺序不能换（先接右、再搬左）；不返回任何值，修改的是传入的树。想要更短可以写递归「逆后序」，但深度 2000 的树会超过递归上限。
